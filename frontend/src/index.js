import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { ChakraProvider } from '@chakra-ui/react'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // strict mode
  <React.StrictMode>
    {/* <ChakraProvider> */}
    <App />
    {/* </ChakraProvider> */}
    </React.StrictMode>
);


