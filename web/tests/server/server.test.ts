import {start, close} from '../../src/server/server'


beforeEach(() => {
	start()
})

afterEach(() => {
	close()
})

describe('Server tests', () => {
	

	// it('Test non-existing route', async () => {
	// 	const res = await request(server).get('/unknown-route')
	// 	expect(res.status).toBe(STATUS_OK)
	// 	expect(res.headers['content-type']).toContain('text/html')
	// })
})
