import { useMutation } from 'react-query'
import { useSnackbarContext } from '../hooks/useSnackbarContext'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'

const fetchData = async (file: File) => {
	if (!file) return
	const formData = new FormData()
	formData.append('file', file)

	try {
		const response = await fetch('/0/process/arks', {
			method: 'POST',
			body: formData,
		})

		if (response.ok) {
			const data = await response.json()
			const jsonData = JSON.stringify(data)

			const blob = new Blob([jsonData], { type: 'application/json' })
			const url = URL.createObjectURL(blob)

			const link = document.createElement('a')
			link.href = url
			link.download = 'result.json'
			document.body.appendChild(link)
			link.click()
			document.body.removeChild(link)
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
