#!/usr/bin/env python3
"""
Script para aplicar migrations no banco de dados PostgreSQL via Render Shell
"""
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def apply_migration():
    """Aplica a migration consolidada no banco de dados"""
    
    # Conectar ao banco de dados usando DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERRO: DATABASE_URL não encontrada!")
        return False
    
    print(f"📡 Conectando ao banco de dados...")
    
    try:
        conn = psycopg2.connect(database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Conectado com sucesso!")
        
        # Ler arquivo de migration
        migration_file = '/opt/render/project/src/backend/migrations/001_complete_schema.sql'
        print(f"📄 Lendo migration: {migration_file}")
        
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        print(f"📝 Migration tem {len(migration_sql)} caracteres")
        print("🚀 Aplicando migration...")
        
        # Executar migration
        cursor.execute(migration_sql)
        
        print("✅ Migration aplicada com sucesso!")
        
        # Verificar tabelas criadas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 Tabelas no banco de dados ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO ao aplicar migration: {e}")
        return False

if __name__ == '__main__':
    success = apply_migration()
    exit(0 if success else 1)

