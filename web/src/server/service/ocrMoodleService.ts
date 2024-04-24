import { MulterFile } from 'multer'

export const validateFile = async (file: MulterFile) => {
	return await fetch('http://127.0.0.1:5000/test_evaluation', {
		method: 'POST',
		headers: {
			'Content-Type': file.mimetype,
			'Content-Length': file.size.toString(),
		},
		body: file.buffer,
	})
}
