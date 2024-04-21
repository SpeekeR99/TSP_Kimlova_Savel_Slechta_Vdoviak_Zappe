import express, { Request, Response } from 'express'
import multer from 'multer'
import { Router } from 'express'
import catchError from '../middleware/catch-error'
import { Route } from '../interface'

const router: Router = express.Router()
const upload = multer({ storage: multer.memoryStorage() })

router.post(
	'/arks',
	upload.single('file'),
	catchError(async (req: Request & { file: File }, res: Response) => {
		console.log(req.file)

		res.json({ status: 'ok' })
	})
)

const route: Route = { path: '/0/process', router }

export default route
