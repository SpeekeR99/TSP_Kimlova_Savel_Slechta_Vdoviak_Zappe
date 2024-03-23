import express, { Express, Request, Response } from 'express'
import dotenv from 'dotenv'
import routes from './routes'
import { Route } from './interface'
import webpack from 'webpack'
import webpackConfig from '../../webpack.config.dev'
import webpackDevMiddleware from 'webpack-dev-middleware'

dotenv.config()
const port = process.env.PORT || 8080
const app: Express = express()

app.use(express.json())

if (process.env.NODE_ENV === 'production') {
	// nothing yet
} else {
	const compiler = webpack(webpackConfig)
	const wdMiddleware = webpackDevMiddleware(compiler)

	app.use(require('webpack-hot-middleware')(compiler))
	app.use(wdMiddleware)
}

// Routes
app.use('/healthcheck', (req: Request, res: Response) => res.sendStatus(200))
routes.forEach(({ path, router }: Route) => app.use(path, router))

app.listen(port, () => {
	console.log(`[server] listening on http://localhost:${port}`)
})
