import { Dispatch, ReactNode } from 'react'

export interface SnackbarPayload {
	message: string
	severity?: string
	autoHideDuration?: number
}

export interface SnackbarState {
	open: boolean
	severity: string
	message: string
	autoHideDuration: number
}

export interface SnackbarContextProviderProps {
	children: ReactNode
}

export interface SnackbarAction {
	type: string
	payload?: SnackbarPayload
}

export interface SnackbarContextType {
	state: SnackbarState
	dispatch: Dispatch<SnackbarAction>
}
