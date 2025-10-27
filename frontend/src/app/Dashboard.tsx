import { useEffect, useState } from 'react'
import { useAuth } from '@/lib/auth'
import Layout from '@/components/Layout'
import Card from '@/components/Card'
import StatusBadge from '@/components/StatusBadge'
import api from '@/lib/api'
import { FileText, CheckCircle, AlertTriangle, User } from 'lucide-react'

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    identities: 0,
    signatures: 0,
    alerts: 0,
  })
  const [recentSignatures, setRecentSignatures] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      // Aqui você faria as chamadas reais para a API
      // Por enquanto, dados mockados
      setStats({
        identities: 1,
        signatures: 5,
        alerts: 0,
      })
      setRecentSignatures([
        {
          id: 1,
          hash: 'a1b2c3d4e5f6...',
          created_at: '2024-01-15T10:30:00Z',
          status: 'verified',
        },
      ])
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600">Carregando...</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h1 className="font-display text-3xl font-bold mb-2">Painel de Controle</h1>
          <p className="text-gray-600">Bem-vindo, {user?.email}</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <Card className="flex items-center space-x-4">
            <div className="bg-blue-100 p-3 rounded-lg">
              <User className="w-8 h-8 text-brand-blue" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Identidades</p>
              <p className="text-2xl font-bold">{stats.identities}</p>
            </div>
          </Card>

          <Card className="flex items-center space-x-4">
            <div className="bg-green-100 p-3 rounded-lg">
              <FileText className="w-8 h-8 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Assinaturas</p>
              <p className="text-2xl font-bold">{stats.signatures}</p>
            </div>
          </Card>

          <Card className="flex items-center space-x-4">
            <div className="bg-red-100 p-3 rounded-lg">
              <AlertTriangle className="w-8 h-8 text-red-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Alertas</p>
              <p className="text-2xl font-bold">{stats.alerts}</p>
            </div>
          </Card>
        </div>

        <Card title="Assinaturas Recentes">
          {recentSignatures.length === 0 ? (
            <p className="text-gray-600 text-center py-8">Nenhuma assinatura registrada ainda</p>
          ) : (
            <div className="space-y-4">
              {recentSignatures.map((sig) => (
                <div key={sig.id} className="flex items-center justify-between border-b pb-4">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <div>
                      <p className="font-mono text-sm">{sig.hash}</p>
                      <p className="text-xs text-gray-500">
                        {new Date(sig.created_at).toLocaleString('pt-BR')}
                      </p>
                    </div>
                  </div>
                  <StatusBadge status="success">Verificado</StatusBadge>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </Layout>
  )
}

