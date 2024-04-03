import { Route } from './interface'
import ocrMoodleRoute from './routes/ocrMoodleRoute'
import generateRoute from './routes/generateRoute'

const routes: Route[] = [ocrMoodleRoute, generateRoute]

export default routes
