import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import { BrowserRouter } from 'react-router-dom'
import { SnackbarContextProvider } from './context/snackbarContext'
import { QueryClient, QueryClientProvider } from 'react-query'
import { BackDropContextProvider } from './context/backDropContext'
import CssBaseline from '@mui/material/CssBaseline'
import { ThemeContextProvider } from './context/themeContext'

createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<BrowserRouter>
			<QueryClientProvider client={new QueryClient()}>
				<SnackbarContextProvider>
					<BackDropContextProvider>
						<ThemeContextProvider>
							<CssBaseline />
							<App />
						</ThemeContextProvider>
					</BackDropContextProvider>
				</SnackbarContextProvider>
			</QueryClientProvider>
		</BrowserRouter>
	</React.StrictMode>
)
