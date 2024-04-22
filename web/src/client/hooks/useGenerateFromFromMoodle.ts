import { useMutation } from 'react-query'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'
import { useSnackbarContext } from '../hooks/useSnackbarContext'

const fetchData = async (quizId) => {
	if (!quizId) return
	try {
		const response = await fetch('/0/generate/from-moodle', {
			method: 'POST',
			body: JSON.stringify(quizId),
		})

		if (response.ok) {
			const data = await response.json()
			console.log('Response:', data)
		} else {
			throw new Error(`Upload failed: ${response.statusText}`)
		}
	} catch (error) {
		throw new Error(`Error: ${error}`)
	}
}

export const useGenerateFromMoodle = () => {
	const { dispatch }: SnackbarContextType = useSnackbarContext()

	const openSnackbar = (message: string, severity: string = 'success') =>
		dispatch(setSnackbarOpen(message, severity))

	return useMutation(fetchData, {
		onSuccess: () => {
			openSnackbar('Files generated succeesfully!')
		},
		onError: () => {
			openSnackbar('Error while generating files!', 'error')
		},
	})
}
