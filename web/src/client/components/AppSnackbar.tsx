import React, { FC } from 'react'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { Alert, AlertColor, Snackbar } from '@mui/material'
import { setSnackbarClose } from '../context/snackbarContext/snackbarActions'
import { useSnackbarContext } from '../hooks/useSnackbarContext'

const AppSnackbar: FC = () => {
	const {
		state: { open, message, severity, autoHideDuration },
		dispatch,
	}: SnackbarContextType = useSnackbarContext()

	const handleClose = () => dispatch(setSnackbarClose())

	return (
		<Snackbar
			open={open}
			autoHideDuration={autoHideDuration}
			anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
			onClose={handleClose}
		>
			<Alert
				onClose={handleClose}
				variant='filled'
				severity={severity as AlertColor}
				sx={{ width: '100%' }}
			>
				{message}
			</Alert>
		</Snackbar>
	)
}

export default AppSnackbar
