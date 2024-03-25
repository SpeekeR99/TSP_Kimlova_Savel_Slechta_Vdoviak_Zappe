export const uploadFile = async (file: File) => {
	if (!file) return

	const formData = new FormData()
	formData.append('file', file)

	// try {
	// 	const response = await fetch('/upload', {
	// 		method: 'POST',
	// 		body: formData,
	// 	})

	// 	if (response.ok) {
	// 		const data = await response.json()
	// 		console.log('Response:', data)
	// 	} else {
	// 		console.error('Upload failed:', response.statusText)
	// 	}
	// } catch (error) {
	// 	console.error('Error:', error)
	// }
}
