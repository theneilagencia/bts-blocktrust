#!/usr/bin/env python3
"""
Script para aplicar migration 002: Adicionar coluna failsafe_password_hash
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Obter DATABASE_URL do Render
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL não configurada!")
    print("   Configure com: export DATABASE_URL='postgres://...'")
    exit(1)

print("🔗 Conectando ao banco de dados...")
print(f"   URL: {DATABASE_URL[:30]}...")

try:
    # Conectar ao banco
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    print("✅ Conectado com sucesso!")
    
    # Ler migration
    migration_path = 'backend/migrations/002_add_failsafe_password.sql'
    
    print(f"\n📄 Lendo migration: {migration_path}")
    
    with open(migration_path, 'r') as f:
        migration_sql = f.read()
    
    print(f"   Tamanho: {len(migration_sql)} bytes")
    
    # Aplicar migration
    print("\n🚀 Aplicando migration...")
    
    cur.execute(migration_sql)
    conn.commit()
    
    print("✅ Migration aplicada com sucesso!")
    
    # Verificar se colunas foram criadas
    print("\n🔍 Verificando colunas criadas...")
    
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'users'
        AND column_name IN ('failsafe_password_hash', 'failsafe_configured')
        ORDER BY column_name
    """)
    
    columns = cur.fetchall()
    
    if columns:
        print(f"✅ Colunas encontradas: {len(columns)}")
        for col in columns:
            print(f"   - {col['column_name']}: {col['data_type']}")
    else:
        print("⚠️  Nenhuma coluna encontrada!")
    
    cur.close()
    conn.close()
    
    print("\n✅ Script concluído com sucesso!")
    
except Exception as e:
    print(f"\n❌ Erro ao aplicar migration: {str(e)}")
    if conn:
        conn.rollback()
    exit(1)

