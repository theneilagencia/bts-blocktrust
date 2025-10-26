import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Home from '@/app/Home'
import Login from '@/app/Login'
import Register from '@/app/Register'
import Dashboard from '@/app/Dashboard'
import RegisterDoc from '@/app/RegisterDoc'
import VerifyDoc from '@/app/VerifyDoc'
import Admin from '@/app/Admin'
import { AuthProvider, useAuth } from '@/lib/auth'
import Toaster from '@/components/Toaster'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user } = useAuth()
  return user ? <>{children}</> : <Navigate to="/login" />
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { user } = useAuth()
  return user && user.role === 'admin' ? <>{children}</> : <Navigate to="/dashboard" />
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/registrar" element={<PrivateRoute><RegisterDoc /></PrivateRoute>} />
          <Route path="/verificar" element={<PrivateRoute><VerifyDoc /></PrivateRoute>} />
          <Route path="/admin" element={<AdminRoute><Admin /></AdminRoute>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App

