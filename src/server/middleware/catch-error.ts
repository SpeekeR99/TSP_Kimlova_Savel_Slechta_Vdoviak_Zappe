import { Request, Response, NextFunction } from 'express'

const catchError = (
	handler: (req: Request, res: Response, next: NextFunction) => Promise<void>
) => {
	return async (req: Request, res: Response, next: NextFunction) => {
		try {
			await handler(req, res, next)
		} catch (e) {
			console.error(e)
			next(e)
		}
	}
}

export default catchError
