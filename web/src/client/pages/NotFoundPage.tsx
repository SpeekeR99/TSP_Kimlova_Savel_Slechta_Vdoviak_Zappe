import React from 'react'
import BaseLayout from '../components/BaseLayout'
import {
	Alert,
	AlertTitle,
	Box,
	Button,
	Container,
	Typography,
} from '@mui/material'

const NotFoundPage = () => (
	<BaseLayout>
		<Container maxWidth='sm' sx={{ justifyContent: 'center' }}>
			<Alert
				severity='warning'
				sx={{
					borderRadius: '15px',
					marginTop: '15%',
					justifyContent: 'center',
				}}
			>
				<AlertTitle>Page not found</AlertTitle>
				<Box
					sx={{
						display: 'flex',
						justifyContent: 'center',
						alignItems: 'center',
						flexDirection: 'column',
					}}
				>
					<Typography variant='h1' style={{ color: 'black' }}>
						404
					</Typography>
					<Typography variant='h6' style={{ color: 'black' }}>
						The page you’re looking for doesn’t exist.
					</Typography>
					<Button variant='contained' style={{ marginTop: 20 }} href='/'>
						Back Home
					</Button>
				</Box>
			</Alert>
		</Container>
	</BaseLayout>
)
export default NotFoundPage
