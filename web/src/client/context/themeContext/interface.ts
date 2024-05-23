import { Theme } from '@mui/material'
import { ReactNode } from 'react'

export interface themeContextType {
	themeMode: Theme
	toggleTheme: () => void
}

export interface themeContextProviderProps {
	children: ReactNode
}
