import { MulterFile } from 'multer'
import { parse } from 'json2csv'

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

export const transformToCSV = (content: any[]) => {
	const flattenedcContent = content.map((res) => {
		const { result, ...fields } = res
		const formattedResult = result.reduce((acc, curr, i) => {
			acc[`answer${i + 1}`] = curr.answer.join(',')
			acc[`points${i + 1}`] = curr.points
			return acc
		}, {})
		return { ...fields, ...formattedResult }
	})

	return parse(flattenedcContent)
}
