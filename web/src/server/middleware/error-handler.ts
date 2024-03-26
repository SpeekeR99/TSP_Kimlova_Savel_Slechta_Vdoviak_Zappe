import { Request, Response, NextFunction } from 'express'
import { CustomError } from '../interface'

const errorHandler = (
	err: CustomError,
	req: Request,
	res: Response,
	next: NextFunction
): void => {
	const statusCode: number = err.statusCode || 500
	res.status(statusCode).json({
		errorMsg: `Caught an error: ${err.message}`,
		errorData: err?.response?.data,
	})
}

export default errorHandler
