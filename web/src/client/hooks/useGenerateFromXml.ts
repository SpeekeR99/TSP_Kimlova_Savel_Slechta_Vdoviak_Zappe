import { useMutation } from 'react-query'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'
import { useSnackbarContext } from '../hooks/useSnackbarContext'

const fetchData = async (files: File[], date: string) => {
	if (!files) throw new Error('Files not selected')
	if (files.length !== 2) throw new Error('Generation needs 2 files!')
	if (!date) throw new Error('Date not present!')

	const formData = new FormData()

	files.forEach((file) => {
		formData.append('files', file)
	})

	formData.append('date', date)

	try {
		const response = await fetch('/0/generate/from-xml', {
			method: 'POST',
			body: formData,
		})

		if (response.ok) {
			const blobData: Blob = await response.blob()

			const link = document.createElement('a')
			link.href = URL.createObjectURL(blobData)
			link.download = 'result.zip'
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

export const useGenerateFromXML = (date: string) => {
	const { dispatch }: SnackbarContextType = useSnackbarContext()

	const openSnackbar = (message: string, severity: string = 'success') =>
		dispatch(setSnackbarOpen(message, severity))

	return useMutation((files: File[]) => fetchData(files, date), {
		onSuccess: () => {
			openSnackbar('Files generated succeesfully!')
		},
		onError: (e) => {
			console.error(e)
			openSnackbar('Error while generating files!', 'error')
		},
	})
}
