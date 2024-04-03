import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import { BrowserRouter } from 'react-router-dom'
import { SnackbarContextProvider } from './context/snackbarContext'

createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<BrowserRouter>
			<SnackbarContextProvider>
				<App />
			</SnackbarContextProvider>
		</BrowserRouter>
	</React.StrictMode>
)
