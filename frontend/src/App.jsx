import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Register from './components/authentication/Register'
import Login from './components/authentication/Login'
import PasswordResetPage from './components/authentication/PasswordResetPage'
import AuthenticationPage from './components/authentication/AuthenticationPage'
import DashboardPage from './pages/DashboardPage'
import UserList from './pages/UserList'
import Teamwork from './pages/TeamWork'

function App() {

  return (
    <>
        <Router>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/authentication" element={<AuthenticationPage />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path='/password-reset' element={<PasswordResetPage />} />
            <Route path='/users' element={<UserList />} />
            <Route path='/teamwork' element={<Teamwork />} />
          </Routes>
        </Router>
        <ToastContainer />
    </>
  )
}

export default App