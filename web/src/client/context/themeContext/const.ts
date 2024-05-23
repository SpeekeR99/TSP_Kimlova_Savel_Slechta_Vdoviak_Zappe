import { createTheme } from '@mui/material'

export const LIGHT_MODE = createTheme({
	palette: {
		mode: 'light',
	},
})

export const DARK_MODE = createTheme({
	palette: {
		mode: 'dark',
	},
})

export const THEME_MODE = 'theme_mode'
