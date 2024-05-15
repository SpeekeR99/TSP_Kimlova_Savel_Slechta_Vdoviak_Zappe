import { Request, Response } from 'express'
import { CustomError } from '../interface'
const SERVER_ERROR_CODE = 500

const errorHandler = (err: CustomError, req: Request, res: Response): void => {
	const statusCode: number = err.statusCode || SERVER_ERROR_CODE
	res.status(statusCode).json({
		errorMsg: `Caught an error: ${err.message}`,
		errorData: err?.response?.data,
	})
}

export default errorHandler
