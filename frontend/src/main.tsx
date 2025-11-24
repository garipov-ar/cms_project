import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import CatalogPage from './pages/CatalogPage'
import DocumentPage from './pages/DocumentPage'

import './styles.css'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<CatalogPage/>} />
        <Route path='/document/:id' element={<DocumentPage/>} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
