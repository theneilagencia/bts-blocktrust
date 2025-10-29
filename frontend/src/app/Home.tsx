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
              Verificação de identidade via KYC com liveness e mint automático de NFT
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

        {/* Como Funciona */}
        <div className="mt-20 bg-white/5 backdrop-blur-sm rounded-2xl p-12">
          <h2 className="font-display text-3xl font-bold text-center mb-12">
            Como Funciona o Blocktrust
          </h2>
          
          <div className="space-y-12">
            {/* 1. Cadastro e Verificação */}
            <div>
              <h3 className="font-display text-2xl font-bold mb-6">1. Cadastro e Verificação</h3>
              <div className="space-y-4 text-gray-300 leading-relaxed">
                <p>
                  Crie uma conta com duas senhas: a senha principal e uma senha de emergência (failsafe), 
                  usada apenas em situações de risco.
                </p>
                <p>
                  Realize a verificação de identidade (KYC) com prova de vida diretamente pelo aplicativo.
                </p>
                <p>
                  O sistema gera automaticamente uma carteira digital autocustodiada, onde suas chaves privadas 
                  são armazenadas localmente e criptografadas.
                </p>
                <p>
                  Um NFT SoulBound — único, intransferível e auditável — é emitido na blockchain Polygon e 
                  vinculado permanentemente à sua identidade digital.
                </p>
                <p>
                  Esse NFT funciona como seu passaporte digital, comprovando identidade e legitimidade em qualquer operação.
                </p>
              </div>
            </div>

            <hr className="border-white/20" />

            {/* 2. Assinatura de Documentos */}
            <div>
              <h3 className="font-display text-2xl font-bold mb-6">2. Assinatura de Documentos</h3>
              <div className="space-y-4 text-gray-300 leading-relaxed">
                <p>
                  (Opcional) Importe sua chave pública PGP para ampliar a compatibilidade com sistemas externos.
                </p>
                <p>
                  Faça o upload do documento a ser assinado.
                </p>
                <p>
                  O sistema valida seu NFT ativo na blockchain, garantindo que sua identidade digital está íntegra.
                </p>
                <p>
                  O documento é assinado com dupla camada de segurança:
                </p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>ECDSA, com sua chave privada local Blocktrust.</li>
                  <li>PGP, para compatibilidade adicional com outras plataformas.</li>
                </ul>
                <p>
                  Apenas o hash criptográfico e os metadados de auditoria são registrados na blockchain — 
                  o conteúdo do documento nunca sai do seu dispositivo.
                </p>
                <p>
                  A assinatura é verificável, mas o conteúdo permanece totalmente privado.
                </p>
              </div>
            </div>

            <hr className="border-white/20" />

            {/* 3. Verificação e Auditoria */}
            <div>
              <h3 className="font-display text-2xl font-bold mb-6">3. Verificação e Auditoria</h3>
              <div className="space-y-4 text-gray-300 leading-relaxed">
                <p>
                  Qualquer pessoa pode verificar a autenticidade de um documento por meio do QR code do certificado 
                  ou do Explorer Blocktrust.
                </p>
                <p>
                  A consulta pública exibe o status do NFT, o hash do documento e o histórico completo de eventos 
                  diretamente na blockchain Polygon.
                </p>
                <p>
                  O painel de auditoria oferece:
                </p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>Histórico de assinaturas e cancelamentos</li>
                  <li>Registro de eventos on-chain (Minting, Proof, Failsafe, etc.)</li>
                  <li>Logs em tempo real, com atualização automática.</li>
                </ul>
                <p>
                  Cada ação é registrada de forma pública, imutável e auditável — transformando confiança em código.
                </p>
              </div>
            </div>

            <hr className="border-white/20" />

            {/* Protocolo de Emergência */}
            <div>
              <h3 className="font-display text-2xl font-bold mb-6">Protocolo de Emergência (Failsafe)</h3>
              <div className="space-y-4 text-gray-300 leading-relaxed">
                <p>
                  Em caso de coerção, fraude ou ameaça, o usuário pode acionar o modo de emergência com sua senha failsafe.
                </p>
                <p>
                  O sistema gera uma assinatura fake visualmente idêntica à real, enganando o invasor.
                </p>
                <p>
                  Simultaneamente, o NFT ativo é automaticamente marcado como inválido na blockchain, impedindo futuras 
                  assinaturas e acionando o protocolo de segurança.
                </p>
                <p>
                  O usuário pode, depois, refazer o KYC e emitir um novo NFT (v+1) para recuperar sua identidade digital.
                </p>
                <p>
                  O NFT não é apagado nem removido — ele permanece registrado na blockchain, apenas marcado como inválido.
                </p>
                <p>
                  Isso preserva a cadeia de auditoria simbiótica, garantindo rastreabilidade e transparência total ao longo do tempo.
                </p>
              </div>
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

