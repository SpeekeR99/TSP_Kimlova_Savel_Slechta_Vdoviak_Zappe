/* eslint-disable max-len */
import { transformToCSV } from '../../../src/server/service/ocrMoodleService'

describe('OCRMoodle service', () => {
	it('should transform content to CSV format correctly', () => {
		// Input data
		const content = [
			{
				body: 0,
				body_celkem: 3,
				body_rel: 0,
				email: 'xxxx@students.zcu.cz',
				jmeno: 'Daniel',
				login: 'xxxx',
				os_cislo: 'AxxNzzzzP',
				prijmeni: 'XXX',
				result: [
					{
						answer: [],
						points: 0,
					},
					{
						answer: [],
						points: 0,
					},
				],
			},
			{
				body: 0,
				body_celkem: 3,
				body_rel: 0,
				email: 'xxx8@students.zcu.cz',
				jmeno: 'Matěj',
				login: 'xxxx',
				os_cislo: 'AxxNzzzzP',
				prijmeni: 'XXX',
				result: [
					{
						answer: [],
						points: 0,
					},
					{
						answer: [],
						points: 0,
					},
				],
			},
		]

		// Expected output
		const expectedCSV = `"body","body_celkem","body_rel","email","jmeno","login","os_cislo","prijmeni","answer1","points1","answer2","points2"
0,3,0,"xxxx@students.zcu.cz","Daniel","xxxx","AxxNzzzzP","XXX","",0,"",0
0,3,0,"xxx8@students.zcu.cz","Matěj","xxxx","AxxNzzzzP","XXX","",0,"",0`

		const csvResult = transformToCSV(content)

		expect(csvResult).toEqual(expectedCSV)
	})

	it('should handle invalid content gracefully', () => {
		const content = []

		const wrapperFunction = () => {
			transformToCSV(content)
		}

		expect(wrapperFunction).toThrow('Empty results')
	})

	it('should handle invalid CSV content gracefully', () => {
		const content = [
			{
				invalidField: 'invalidValue',
			},
		]

		const wrapperFunction = () => {
			transformToCSV(content)
		}

		expect(wrapperFunction).toThrow('Content does not contain result field!')
	})
})
