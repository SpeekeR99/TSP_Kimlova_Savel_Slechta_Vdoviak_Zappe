import xml2js from 'xml2js'
import { MulterFile } from 'multer'

interface ParsedQuestions {
	type: string | null
	id: string
	text: string
	answers: any[]
	defaultGrade: number
	penalty: number
}

const getValueFromHTMLString = (htmlString: string): string => {
	const startIndex = htmlString.indexOf('>') + 1
	const endIndex = htmlString.lastIndexOf('<')

	return htmlString
		.substring(startIndex, endIndex === -1 ? htmlString.length : endIndex)
		.trim()
}

const getAnswers = (answers: any[]): object[] => {
	return answers.map((answer) => {
		const text = getValueFromHTMLString(answer.text[0])
		const { fraction } = answer['$']
		return { text, fraction }
	})
}

export const parseXMLFile = (file: MulterFile): Promise<ParsedQuestions[]> => {
	return new Promise((resolve, reject) => {
		const xmlData = file.buffer.toString()

		xml2js.parseString(xmlData, (err, parsedString) => {
			if (err) reject(new Error(`Error parsing XML:' ${err}`))

			const { quiz } = parsedString
			if (!quiz) reject(new Error('XML file does not contain quiz!'))

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
					const text = getValueFromHTMLString(questiontext[0].text[0])

					const answers = getAnswers(question.answer)

					const [defaultGrade] = question.defaultgrade
					const [penalty] = question.penalty

					return { type, id, text, answers, defaultGrade, penalty }
				})
				.filter(Boolean)

			resolve(result)
		})
	})
}

export const generateArks = async (parsedXML: ParsedQuestions[]) => {
	const port = process.env.AI_API_PORT || 5000
	const host = process.env.AI_API_HOST || '127.0.0.1'
	return await fetch(`http://${host}:${port}/get_print_data`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ data: parsedXML }),
	})
}
