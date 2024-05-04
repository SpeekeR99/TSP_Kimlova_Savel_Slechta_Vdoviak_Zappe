import { useMutation } from 'react-query'
import { useSnackbarContext } from '../hooks/useSnackbarContext'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'

const fetchData = async (files: File[]) => {
	if (!files) throw new Error('Files are not selected!')
	if (files.length !== 1) throw new Error('Upload needs 1 file!')

	const formData = new FormData()
	formData.append('file', files[0])

	try {
		const response = await fetch('/0/process/arks', {
			method: 'POST',
			body: formData,
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

export const useUploadArks = () => {
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
