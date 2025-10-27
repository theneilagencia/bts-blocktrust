import { useState } from 'react'
import { ethers } from 'ethers'
import Layout from '../components/Layout'
import Card from '../components/Card'
import Button from '../components/Button'
import Input from '../components/Input'
import FileDrop from '../components/FileDrop'
import HashField from '../components/HashField'
import { showToast } from '../components/Toaster'
import { calculateSHA256 } from '../lib/hash'
import api from '../lib/api'
import {
  HashMode,
  normalizeBytes32FromHexNoPrefix,
  computeKeccakFromFile,
  ensurePolygonNetwork,
  retryWithBackoff,
  extractErrorMessage,
  logTransaction,
} from '../lib/blockchain'

export default function RegisterDoc() {
  const [file, setFile] = useState<File | null>(null)
  const [hash, setHash] = useState('')
  const [wallet, setWallet] = useState('')
  const [loading, setLoading] = useState(false)
  const [txHash, setTxHash] = useState('')
  const [hashMode, setHashMode] = useState<HashMode>('sha256')
  const [manualHash, setManualHash] = useState('')

  const handleFileSelect = async (selectedFile: File) => {
    setFile(selectedFile)
    showToast('info', `Calculando hash ${hashMode.toUpperCase()}...`)
    
    try {
      let calculatedHash: string

      if (hashMode === 'sha256') {
        calculatedHash = await calculateSHA256(selectedFile)
        // Normalizar para bytes32 (garantir prefixo 0x)
        calculatedHash = normalizeBytes32FromHexNoPrefix(calculatedHash)
      } else {
        // Keccak-256
        calculatedHash = await computeKeccakFromFile(selectedFile)
      }

      setHash(calculatedHash)
      showToast('success', `Hash ${hashMode.toUpperCase()} calculado com sucesso!`)
    } catch (error: any) {
      showToast('error', error.message || 'Erro ao calcular hash')
      console.error('Erro ao calcular hash:', error)
    }
  }

  const handleManualHashChange = (value: string) => {
    setManualHash(value)
    
    // Tentar normalizar em tempo real (sem mostrar erro)
    try {
      const normalized = normalizeBytes32FromHexNoPrefix(value)
      setHash(normalized)
    } catch {
      // Não fazer nada, deixar o usuário terminar de digitar
      setHash(value)
    }
  }

  const handleHashModeChange = async (mode: HashMode) => {
    setHashMode(mode)
    setHash('')
    setManualHash('')
    
    // Se já houver um arquivo selecionado, recalcular o hash
    if (file) {
      await handleFileSelect(file)
    }
  }

  const handleRegister = async () => {
    if (!hash || !wallet) {
      showToast('error', 'Preencha todos os campos')
      return
    }

    setLoading(true)

    try {
      // 1. Normalizar hash
      let normalizedHash: string
      try {
        normalizedHash = normalizeBytes32FromHexNoPrefix(hash)
      } catch (error: any) {
        showToast('error', error.message)
        setLoading(false)
        return
      }

      // 2. Garantir que está na rede Polygon
      showToast('info', 'Verificando rede Polygon...')
      try {
        await ensurePolygonNetwork()
      } catch (error: any) {
        showToast('error', error.message)
        setLoading(false)
        return
      }

      // 3. Obter chainId e endereço da wallet conectada
      const provider = new ethers.BrowserProvider(window.ethereum!)
      const network = await provider.getNetwork()
      const chainId = Number(network.chainId)
      const signer = await provider.getSigner()
      const signerAddress = await signer.getAddress()

      console.log('📍 Informações da transação:')
      console.log('  ChainId:', chainId)
      console.log('  Wallet:', signerAddress)
      console.log('  Hash Mode:', hashMode)
      console.log('  Document Hash:', normalizedHash)

      // 4. Registrar assinatura com retry
      showToast('info', 'Registrando documento na blockchain...')
      
      const response = await retryWithBackoff(async () => {
        return await api.post('/proxy/signature', {
          hash: normalizedHash,
          signer: wallet,
        })
      })

      const resultTxHash = response.data.tx_hash

      // 5. Log de sucesso
      logTransaction({
        timestamp: new Date().toISOString(),
        chainId,
        method: 'registerSignature',
        hashMode,
        docHash: normalizedHash,
        txHash: resultTxHash,
        status: 'success',
      })

      setTxHash(resultTxHash)
      showToast('success', 'Documento registrado na blockchain!')
      
    } catch (error: any) {
      // Extrair mensagem de erro detalhada
      const errorMessage = extractErrorMessage(error)
      
      // Log de erro
      logTransaction({
        timestamp: new Date().toISOString(),
        chainId: 137, // Assumir Polygon
        method: 'registerSignature',
        hashMode,
        docHash: hash,
        status: 'error',
        error: errorMessage,
      })

      console.error('❌ Erro ao registrar documento:', error)
      showToast('error', errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto space-y-8">
        <div>
          <h1 className="font-display text-3xl font-bold mb-2">Registrar Documento</h1>
          <p className="text-gray-600">
            Faça o registro blockchain do seu documento de forma segura e privada
          </p>
        </div>

        <Card title="Configurações de Hash">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Modo de Hash
              </label>
              <div className="flex space-x-4">
                <button
                  onClick={() => handleHashModeChange('sha256')}
                  className={`px-4 py-2 rounded-lg font-medium transition ${
                    hashMode === 'sha256'
                      ? 'bg-brand-blue text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  SHA-256
                </button>
                <button
                  onClick={() => handleHashModeChange('keccak256')}
                  className={`px-4 py-2 rounded-lg font-medium transition ${
                    hashMode === 'keccak256'
                      ? 'bg-brand-blue text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Keccak-256
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                {hashMode === 'sha256'
                  ? 'SHA-256: Padrão para a maioria dos casos (compatível com certificados digitais)'
                  : 'Keccak-256: Hash nativo do Ethereum/Polygon (usado em contratos inteligentes)'}
              </p>
            </div>

            {hashMode === 'sha256' && (
              <div>
                <Input
                  label="Hash Manual (Opcional)"
                  value={manualHash}
                  onChange={(e) => handleManualHashChange(e.target.value)}
                  placeholder="Cole o hash SHA-256 aqui (com ou sem 0x)"
                  helperText="Se você já tem o hash SHA-256, pode colá-lo aqui ao invés de fazer upload do arquivo"
                />
              </div>
            )}
          </div>
        </Card>

        <Card title="1. Selecione o Documento">
          <FileDrop onFileSelect={handleFileSelect} />
          {file && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Arquivo selecionado:</p>
              <p className="font-medium">{file.name}</p>
              <p className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
          )}
        </Card>

        {hash && (
          <Card title="2. Hash do Documento">
            <HashField hash={hash} />
            <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Modo:</strong> {hashMode.toUpperCase()}
              </p>
              <p className="text-xs text-blue-600 mt-1">
                Este hash representa seu documento de forma única e será registrado na blockchain Polygon.
              </p>
            </div>
          </Card>
        )}

        {hash && (
          <Card title="3. Informações de Registro">
            <div className="space-y-4">
              <Input
                label="Endereço da Wallet (Polygon)"
                value={wallet}
                onChange={(e) => setWallet(e.target.value)}
                placeholder="0x..."
                required
                helperText="Certifique-se de que sua carteira MetaMask está conectada à rede Polygon (chainId 137)"
              />

              <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-sm text-yellow-800">
                  ⚠️ <strong>Importante:</strong> Antes de registrar, certifique-se de que:
                </p>
                <ul className="text-xs text-yellow-700 mt-2 ml-4 list-disc space-y-1">
                  <li>Sua carteira MetaMask está instalada e desbloqueada</li>
                  <li>Você está conectado à rede <strong>Polygon Mainnet (chainId 137)</strong></li>
                  <li>Você tem MATIC suficiente para pagar a taxa de gas</li>
                </ul>
              </div>

              <Button
                onClick={handleRegister}
                disabled={loading || !wallet}
                className="w-full"
              >
                {loading ? 'Registrando...' : 'Registrar na Blockchain'}
              </Button>
            </div>
          </Card>
        )}

        {txHash && (
          <Card title="✅ Registro Concluído">
            <div className="space-y-4">
              <p className="text-green-600 font-medium">
                Seu documento foi registrado com sucesso na blockchain Polygon!
              </p>
              <HashField hash={txHash} label="Transaction Hash" />
              <a
                href={`https://polygonscan.com/tx/${txHash}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-4 py-2 bg-brand-blue text-white rounded-lg hover:bg-blue-700 transition"
              >
                Ver transação no PolygonScan →
              </a>
            </div>
          </Card>
        )}
      </div>
    </Layout>
  )
}

