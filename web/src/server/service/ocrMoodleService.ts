import { MulterFile } from 'multer'

export const validateFile = async (file: MulterFile) => {
	const port = process.env.AI_API_PORT || 5000
	const host = process.env.AI_API_HOST || '127.0.0.1'
	return await fetch(`http://${host}:${port}/test_evaluation`, {
		method: 'POST',
		headers: {
			'Content-Type': file.mimetype,
			'Content-Length': file.size.toString(),
		},
		body: file.buffer,
	})
}
