import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import Register from './components/authentication/Register'
import Login from './components/authentication/Login'
import PasswordResetPage from './components/authentication/PasswordResetPage'
import SetTasks from './components/AdminDashboard/SetTasks'
import AuthenticationPage from './components/authentication/AuthenticationPage'
import HomePage from './pages/HomePage'


function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<AuthenticationPage />} />
          <Route path="/authentication" element={<AuthenticationPage />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path='/password-reset' element={<PasswordResetPage />} />
          <Route path='/home' element={<HomePage />} />
          <Route path='/settasks' element={<SetTasks />} />
        </Routes>
      </Router>
      <ToastContainer />
    </>
  )
}

export default App
