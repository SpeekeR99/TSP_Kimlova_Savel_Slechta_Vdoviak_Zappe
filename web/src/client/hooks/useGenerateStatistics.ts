import { useMutation } from 'react-query'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'
import { useSnackbarContext } from '../hooks/useSnackbarContext'

const fetchData = async (files: File[]) => {
	if (!files) throw new Error('Files not selected')
	if (files.length !== 1) throw new Error('Generation needs 1 file!')

	const formData = new FormData()

	formData.append('file', files[0])

	try {
		const response = await fetch('/0/generate/statistics', {
			method: 'POST',
			body: formData,
		})

		if (response.ok) {
			return await response.json()
		} else {
			throw new Error(`Upload failed: ${response.statusText}`)
		}
	} catch (error) {
		throw new Error(`Error: ${error}`)
	}
}

export const useGenerateStatistics = (setStatistics) => {
	const { dispatch }: SnackbarContextType = useSnackbarContext()

	const openSnackbar = (message: string, severity: string = 'success') =>
		dispatch(setSnackbarOpen(message, severity))

	return useMutation((files: File[]) => fetchData(files), {
		onSuccess: (data) => {
			const TIMEOUT = 100
			setTimeout(() => setStatistics(data), TIMEOUT)
			openSnackbar('Statistics generated succeesfully!')
		},
		onError: (e) => {
			console.error(e)
			openSnackbar('Error while generating statistics!', 'error')
		},
	})
}
