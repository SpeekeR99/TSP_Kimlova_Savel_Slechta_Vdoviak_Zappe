import express, { Request, Response } from 'express'
import multer from 'multer'
import { Router } from 'express'
import catchError from '../middleware/catch-error'
import { Route } from '../interface'
import { MulterFile } from 'multer'
import { transformToCSV, validateFile } from '../service/ocrMoodleService'
import JSZip from 'jszip'

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
		if (!result) throw new Error('Result is not present!')

		const { result: studentResults, log } = result
		const csvResult = transformToCSV(studentResults)

		const zip = new JSZip()
		zip.file('result.csv', csvResult)
		zip.file('log.txt', log)

		const zipArchive = await zip.generateAsync({ type: 'nodebuffer' })
		res.send(zipArchive)
	})
)

const route: Route = { path: '/0/process', router }

export default route
