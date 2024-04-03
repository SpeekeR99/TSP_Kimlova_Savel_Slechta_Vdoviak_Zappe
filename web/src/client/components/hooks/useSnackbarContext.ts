import { useContext } from 'react'
import { SnackbarContext } from '../../context/snackbarContext'

export const useSnackbarContext = () => {
	const context = useContext(SnackbarContext)

	if (!context)
		throw new Error('Context has to be used inside context provider!')

	return context
}
