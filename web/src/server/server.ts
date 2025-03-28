/* eslint-disable @typescript-eslint/no-var-requires */

import express, { Express, NextFunction, Request, Response } from 'express'
import dotenv from 'dotenv'
import routes from './routes'
import { Route } from './interface'
import errorHandler from './middleware/error-handler'
import path from 'path'
const DIST_DIR = path.resolve(__dirname, '../../')
const PORT = 8080
const CODE_OK = 200

dotenv.config()
const port = process.env.PORT || PORT
export const app: Express = express()

app.use(express.json())

const loadRoutes = () => {
	app.use('/healthcheck', (req: Request, res: Response) =>
		res.sendStatus(CODE_OK)
	)
	routes.forEach(({ path, router }: Route) => app.use(path, router))
}

if (process.env.NODE_ENV === 'production') {
	app.use(express.static(DIST_DIR))

	loadRoutes()
	app.get('*', (req: Request, res: Response) => {
		res.sendFile(path.join(DIST_DIR, 'index.html'))
	})
} else if (process.env.NODE_ENV === 'development') {
	const config = require('../../webpack.config.dev')
	const compiler = require('webpack')(config)
	const wdMiddleware = require('webpack-dev-middleware')(compiler)

	app.use(require('webpack-hot-middleware')(compiler))
	app.use(wdMiddleware)

	loadRoutes()
	app.get('*', (req: Request, res: Response, next: NextFunction) => {
		const filename = path.join(compiler.outputPath, 'index.html')
		compiler.outputFileSystem.readFile(filename, (err, result) => {
			if (err) {
				return next(err)
			}
			res.set('content-type', 'text/html')
			res.send(result)
			res.end()
		})
	})
}

app.use(errorHandler)

let server

export function start() {
	server = app.listen(port, () => {
		console.log(`[server] listening on http://localhost:${port}`)
	})
	return server
}

export function close() {
	server?.close()
}

