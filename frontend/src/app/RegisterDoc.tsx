import { useState } from 'react'
import Layout from '../components/Layout'
import Card from '../components/Card'
import Button from '../components/Button'
import Input from '../components/Input'
import FileDrop from '../components/FileDrop'
import HashField from '../components/HashField'
import { showToast } from '../components/Toaster'
import { calculateSHA256 } from '../lib/hash'
import api from '../lib/api'

export default function RegisterDoc() {
  const [file, setFile] = useState<File | null>(null)
  const [hash, setHash] = useState('')
  const [wallet, setWallet] = useState('')
  const [loading, setLoading] = useState(false)
  const [txHash, setTxHash] = useState('')

  const handleFileSelect = async (selectedFile: File) => {
    setFile(selectedFile)
    showToast('info', 'Calculando hash...')
    
    try {
      const calculatedHash = await calculateSHA256(selectedFile)
      setHash(calculatedHash)
      showToast('success', 'Hash calculado com sucesso!')
    } catch (error) {
      showToast('error', 'Erro ao calcular hash')
    }
  }

  const handleRegister = async () => {
    if (!hash || !wallet) {
      showToast('error', 'Preencha todos os campos')
      return
    }

    setLoading(true)

    try {
      const response = await api.post('/proxy/signature', {
        hash,
        signer: wallet,
      })

      setTxHash(response.data.tx_hash)
      showToast('success', 'Documento registrado na blockchain!')
    } catch (error: any) {
      showToast('error', error.response?.data?.error || 'Erro ao registrar documento')
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
            <p className="text-sm text-gray-600 mt-2">
              Este hash representa seu documento de forma única e será registrado na blockchain.
            </p>
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
              />

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
                Seu documento foi registrado com sucesso na blockchain!
              </p>
              <HashField hash={txHash} label="Transaction Hash" />
              <a
                href={`https://polygonscan.com/tx/${txHash}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-brand-blue hover:underline text-sm"
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

