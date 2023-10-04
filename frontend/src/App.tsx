// import { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Flex } from '@chakra-ui/react'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import HomePage from './components/HomePage'
import NotFound from './components/NotFound'
import Login from './components/Authentication/Login'
import Register from './components/Authentication/Register'
import ForgotPassword from './components/Authentication/ForgotPassword'
import Dashboard from './components/Dashboard'
import AddAssets from './components/AddAssets'
function App() {

  return (
    <>
    <Flex direction='column' h={'100vh'}>
      <Router>
        <Navbar isLoggedIn={true} />
        <Flex direction='column' flex='1'>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/add-assets" element={<AddAssets />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        </Flex>
        <Footer />
      </Router>
    </Flex>
    </>
  )
}

export default App
