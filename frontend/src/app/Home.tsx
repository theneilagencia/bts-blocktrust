import { Link } from 'react-router-dom'
import { Shield, FileCheck, Lock, Globe, Wallet, Key, AlertTriangle, FileSignature, CheckCircle, ArrowRight } from 'lucide-react'
import Button from '../components/Button'

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="container-custom py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <img src="/logo-black.png" alt="BTS Blocktrust" className="h-8" />
              <span className="text-xs bg-brand-blue text-white px-2 py-1 rounded-full font-medium">v1.4</span>
            </div>
            <div className="flex items-center space-x-3">
              <Link to="/login">
                <Button variant="secondary" className="text-sm">Entrar</Button>
              </Link>
              <Link to="/register">
                <Button className="text-sm">Criar Conta</Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 bg-gradient-to-b from-gray-50 to-white">
        <div className="container-custom">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="font-display text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Identidade Digital Soberana e Assinatura Blockchain
            </h1>
            <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
              Sistema completo de identidade verificada (KYC), carteira autocustodiada, 
              NFT SoulBound e assinatura dupla (PGP + Blockchain) com protocolo de emergência
            </p>
            <Link to="/register">
              <Button size="lg" className="text-base px-8 py-4 shadow-lg hover:shadow-xl transition-shadow">
                Começar Agora
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          </div>

          {/* Video Section */}
          <div className="mt-16 max-w-5xl mx-auto">
            <div className="relative aspect-video rounded-2xl overflow-hidden shadow-2xl border border-gray-200">
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
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 bg-white">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Módulos e Funcionalidades
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Tecnologia de ponta para garantir segurança, privacidade e controle total da sua identidade digital
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {/* Card 1 */}
            <div className="group bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl hover:border-brand-blue transition-all duration-300">
              <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-brand-blue transition-colors">
                <Wallet className="w-7 h-7 text-brand-blue group-hover:text-white transition-colors" />
              </div>
              <h3 className="font-display text-lg font-bold text-gray-900 mb-3">Carteira Proprietária</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Geração e gerenciamento de chaves privadas secp256k1 com criptografia local
              </p>
            </div>

            {/* Card 2 */}
            <div className="group bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl hover:border-brand-blue transition-all duration-300">
              <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-brand-blue transition-colors">
                <Shield className="w-7 h-7 text-brand-blue group-hover:text-white transition-colors" />
              </div>
              <h3 className="font-display text-lg font-bold text-gray-900 mb-3">NFT SoulBound</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Identidade única não-transferível vinculada ao KYC com cancelamento automático
              </p>
            </div>

            {/* Card 3 */}
            <div className="group bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl hover:border-brand-blue transition-all duration-300">
              <div className="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-brand-blue transition-colors">
                <FileSignature className="w-7 h-7 text-brand-blue group-hover:text-white transition-colors" />
              </div>
              <h3 className="font-display text-lg font-bold text-gray-900 mb-3">Assinatura Dupla</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                PGP + Blockchain para máxima segurança e não-repúdio de documentos
              </p>
            </div>

            {/* Card 4 */}
            <div className="group bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl hover:border-red-500 transition-all duration-300">
              <div className="w-14 h-14 bg-red-50 rounded-xl flex items-center justify-center mb-6 group-hover:bg-red-500 transition-colors">
                <AlertTriangle className="w-7 h-7 text-red-500 group-hover:text-white transition-colors" />
              </div>
              <h3 className="font-display text-lg font-bold text-gray-900 mb-3">Protocolo Failsafe</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                Senha de emergência para situações de coação com cancelamento automático de NFT
              </p>
            </div>
          </div>

          {/* Additional Features */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <FileCheck className="w-8 h-8 text-brand-blue" />
              </div>
              <h3 className="font-display text-xl font-bold text-gray-900 mb-3">KYC Integrado</h3>
              <p className="text-gray-600 leading-relaxed">
                Verificação de identidade via KYC com liveness e mint automático de NFT
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Lock className="w-8 h-8 text-brand-blue" />
              </div>
              <h3 className="font-display text-xl font-bold text-gray-900 mb-3">Privacidade Total</h3>
              <p className="text-gray-600 leading-relaxed">
                Chaves privadas nunca saem do dispositivo. Criptografia AES-256 + PBKDF2
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Globe className="w-8 h-8 text-brand-blue" />
              </div>
              <h3 className="font-display text-xl font-bold text-gray-900 mb-3">Blockchain Polygon</h3>
              <p className="text-gray-600 leading-relaxed">
                Registro imutável e verificável em blockchain pública de baixo custo
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Como Funciona o Blocktrust
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Processo simples e seguro em três etapas principais
            </p>
          </div>

          <div className="max-w-5xl mx-auto space-y-16">
            {/* Step 1 */}
            <div className="flex flex-col md:flex-row gap-8 items-start">
              <div className="flex-shrink-0">
                <div className="w-16 h-16 bg-brand-blue text-white rounded-2xl flex items-center justify-center font-display text-2xl font-bold">
                  1
                </div>
              </div>
              <div className="flex-1">
                <h3 className="font-display text-2xl font-bold text-gray-900 mb-4">Cadastro e Verificação</h3>
                <div className="space-y-4 text-gray-700 leading-relaxed">
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
            </div>

            <div className="border-t border-gray-300"></div>

            {/* Step 2 */}
            <div className="flex flex-col md:flex-row gap-8 items-start">
              <div className="flex-shrink-0">
                <div className="w-16 h-16 bg-brand-blue text-white rounded-2xl flex items-center justify-center font-display text-2xl font-bold">
                  2
                </div>
              </div>
              <div className="flex-1">
                <h3 className="font-display text-2xl font-bold text-gray-900 mb-4">Assinatura de Documentos</h3>
                <div className="space-y-4 text-gray-700 leading-relaxed">
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
                  <ul className="space-y-2 ml-6">
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-brand-blue mr-3 mt-0.5 flex-shrink-0" />
                      <span>ECDSA, com sua chave privada local Blocktrust.</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-brand-blue mr-3 mt-0.5 flex-shrink-0" />
                      <span>PGP, para compatibilidade adicional com outras plataformas.</span>
                    </li>
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
            </div>

            <div className="border-t border-gray-300"></div>

            {/* Step 3 */}
            <div className="flex flex-col md:flex-row gap-8 items-start">
              <div className="flex-shrink-0">
                <div className="w-16 h-16 bg-brand-blue text-white rounded-2xl flex items-center justify-center font-display text-2xl font-bold">
                  3
                </div>
              </div>
              <div className="flex-1">
                <h3 className="font-display text-2xl font-bold text-gray-900 mb-4">Verificação e Auditoria</h3>
                <div className="space-y-4 text-gray-700 leading-relaxed">
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
                  <ul className="space-y-2 ml-6">
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-brand-blue mr-3 mt-0.5 flex-shrink-0" />
                      <span>Histórico de assinaturas e cancelamentos</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-brand-blue mr-3 mt-0.5 flex-shrink-0" />
                      <span>Registro de eventos on-chain (Minting, Proof, Failsafe, etc.)</span>
                    </li>
                    <li className="flex items-start">
                      <CheckCircle className="w-5 h-5 text-brand-blue mr-3 mt-0.5 flex-shrink-0" />
                      <span>Logs em tempo real, com atualização automática.</span>
                    </li>
                  </ul>
                  <p>
                    Cada ação é registrada de forma pública, imutável e auditável — transformando confiança em código.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Failsafe Protocol Section */}
      <section className="py-20 bg-gradient-to-br from-red-50 to-orange-50">
        <div className="container-custom">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-start gap-6 mb-8">
              <div className="flex-shrink-0">
                <div className="w-16 h-16 bg-red-500 text-white rounded-2xl flex items-center justify-center">
                  <AlertTriangle className="w-8 h-8" />
                </div>
              </div>
              <div>
                <h2 className="font-display text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                  Protocolo de Emergência (Failsafe)
                </h2>
                <p className="text-lg text-gray-700 leading-relaxed">
                  Proteção avançada para situações de coerção ou ameaça
                </p>
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 md:p-10 shadow-xl border border-gray-200">
              <div className="space-y-6 text-gray-700 leading-relaxed">
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
                <p className="font-medium text-gray-900">
                  Isso preserva a cadeia de auditoria simbiótica, garantindo rastreabilidade e transparência total ao longo do tempo.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-brand-navy text-white">
        <div className="container-custom text-center">
          <h2 className="font-display text-3xl md:text-5xl font-bold mb-6">
            Pronto para começar?
          </h2>
          <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
            Crie sua identidade digital soberana agora e tenha controle total sobre suas assinaturas e documentos
          </p>
          <Link to="/register">
            <Button size="lg" className="bg-white text-brand-navy hover:bg-gray-100 text-base px-8 py-4 shadow-lg">
              Criar Conta Gratuita
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="container-custom">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <img src="/logo.png" alt="BTS Blocktrust" className="h-8" />
              <span className="text-sm">Sistema descentralizado de registro blockchain</span>
            </div>
            <p className="text-sm">
              2025 BTS Global Corp © Todos os direitos reservados
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

