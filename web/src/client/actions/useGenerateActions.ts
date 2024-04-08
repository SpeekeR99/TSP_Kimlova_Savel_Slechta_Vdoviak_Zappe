import { useMutation } from 'react-query'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'
import { useSnackbarContext } from '../hooks/useSnackbarContext'

const fetchData = async (quizId) => {
	if (!quizId) return
	await new Promise((resolve) => setTimeout(resolve, 2000))
	try {
		const response = await fetch('/0/generate/', {
			method: 'POST',
			body: JSON.stringify(quizId),
		})

		if (response.ok) {
			const data = await response.json()
			console.log('Response:', data)
		} else {
			console.error('Upload failed:', response.statusText)
		}
	} catch (error) {
		console.error('Error:', error)
	}
}

export const useGenerateActions = () => {
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
