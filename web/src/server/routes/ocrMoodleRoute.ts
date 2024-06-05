import express, { Request, Response } from 'express'
import multer from 'multer'
import { Router } from 'express'
import catchError from '../middleware/catch-error'
import { Route } from '../interface'
import { MulterFile } from 'multer'
import { transformToCSV, validateFile } from '../service/ocrMoodleService'

const router: Router = express.Router()
const upload = multer({ storage: multer.memoryStorage() })

router.post(
	'/arks',
	upload.single('file'),
	catchError(async (req: Request & { file: MulterFile }, res: Response) => {
		const { file } = req
		if (!file) throw new Error('PDF file not present!')

		const response = await validateFile(file)
		if (!response.ok) throw new Error('Failed to validate data')

		const result = await response.json()
		const csvResult = transformToCSV(result.result)
		const logText = result.log

		console.log(logText)
		/* TODO: Save logText to a file and send .zip file with csvResult and logText */

		res.send(csvResult)
	})
)

const route: Route = { path: '/0/process', router }

export default route
