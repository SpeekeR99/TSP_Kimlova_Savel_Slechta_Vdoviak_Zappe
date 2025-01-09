import { BAR_CHART, PIE_CHART } from '../../client/shared/const'

const getQuestionAveragePoints = (data, numOfPoints) => {
	return Object.entries(data).reduce(
		(acc, [key, answers]: [key: string, answers: any[]]) => {
			const sum = answers.reduce((accumulator, { points }) => {
				return accumulator + parseInt(points)
			}, 0)
			acc[key] = sum / numOfPoints
			return acc
		},
		{}
	)
}
// const getQuestionAveragePoints = (data, numOfPoints) => {
// 	const values = [
// 		Object.entries(data).reduce(
// 			(acc, [key, answers]: [key: string, answers: any[]], index: number) => {
// 				const sum = answers.reduce((accumulator, { points }) => {
// 					return accumulator + parseInt(points)
// 				}, 0)
// 				acc[key] = sum / numOfPoints
// 				//  {
// 				// 	value: sum / numOfPoints,
// 				// 	label: `Question ${index + 1}`,
// 				// 	dataKey: key,
// 				// }
// 				return acc
// 			},
// 			{}
// 		),
// 	]

// 	const keys = Object.keys(values[0])
// 	const series = keys.map((key, index) => ({
// 		dataKey: key,
// 		label: `Question ${index + 1}`,
// 	}))

// 	return { values, series }
// }

const getStudentsDividedIntoGroups = (data) => {
	const points = data.map((student) => student.body_rel)
	const FIRST = 0.9
	const SECOND = 0.8
	const THIRD = 0.7
	const FOURTH = 0.6

	const groups = points.reduce(
		(acc, point) => {
			const value = parseFloat(point)

			if (value >= FIRST) {
				acc['first'].push(value)
			} else if (value >= SECOND) {
				acc['second'].push(value)
			} else if (value >= THIRD) {
				acc['third'].push(value)
			} else if (value >= FOURTH) {
				acc['fourth'].push(value)
			} else {
				acc['fifth'].push(value)
			}
			return acc
		},

		{ first: [], second: [], third: [], fourth: [], fifth: [] }
	)
	const labels = [
		'Výborně (0.9 - 1)',
		'Chvalitebně (0.8 - 0.89)',
		'Dobře (0.7 - 0.79)',
		'Dostatečně (0.6 - 0.69)',
		'Nedostatečně (pod 0.6)',
	]

	return Object.values(groups).map((group: any[], i) => ({
		id: i,
		value: group.length,
		label: labels[i],
	}))
}

const getQuestionsWithAnswers = ({ data, numOfQuestions }) => {
	const result = {}

	for (let i = 1; i <= numOfQuestions; i++) {
		result[`question${i}`] = []
	}

	data.forEach((studentData) => {
		const studentResults = studentData.result
		Object.keys(result).forEach((key, index) => {
			result[key].push(studentResults[index])
		})
	})

	return result
}

export const prepareDataForStatistics = (data) => {
	const numOfQuestions = data[0].result.length
	const numOfPoints = data[0].body_celkem

	const questionsWithAnswers = getQuestionsWithAnswers({ data, numOfQuestions })

	const questionAveragePoints = getQuestionAveragePoints(
		questionsWithAnswers,
		numOfPoints
	)

	const studentsDividedIntoGroups = getStudentsDividedIntoGroups(data)

	const result = [
		{
			name: 'Průměrný počet bodů za otázku',
			values: questionAveragePoints,
			graphType: BAR_CHART,
		},
		{
			name: 'Výsledky studentů',
			values: studentsDividedIntoGroups,
			graphType: PIE_CHART,
		},
	]

	return result
}
