import { useMutation } from 'react-query'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'
import { useSnackbarContext } from '../hooks/useSnackbarContext'
import { Dayjs } from 'dayjs'

const fetchData = async (
	files: File[],
	date: string,
	formId: string,
	scriptURL: string
) => {
	if (!files) throw new Error('Files not selected')
	if (!formId) throw new Error('Form ID is not specified')
	if (files.length !== 1) throw new Error('Generation needs 1 file!')
	if (!date) throw new Error('Date not present!')

	const formData = new FormData()
	formData.append('file', files[0])
	formData.append('formId', formId)
	formData.append('date', date)
	formData.append('scriptURL', scriptURL)

	try {
		const response = await fetch('/0/generate/from-gcroom', {
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

export const useGenerateFromGCroom = (
	date: Dayjs,
	{ formId, scriptURL }: { formId: string; scriptURL: string }
) => {
	const { dispatch }: SnackbarContextType = useSnackbarContext()

	const openSnackbar = (message: string, severity: string = 'success') =>
		dispatch(setSnackbarOpen(message, severity))

	return useMutation(
		(files: File[]) => fetchData(files, date.toISOString(), formId, scriptURL),
		{
			onSuccess: () => {
				openSnackbar('Files generated succeesfully!')
			},
			onError: (e) => {
				console.error(e)
				openSnackbar('Error while generating files!', 'error')
			},
		}
	)
}
