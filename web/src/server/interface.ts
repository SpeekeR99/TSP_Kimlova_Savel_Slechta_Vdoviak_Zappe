import { Router } from 'express'
import { MulterFile } from 'multer'

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

export interface Question {
	type: string | null
	id: string
	text: string
	answers: object[]
	defaultGrade: number
	penalty: number
}

export interface Student {
	jmeno: string
	prijmeni: string
	vizualni_id: string
	os_cislo: string
}

export interface Quiz {
	questions: Question[]
	students: Student[]
	date: string
}
