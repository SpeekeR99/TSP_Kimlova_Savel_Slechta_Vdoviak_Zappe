import express, { Request, Response } from 'express'
import { Router } from 'express'
import multer, { MulterFile } from 'multer'
import catchError from '../middleware/catch-error'
import { Quiz, Route } from '../interface'
import path from 'path'
import {
	fetchGoogleFormQuizData,
	generateArks,
	generateArksFromGForms,
	parseQuizXMLFile,
	parseResultCSVFile,
	parseStudentCSVFile,
	processResultData,
} from '../service/generateService'
import { prepareDataForStatistics } from '../service/graphService'

const router: Router = express.Router()
const upload = multer({ storage: multer.memoryStorage() })

router.post(
	'/from-moodle',
	catchError(async (req: Request, res: Response) => {
		res.json({ status: 'ok' })
	})
)

router.post(
	'/from-xml',
	upload.array('files'),
	catchError(async (req: Request & { files: MulterFile[] }, res: Response) => {
		const { files } = req
		const { date } = req.body
		if (!files) throw new Error('Files are not present!')
		if (!date) throw new Error('Date not present!')

		const quiz: Quiz = await files.reduce(
			async (accPromise, file: MulterFile): Promise<Quiz> => {
				const acc = await accPromise
				const ext = path.extname(file.originalname)

				if (ext === '.xml') acc.questions = await parseQuizXMLFile(file)
				else if (ext === '.csv') acc.students = await parseStudentCSVFile(file)
				else throw new Error('Unsupported file type')
				return acc
			},
			Promise.resolve({})
		)

		quiz.date = date
		const response = await generateArks(quiz)

		if (!response.ok) throw new Error('Failed to fetch file content')

		const arrayBuffer = await response.arrayBuffer()
		const buffer = Buffer.from(arrayBuffer)

		res.send(buffer)
	})
)

router.post(
	'/from-gcroom',
	upload.single('file'),
	catchError(async (req: Request & { file: MulterFile }, res: Response) => {
		const { file } = req
		const { date, formId, scriptURL } = req.body

		if (!file) throw new Error('Student file is not present!')
		if (!date) throw new Error('Date not present!')
		if (!formId) throw new Error('Form Id is not present!')
		if (!scriptURL) throw new Error('Script URL is not present!')

		const quiz: Quiz = { students: null, questions: null, date: '' }
		quiz.students = await parseStudentCSVFile(file)
		quiz.questions = JSON.parse(
			await fetchGoogleFormQuizData(formId, scriptURL)
		)
		quiz.date = date

		const response = await generateArksFromGForms(quiz)

		if (!response.ok) throw new Error('Failed to fetch file content')

		const arrayBuffer = await response.arrayBuffer()
		const buffer = Buffer.from(arrayBuffer)

		res.send(buffer)
	})
)

router.post(
	'/statistics',
	upload.single('file'),
	catchError(async (req: Request & { file: MulterFile }, res: Response) => {
		const { file } = req

		if (!file) throw new Error('Student file is not present!')

		const data = await parseResultCSVFile(file)
		const result = await processResultData(data)
		const resultData = await prepareDataForStatistics(result)

		if (!result || !resultData) throw new Error('Error processing file!')

		res.json(resultData)
	})
)

const route: Route = { path: '/0/generate', router }

export default route
