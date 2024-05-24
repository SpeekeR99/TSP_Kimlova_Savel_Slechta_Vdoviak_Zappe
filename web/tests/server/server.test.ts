import request from 'supertest'
import server from '../../src/server/server'

const STATUS_OK = 200

afterAll(async () => {
	await server.close() // Close the server after all tests are done
})

describe('Server tests', () => {
	it('/healthcheck route test', async () => {
		const res = await request(server).get('/healthcheck')
		expect(res.status).toBe(STATUS_OK)
	})

	// it('Test non-existing route', async () => {
	// 	const res = await request(server).get('/unknown-route')
	// 	expect(res.status).toBe(STATUS_OK)
	// 	expect(res.headers['content-type']).toContain('text/html')
	// })
})
