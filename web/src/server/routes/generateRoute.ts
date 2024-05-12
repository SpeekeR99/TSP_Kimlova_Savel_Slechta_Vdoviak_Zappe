import express, { Request, Response } from 'express'
import { Router } from 'express'
import multer, { MulterFile } from 'multer'
import catchError from '../middleware/catch-error'
import { Quiz, Route } from '../interface'
import path from 'path'
import {
	generateArks,
	parseQuizXMLFile,
	parseStudentCSVFile,
} from '../service/generateService'

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
		if (!files) throw new Error('Files are not present!')

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

		const response = await generateArks(quiz)

		if (!response.ok) throw new Error('Failed to fetch file content')

		const arrayBuffer = await response.arrayBuffer()
		const buffer = Buffer.from(arrayBuffer)

		res.send(buffer)
	})
)

const route: Route = { path: '/0/generate', router }

export default route
