import xml2js from 'xml2js'
import { MulterFile } from 'multer'
import { Question, Quiz, Student } from '../interface'
import csv from 'csv-parser'
import { Readable } from 'stream'
import iconv from 'iconv-lite'

const getValueFromHTMLString = (htmlString: string): string => {
	return htmlString
}

const getAnswers = (answers: any[]): object[] => {
	return answers.map((answer) => {
		const text = checkForImage(getValueFromHTMLString(answer.text[0]), answer)
		const { fraction } = answer['$']
		return { text, fraction }
	})
}

export const parseQuizXMLFile = (file: MulterFile): Promise<Question[]> => {
	return new Promise((resolve, reject) => {
		const xmlData = file.buffer.toString()

		xml2js.parseString(xmlData, (err, parsedString) => {
			if (err) reject(new Error(`Error parsing XML: ${err}`))
			const { quiz } = parsedString
			if (!quiz && quiz !== '')
				reject(new Error('XML file does not contain quiz!'))

			const { question: questions } = quiz
			if (!questions) reject(new Error('XML file does not contain questions!'))

			const allowedQuestionTypes: string[] = ['multichoice', 'truefalse']

			const result = questions
				.map((question) => {
					const { type } = question['$']
					if (!allowedQuestionTypes.includes(type)) return null

					const { idnumber } = question
					const [id] = idnumber

					const { questiontext } = question
					const text = getQuestionText(questiontext[0])
					const name = question.name[0].text

					const answers = getAnswers(question.answer)

					const [defaultGrade] = question.defaultgrade
					const [penalty] = question.penalty

					return { type, id, text, answers, defaultGrade, penalty, name }
				})
				.filter(Boolean)

			resolve(result)
		})
	})
}

const getQuestionText = (questiontextNode) => {
	return checkForImage(getValueFromHTMLString(questiontextNode.text[0]), questiontextNode)
}

const checkForImage = (text, inputObject) => {
	if (text.includes('<img') && inputObject.file) {
		const regex = /<img([^>]*)src="([^"]*)"([^>]*)>/

		const content = inputObject.file[0]._
		const name = inputObject.file[0]['$']
		const file = getValueFromHTMLString(content)
		let extension = name.name.split('.').pop()
		if (extension === 'svg')
			extension = 'svg+xml'

		/* replace <img src="anything" with <img src="data:image/extension;base64,file" */
		/* Retain the alt attribute and everything else */
		const dataURL = `data:image/${extension};base64,${file}`
		return text.replace(regex, `<img$1src="${dataURL}"$3>`)
	}
	return text
}

export const generateArks = async (quiz: Quiz): Promise<Response> => {
	const PORT = 5000
	const port = process.env.AI_API_PORT || PORT
	const host = process.env.AI_API_HOST || '127.0.0.1'
	return await fetch(`http://${host}:${port}/get_print_data`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(quiz),
	})
}

export const parseStudentCSVFile = async (
	file: MulterFile
): Promise<Student[]> => {
	const csvData = iconv.decode(file.buffer, 'windows-1250')

	const results = []
	return new Promise((resolve, reject) => {
		const stream = Readable.from([csvData])

		stream
			.pipe(csv({ separator: ';' }))
			.on('data', (data) => {
				results.push(data)
			})

			.on('end', () => {
				resolve(results)
			})
			.on('error', (error) => {
				reject(error)
			})
	})
}
