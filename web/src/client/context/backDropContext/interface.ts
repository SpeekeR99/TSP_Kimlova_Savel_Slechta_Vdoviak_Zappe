import { Dispatch, ReactNode } from 'react'

export interface BackDropContextProviderProps {
	children: ReactNode
}

export interface BackDroprContextType {
	openBackDrop: boolean
	setOpenBackDrop: Dispatch<React.SetStateAction<boolean>>
}
