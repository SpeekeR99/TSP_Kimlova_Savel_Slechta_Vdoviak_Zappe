import { useMutation } from 'react-query'
import { useSnackbarContext } from '../hooks/useSnackbarContext'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'

const fetchData = async (file: File) => {
	if (!file) return
	await new Promise((resolve) => setTimeout(resolve, 2000))
	const formData = new FormData()
	formData.append('file', file)

	try {
		const response = await fetch('/0/process/', {
			method: 'POST',
			body: formData,
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

export const useUploadActions = () => {
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
