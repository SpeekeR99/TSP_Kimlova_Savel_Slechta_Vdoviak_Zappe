import express, { Request, Response } from 'express'
import { Router } from 'express'
import catchError from '../middleware/catch-error'
import { Route } from '../interface'

const router: Router = express.Router()

router.post(
	'/',
	catchError(async (req: Request, res: Response) => {
		console.log(req.body)
		res.json({ status: 'ok' })
	})
)

const route: Route = { path: '/0/generate', router }

export default route
