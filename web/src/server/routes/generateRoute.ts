import express, { Request, Response } from 'express'
import { Router } from 'express'
import multer, { MulterFile } from 'multer'
import catchError from '../middleware/catch-error'
import { Route } from '../interface'
import { parseXMLFile } from '../service/generateService'

const router: Router = express.Router()
const upload = multer({ storage: multer.memoryStorage() })

router.post(
	'/from-moodle',
	catchError(async (req: Request, res: Response) => {
		console.log(req.body)
		res.json({ status: 'ok' })
	})
)

router.post(
	'/from-xml',
	upload.single('file'),
	catchError(async (req: Request & { file: MulterFile }, res: Response) => {
		const { file } = req
		if (!file) throw new Error('XML file not present!')

		const parsedXML = await parseXMLFile(file)
		console.log(parsedXML)
		res.json({ status: 'ok' })
	})
)

const route: Route = { path: '/0/generate', router }

export default route
