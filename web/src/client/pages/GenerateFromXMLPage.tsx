import React, { useState } from 'react'
import BaseLayout from '../components/BaseLayout'
import MyDropzone from '../components/MyDropZone'
import { useGenerateFromXML } from '../hooks/useGenerateFromXml'
import MyBreadcrump from '../components/MyBreadcrump'
import { DatePicker } from '@mui/x-date-pickers'
import dayjs, { Dayjs } from 'dayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { Box } from '@mui/material'
import 'dayjs/locale/en-gb'

const MAX_YEAR = 2100

const GenerateFromXMLPage = () => {
	const [date, setDate] = useState<Dayjs | null>(dayjs(Date.now()))
	const [isDateValid, setIsDateValid] = useState<boolean>(true)

	const handleDateChange = (newDate: Dayjs | null) => {
		const today = Date.now()
		const dateValid =
			newDate.isValid() &&
			newDate.year() < MAX_YEAR &&
			(newDate.isAfter(today) || newDate.isSame(today))

		if (dateValid) setDate(newDate)
		setIsDateValid(dateValid)
	}

	return (
		<BaseLayout>
			<MyBreadcrump parts={['generate', 'from-XML']} />
			<Box display='flex' justifyContent='flex-end'>
				<LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale='en-gb'>
					<DatePicker
						disablePast
						label='Exam date'
						value={date}
						onChange={handleDateChange}
						maxDate={dayjs().year(MAX_YEAR).startOf('year')}
					/>
				</LocalizationProvider>
			</Box>
			<MyDropzone
				accept={{ 'application/xml': ['.xml'], 'text/csv': ['.csv'] }}
				maxFiles={2}
				useAction={() => useGenerateFromXML(date)}
				valid={isDateValid}
			/>
		</BaseLayout>
	)
}

export default GenerateFromXMLPage
