import React, { FC } from 'react'
import { Backdrop, CircularProgress } from '@mui/material'
import { useBackDropContext } from '../hooks/useBackDropContext'
import { BackDroprContextType } from '../context/backDropContext/interface'

const AppBackDrop: FC = () => {
	const { openBackDrop }: BackDroprContextType = useBackDropContext()

	return (
		<Backdrop
			sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
			open={openBackDrop}
		>
			<CircularProgress color='inherit' />
		</Backdrop>
	)
}

export default AppBackDrop
