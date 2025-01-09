import React, { useState } from 'react'
import BaseLayout from '../components/BaseLayout'

import MyBreadcrump from '../components/MyBreadcrump'
import MyDropzone from '../components/MyDropZone'
import { useGenerateStatistics } from '../hooks/useGenerateStatistics'
import {
	Button,
	Container,
	Grid,
	Paper,
	Stack,
	Typography,
} from '@mui/material'
import { BarChart, PieChart } from '@mui/x-charts'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'

const StatisticsPage = () => {
	const [statistics, setStatistics] = useState(null)

	if (!statistics) {
		return (
			<BaseLayout>
				<MyBreadcrump parts={['statistics']} />
				<MyDropzone
					accept={{ 'text/csv': ['.csv'] }}
					maxFiles={1}
					useAction={() => useGenerateStatistics(setStatistics)}
					valid={true}
				/>
			</BaseLayout>
		)
	} else {
		const [graph1, graph2] = statistics

		return (
			<BaseLayout>
				<Stack
					direction='row'
					spacing={2}
					sx={{
						justifyContent: 'space-between',
						alignItems: 'center',
					}}
				>
					<MyBreadcrump parts={['statistics']} />

					<Button
						variant='contained'
						size='medium'
						onClick={() => setStatistics(null)}
					>
						<ArrowBackIcon />
					</Button>
				</Stack>

				<Container maxWidth='xl'>
					<Grid
						container
						spacing={5}
						sx={{
							justifyContent: 'center',
							alignItems: 'center',
							marginTop: '1%',
						}}
					>
						<Grid item md={6}>
							<Paper elevation={3}>
								<Typography variant='h6' align='center' gutterBottom>
									{graph1.name}
								</Typography>
								<BarChart
									grid={{ horizontal: true }}
									xAxis={[
										{
											scaleType: 'band',
											data: Object.keys(graph1.values),
											colorMap: {
												type: 'ordinal',
												colors: [
													'#ccebc5',
													'#a8ddb5',
													'#7bccc4',
													'#4eb3d3',
													'#2b8cbe',
													'#08589e',
												],
											},
										},
									]}
									series={[
										{
											data: Object.values(graph1.values).map(
												(val: number) => val
											),
										},
									]}
									borderRadius={7}
									height={300}
								/>
							</Paper>
						</Grid>

						<Grid item md={6}>
							<Paper elevation={3}>
								<Typography variant='h6' align='center' gutterBottom>
									{graph2.name}
								</Typography>
								<PieChart
									series={[
										{
											data: graph2.values,
											highlightScope: { fade: 'global', highlight: 'item' },
											faded: {
												innerRadius: 30,
												additionalRadius: -30,
												color: 'gray',
												outerRadius: 97,
												paddingAngle: 2,
												cornerRadius: 3,
											},
										},
									]}
									height={300}
								/>
							</Paper>
						</Grid>
					</Grid>
				</Container>
			</BaseLayout>
		)
	}
}
export default StatisticsPage
