import express, { Express, Request, Response } from 'express'
import dotenv from 'dotenv'
import routes from './routes'
import { Route } from './interface'
import webpack from 'webpack'
import webpackConfig from '../../webpack.config.dev'
import webpackDevMiddleware from 'webpack-dev-middleware'
import errorHandler from './middleware/error-handler'
import path from 'path'
const DIST_DIR = path.resolve(__dirname, '../../')

dotenv.config()
const port = process.env.PORT || 8080
const app: Express = express()

app.use(express.json())

if (process.env.NODE_ENV === 'production') {
	app.use(express.static(DIST_DIR))
} else {
	const compiler = webpack(webpackConfig)
	const wdMiddleware = webpackDevMiddleware(compiler)

	app.use(require('webpack-hot-middleware')(compiler))
	app.use(wdMiddleware)
}

// Routes
app.use('/healthcheck', (req: Request, res: Response) => res.sendStatus(200))
routes.forEach(({ path, router }: Route) => app.use(path, router))
app.use(errorHandler)

app.listen(port, () => {
	console.log(`[server] listening on http://localhost:${port}`)
})
