import { Link } from 'react-router-dom'
import { Shield, FileCheck, Lock, Globe } from 'lucide-react'
import Button from '../components/Button'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-navy to-brand-neutral text-white">
      <nav className="container-custom py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <img src="/logo.png" alt="BTS Blocktrust" className="h-10" />
          </div>
          <div className="space-x-4">
            <Link to="/login">
              <Button variant="secondary">Entrar</Button>
            </Link>
            <Link to="/register">
              <Button>Criar Conta</Button>
            </Link>
          </div>
        </div>
      </nav>

      <div className="container-custom py-20">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="font-display text-5xl md:text-6xl font-bold mb-6">
            Registro Blockchain de Documentos
          </h1>
          <p className="text-xl text-gray-300 mb-12">
            Sistema descentralizado para registro, assinatura e verificação de documentos 
            com segurança blockchain e conformidade LGPD
          </p>
          <Link to="/register">
            <Button size="lg" className="text-lg px-8 py-4">
              Começar Agora
            </Button>
          </Link>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 text-center">
            <FileCheck className="w-12 h-12 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold mb-2">Registro Seguro</h3>
            <p className="text-gray-300">
              Registre documentos na blockchain Polygon com hash SHA-256
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 text-center">
            <Lock className="w-12 h-12 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold mb-2">Privacidade Total</h3>
            <p className="text-gray-300">
              Apenas o hash trafega. Seus documentos permanecem privados
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 text-center">
            <Globe className="w-12 h-12 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold mb-2">Verificação Global</h3>
            <p className="text-gray-300">
              Verifique autenticidade instantaneamente via blockchain
            </p>
          </div>
        </div>
      </div>

      <footer className="container-custom py-8 mt-20 border-t border-white/20">
        <p className="text-center text-gray-400">
          2025 BTS Global Corp © Todos os direitos reservados
        </p>
      </footer>
    </div>
  )
}

