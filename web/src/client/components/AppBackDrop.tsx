import React from 'react'
import { Backdrop, CircularProgress } from '@mui/material'

interface AppBackDropProps {
	isLoading: boolean
}

const AppBackDrop = ({ isLoading }: AppBackDropProps) => (
	<Backdrop
		sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
		open={isLoading}
	>
		<CircularProgress color='inherit' />
	</Backdrop>
)

export default AppBackDrop
