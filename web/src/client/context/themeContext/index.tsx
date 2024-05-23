import React, { createContext, useState } from 'react'
import { themeContextProviderProps, themeContextType } from './interface'
import { Theme } from '@mui/material'
import { DARK_MODE, LIGHT_MODE, THEME_MODE } from './const'
import { ThemeProvider } from '@mui/material/styles'

export const ThemeContext = createContext<themeContextType>({
	themeMode: LIGHT_MODE,
	toggleTheme: () => null,
})

export const ThemeContextProvider = ({
	children,
}: themeContextProviderProps) => {
	const [themeMode, setThemeMode] = useState<Theme>(() => {
		const storedThemeMode = localStorage.getItem(THEME_MODE)
		return storedThemeMode && storedThemeMode === 'dark'
			? DARK_MODE
			: LIGHT_MODE
	})

	const toggleTheme = () => {
		const newTheme = themeMode === LIGHT_MODE ? DARK_MODE : LIGHT_MODE
		localStorage.setItem(THEME_MODE, newTheme.palette.mode)
		setThemeMode(newTheme)
	}

	return (
		<ThemeContext.Provider value={{ themeMode, toggleTheme }}>
			<ThemeProvider theme={themeMode}>{children}</ThemeProvider>
		</ThemeContext.Provider>
	)
}
