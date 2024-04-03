import React, { createContext, useReducer, useContext } from 'react'
import { SET_CLOSE, SET_OPEN } from './const'
import {
	SnackbarAction,
	SnackbarContextProviderProps,
	SnackbarContextType,
	SnackbarState,
} from './interface'

export const SnackbarContext = createContext<SnackbarContextType>({
	state: {
		open: false,
		severity: 'success',
		message: '',
		autoHideDuration: 4000,
	},
	dispatch: () => null,
})

const snackbarReducer = (state: SnackbarState, action: SnackbarAction) => {
	switch (action.type) {
		case SET_OPEN:
			return {
				...state,
				...action.payload,
				open: true,
			}
		case SET_CLOSE:
			return {
				...state,
				open: false,
			}
		default:
			return state
	}
}

export const SnackbarContextProvider = ({
	children,
}: SnackbarContextProviderProps) => {
	const [state, dispatch] = useReducer(snackbarReducer, {
		open: false,
		severity: 'success',
		message: '',
		autoHideDuration: 4000,
	})

	return (
		<SnackbarContext.Provider value={{ state, dispatch }}>
			{children}
		</SnackbarContext.Provider>
	)
}
