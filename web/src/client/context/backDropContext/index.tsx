import React, { createContext, useState } from 'react'
import { BackDropContextProviderProps, BackDroprContextType } from './interface'

export const backDropContext = createContext<BackDroprContextType>({
	openBackDrop: false,
	setOpenBackDrop: () => null,
})

export const BackDropContextProvider = ({
	children,
}: BackDropContextProviderProps) => {
	const [openBackDrop, setOpenBackDrop] = useState(false)

	return (
		<backDropContext.Provider value={{ openBackDrop, setOpenBackDrop }}>
			{children}
		</backDropContext.Provider>
	)
}
