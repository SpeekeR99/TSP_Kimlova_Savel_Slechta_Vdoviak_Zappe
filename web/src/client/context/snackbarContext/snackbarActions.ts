import { SET_CLOSE, SET_OPEN } from './const'
import { SnackbarPayload } from './interface'
const HIDE_DURATION_TIME = 4000

export const setSnackbarOpen = (
	message: string,
	severity: string = 'success',
	autoHideDuration: number = HIDE_DURATION_TIME
): { type: string; payload: SnackbarPayload } => {
	return { type: SET_OPEN, payload: { message, severity, autoHideDuration } }
}

export const setSnackbarClose = (): { type: string } => {
	return { type: SET_CLOSE }
}
