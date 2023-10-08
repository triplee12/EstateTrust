import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import customTheme from './assets/custom_theme.ts'
import { extendTheme, ChakraProvider } from "@chakra-ui/react"
import { PersistGate } from 'redux-persist/integration/react'
import {store} from './store'
import { Provider } from 'react-redux';
import { persistor } from './store';

const theme = extendTheme(customTheme)
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <ChakraProvider theme={theme}>
          <App />
        </ChakraProvider>
      </PersistGate>
    </Provider>
  </React.StrictMode>,
)
