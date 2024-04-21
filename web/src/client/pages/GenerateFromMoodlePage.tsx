import React, { useState, ChangeEvent, useEffect, FC } from 'react'
import BaseLayout from '../components/BaseLayout'
import { Box, Button, Container, Stack, TextField } from '@mui/material'
import { useBackDropContext } from '../hooks/useBackDropContext'
import { useGenerateFromMoodle } from '../hooks/useGenerateFromFromMoodle'
import MyBreadcrump from '../components/MyBreadcrump'

const Form: FC = () => {
	const [quizId, setQuizId] = useState<string>('')
	const { mutate, isLoading } = useGenerateFromMoodle()
	const { setOpenBackDrop } = useBackDropContext()

	const handleQuizIdChange = (e: ChangeEvent<HTMLInputElement>) => {
		setQuizId(e.target.value)
	}

	useEffect(() => {
		setOpenBackDrop(isLoading)
	}, [isLoading])

	return (
		<Box width='90%' padding='10px'>
			<TextField
				id='Quiz id'
				label='Quiz id'
				placeholder='Quiz id'
				fullWidth
				sx={{ minWidth: '100%' }}
				onChange={handleQuizIdChange}
			/>
			<Box
				display='flex'
				alignSelf='flex-end'
				marginTop='3%'
				sx={{ float: 'right' }}
			>
				<Button
					variant='contained'
					disabled={quizId === ''}
					onClick={() => mutate(quizId)}
				>
					Generate
				</Button>
			</Box>
		</Box>
	)
}

const GenerateFromMoodlePage: FC = () => {
	return (
		<BaseLayout>
			<MyBreadcrump parts={['generate', 'from-moodle']} />
			<Container sx={{ width: '60%' }}>
				<Stack
					textAlign='center'
					direction='column'
					alignItems='center'
					justifyContent='center'
					border='solid 1px'
					borderRadius='10px'
					marginTop='8%'
					padding='50px'
				>
					<Form />
				</Stack>
			</Container>
		</BaseLayout>
	)
}

export default GenerateFromMoodlePage
