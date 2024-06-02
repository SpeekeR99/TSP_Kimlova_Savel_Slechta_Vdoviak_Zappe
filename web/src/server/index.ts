import {start, close} from '../server/server'

start()

const teardown = async () => {
	console.log('\nServer is shutting down gracefully')

	close()
	process.exit(0) // should be on for dev only, but had some problems with it on prod
}

process.on('SIGINT', teardown)
process.on('SIGTERM', teardown)
