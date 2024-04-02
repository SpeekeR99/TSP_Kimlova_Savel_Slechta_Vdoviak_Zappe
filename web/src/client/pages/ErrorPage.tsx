import React from 'react'
import BaseLayout from '../components/BaseLayout'
import Alert from '@mui/material/Alert'
import { AlertTitle, Button, Container, Stack, Typography } from '@mui/material'

const ErrorPage = () => (
	<BaseLayout>
		<Container maxWidth='sm' sx={{ justifyContent: 'center' }}>
			<Alert
				severity='error'
				sx={{
					borderRadius: '15px',
					marginTop: '30%',
					justifyContent: 'center',
				}}
			>
				<AlertTitle>Error uploading file</AlertTitle>
				<Stack direction='column' spacing={2}>
					<Typography variant='h6' style={{ color: 'black' }}>
						Error occured while uploading your file.
					</Typography>
					<Button variant='contained' sx={{ marginTop: 20 }} href='/'>
						Back Home
					</Button>
				</Stack>
			</Alert>
		</Container>
	</BaseLayout>
)

export default ErrorPage
