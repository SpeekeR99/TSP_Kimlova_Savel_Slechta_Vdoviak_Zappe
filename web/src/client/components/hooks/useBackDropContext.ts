import { useContext } from 'react'
import { backDropContext } from '../../context/backDropContext'

export const useBackDropContext = () => {
	const context = useContext(backDropContext)

	if (!context)
		throw new Error('Context has to be used inside context provider!')

	return context
}
