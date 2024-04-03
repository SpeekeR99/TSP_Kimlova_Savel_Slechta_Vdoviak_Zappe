import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import { BrowserRouter } from 'react-router-dom'
import { SnackbarContextProvider } from './context/snackbarContext'
import { QueryClient, QueryClientProvider } from 'react-query'
import { BackDropContextProvider } from './context/backDropContext'

createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<BrowserRouter>
			<QueryClientProvider client={new QueryClient()}>
				<SnackbarContextProvider>
					<BackDropContextProvider>
						<App />
					</BackDropContextProvider>
				</SnackbarContextProvider>
			</QueryClientProvider>
		</BrowserRouter>
	</React.StrictMode>
)
