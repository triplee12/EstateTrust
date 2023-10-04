import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import customTheme from './assets/custom_theme.ts'
import { extendTheme, ChakraProvider } from "@chakra-ui/react"


const theme = extendTheme(customTheme)
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>,
)
