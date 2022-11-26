import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
// import chakra
import { ChakraProvider } from '@chakra-ui/react'
// import theme from './theme'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ChakraProvider>
    <App />
    </ChakraProvider>
  </React.StrictMode>
)
