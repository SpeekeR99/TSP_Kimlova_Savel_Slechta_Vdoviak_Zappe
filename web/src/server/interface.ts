import { Router } from 'express'

export interface Route {
	path: string
	router: Router
}

export interface CustomError extends Error {
	statusCode?: number
	response?: {
		data: any
	}
}
