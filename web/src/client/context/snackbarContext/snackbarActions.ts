import { SET_CLOSE, SET_OPEN } from './const'
import { SnackbarPayload } from './interface'

export const setSnackbarOpen = (
	message: string,
	severity: string = 'success',
	autoHideDuration: number = 4000
): { type: string; payload: SnackbarPayload } => {
	return { type: SET_OPEN, payload: { message, severity, autoHideDuration } }
}

export const setSnackbarClose = (): { type: string } => {
	return { type: SET_CLOSE }
}
