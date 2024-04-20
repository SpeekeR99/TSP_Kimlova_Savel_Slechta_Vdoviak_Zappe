import express, { Request, Response } from 'express'
import { Router } from 'express'
import catchError from '../middleware/catch-error'
import { Route } from '../interface'

const router: Router = express.Router()

router.post(
	'/from-moodle',
	catchError(async (req: Request, res: Response) => {
		console.log(req.body)
		res.json({ status: 'ok' })
	})
)

router.post(
	'/from-xml',
	catchError(async (req: Request, res: Response) => {
		console.log(req.body)
		res.json({ status: 'ok' })
	})
)

const route: Route = { path: '/0/generate', router }

export default route
