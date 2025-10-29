import { Link } from 'react-router-dom'
import { Shield, FileCheck, Lock, Globe, Wallet, Key, AlertTriangle, FileSignature } from 'lucide-react'
import Button from '../components/Button'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-navy to-brand-neutral text-white">
      <nav className="container-custom py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <img src="/logo.png" alt="BTS Blocktrust" className="h-10" />
            <span className="text-sm bg-brand-accent px-2 py-1 rounded">v1.4</span>
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
            Identidade Digital Soberana e Assinatura Blockchain
          </h1>
          <p className="text-xl text-gray-300 mb-12">
            Sistema completo de identidade verificada (KYC), carteira autocustodiada, 
            NFT SoulBound e assinatura dupla (PGP + Blockchain) com protocolo de emergência
          </p>

          {/* Vídeo institucional */}
          <div className="w-full flex flex-col items-center justify-center mt-10 mb-16">
            <div className="w-full max-w-4xl aspect-video rounded-2xl overflow-hidden shadow-lg">
              <iframe
                className="w-full h-full"
                src="https://www.youtube.com/embed/HAz8u9dWt28"
                title="Conheça o BTS Blocktrust"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                loading="lazy"
              ></iframe>
            </div>
          </div>

          <Link to="/register">
            <Button size="lg" className="text-lg px-8 py-4">
              Começar Agora
            </Button>
          </Link>
        </div>

        {/* Módulos Principais */}
        <div className="mt-20 mb-12">
          <h2 className="font-display text-3xl font-bold text-center mb-12">
            Módulos e Funcionalidades
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center hover:bg-white/20 transition">
              <Wallet className="w-12 h-12 mx-auto mb-4 text-brand-accent" />
              <h3 className="font-display text-lg font-bold mb-2">Carteira Proprietária</h3>
              <p className="text-sm text-gray-300">
                Geração e gerenciamento de chaves privadas secp256k1 com criptografia local
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center hover:bg-white/20 transition">
              <Shield className="w-12 h-12 mx-auto mb-4 text-brand-accent" />
              <h3 className="font-display text-lg font-bold mb-2">NFT SoulBound</h3>
              <p className="text-sm text-gray-300">
                Identidade única não-transferível vinculada ao KYC com cancelamento automático
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center hover:bg-white/20 transition">
              <FileSignature className="w-12 h-12 mx-auto mb-4 text-brand-accent" />
              <h3 className="font-display text-lg font-bold mb-2">Assinatura Dupla</h3>
              <p className="text-sm text-gray-300">
                PGP + Blockchain para máxima segurança e não-repúdio de documentos
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center hover:bg-white/20 transition">
              <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-red-400" />
              <h3 className="font-display text-lg font-bold mb-2">Protocolo Failsafe</h3>
              <p className="text-sm text-gray-300">
                Senha de emergência para situações de coação com cancelamento automático de NFT
              </p>
            </div>
          </div>
        </div>

        {/* Funcionalidades Detalhadas */}
        <div className="grid md:grid-cols-3 gap-8 mt-12">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 text-center">
            <FileCheck className="w-12 h-12 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold mb-2">KYC Integrado</h3>
            <p className="text-gray-300">
              Verificação de identidade via Sumsub com liveness e mint automático de NFT
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 text-center">
            <Lock className="w-12 h-12 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold mb-2">Privacidade Total</h3>
            <p className="text-gray-300">
              Chaves privadas nunca saem do dispositivo. Criptografia AES-256 + PBKDF2
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 text-center">
            <Globe className="w-12 h-12 mx-auto mb-4" />
            <h3 className="font-display text-xl font-bold mb-2">Blockchain Polygon</h3>
            <p className="text-gray-300">
              Registro imutável e verificável em blockchain pública de baixo custo
            </p>
          </div>
        </div>

        {/* Fluxos de Uso */}
        <div className="mt-20 bg-white/5 backdrop-blur-sm rounded-2xl p-12">
          <h2 className="font-display text-3xl font-bold text-center mb-8">
            Como Funciona
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="font-display text-xl font-bold mb-4 flex items-center">
                <span className="bg-brand-accent text-brand-navy w-8 h-8 rounded-full flex items-center justify-center mr-3">1</span>
                Cadastro e Verificação
              </h3>
              <ul className="space-y-2 text-gray-300 ml-11">
                <li>• Crie conta com senha normal e senha de emergência</li>
                <li>• Complete o processo de KYC (verificação de identidade)</li>
                <li>• Sistema gera automaticamente sua carteira proprietária</li>
                <li>• NFT SoulBound é mintado e vinculado à sua identidade</li>
              </ul>
            </div>

            <div>
              <h3 className="font-display text-xl font-bold mb-4 flex items-center">
                <span className="bg-brand-accent text-brand-navy w-8 h-8 rounded-full flex items-center justify-center mr-3">2</span>
                Assinatura de Documentos
              </h3>
              <ul className="space-y-2 text-gray-300 ml-11">
                <li>• Importe sua chave pública PGP (opcional)</li>
                <li>• Faça upload do documento para assinar</li>
                <li>• Sistema valida seu NFT ativo na blockchain</li>
                <li>• Assinatura dupla (PGP + ECDSA) é registrada on-chain</li>
              </ul>
            </div>

            <div>
              <h3 className="font-display text-xl font-bold mb-4 flex items-center">
                <span className="bg-brand-accent text-brand-navy w-8 h-8 rounded-full flex items-center justify-center mr-3">3</span>
                Verificação e Auditoria
              </h3>
              <ul className="space-y-2 text-gray-300 ml-11">
                <li>• Qualquer pessoa pode verificar a autenticidade</li>
                <li>• Consulta pública na blockchain Polygon</li>
                <li>• Histórico completo de eventos e assinaturas</li>
                <li>• Explorer com logs de auditoria em tempo real</li>
              </ul>
            </div>

            <div>
              <h3 className="font-display text-xl font-bold mb-4 flex items-center">
                <span className="bg-red-400 text-brand-navy w-8 h-8 rounded-full flex items-center justify-center mr-3">⚠</span>
                Protocolo de Emergência
              </h3>
              <ul className="space-y-2 text-gray-300 ml-11">
                <li>• Use senha de emergência em situações de coação</li>
                <li>• Sistema gera assinatura fake indistinguível</li>
                <li>• NFT é cancelado automaticamente e secretamente</li>
                <li>• Todas as assinaturas futuras ficam inválidas</li>
              </ul>
            </div>
          </div>
        </div>


      </div>

      <footer className="container-custom py-8 mt-20 border-t border-white/20">
        <p className="text-center text-gray-400">
          2025 BTS Global Corp © Todos os direitos reservados | Blocktrust v1.4
        </p>
      </footer>
    </div>
  )
}

