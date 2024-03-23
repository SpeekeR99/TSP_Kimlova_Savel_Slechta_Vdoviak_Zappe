import React from 'react'
import { Route, Routes } from 'react-router-dom'
import { ERROR_PAGE, MAIN_PAGE, NOT_FOUND_PAGE } from './constants'
import MainPage from './pages/MainPage'
import ErrorPage from './pages/ErrorPage'
import NotFoundPage from './pages/NotFoundPage'

const App = () => (
	<Routes>
		<Route path={MAIN_PAGE} element={<MainPage />} />
		<Route path={ERROR_PAGE} element={<ErrorPage />} />
		<Route path={NOT_FOUND_PAGE} element={<NotFoundPage />} />
	</Routes>
)

export default App
