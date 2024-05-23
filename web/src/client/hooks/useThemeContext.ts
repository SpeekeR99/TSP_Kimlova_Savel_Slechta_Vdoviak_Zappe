import { useContext } from 'react'
import { ThemeContext } from '../context/themeContext'

export const useThemeContext = () => {
	const context = useContext(ThemeContext)

	if (!context)
		throw new Error('Context has to be used inside context provider!')

	return context
}
