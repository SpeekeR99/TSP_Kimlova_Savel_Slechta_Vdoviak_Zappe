import React from 'react'
import { Route, Routes } from 'react-router-dom'
import {
	ABOUT_PAGE,
	ERROR_PAGE,
	GENERATE_FROM_XML_PAGE,
	GENERATE_PAGE,
	MAIN_PAGE,
	NOT_FOUND_PAGE,
	STATISTICS_PAGE,
} from './constants'
import MainPage from './pages/MainPage'
import ErrorPage from './pages/ErrorPage'
import NotFoundPage from './pages/NotFoundPage'
import AboutPage from './pages/AboutPage'
import GeneratePage from './pages/GenerateFromMoodlePage'
import GenerateFromXMLPage from './pages/GenerateFromXMLPage'
import StatisticsPage from './pages/StatisticsPage'

const App = () => (
	<Routes>
		<Route path={MAIN_PAGE} element={<MainPage />} />
		<Route path={ERROR_PAGE} element={<ErrorPage />} />
		<Route path={GENERATE_PAGE} element={<GeneratePage />} />
		<Route path={ABOUT_PAGE} element={<AboutPage />} />
		<Route path={GENERATE_FROM_XML_PAGE} element={<GenerateFromXMLPage />} />
		<Route path={NOT_FOUND_PAGE} element={<NotFoundPage />} />
		<Route path={STATISTICS_PAGE} element={<StatisticsPage />} />
	</Routes>
)

export default App
