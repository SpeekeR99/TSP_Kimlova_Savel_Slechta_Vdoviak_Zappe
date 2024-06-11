import { MulterFile } from 'multer'
import { parse } from 'json2csv'

export const validateFile = async (file: MulterFile) => {
	const PORT = 5000
	const port = process.env.AI_API_PORT || PORT
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

		if (!result) throw new Error('Content does not contain result field!')

		const formattedResult = result.reduce((acc, curr, i) => {
			acc[`answer${i + 1}`] = curr.answer.join(',')
			acc[`points${i + 1}`] = curr.points
			return acc
		}, {})
		return { ...fields, ...formattedResult }
	})

	if (flattenedcContent.length === 0) throw new Error('Empty results')

	return parse(flattenedcContent)
}
