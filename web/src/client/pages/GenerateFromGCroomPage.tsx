import React, { useState } from 'react'
import BaseLayout from '../components/BaseLayout'
import MyDropzone from '../components/MyDropZone'
import MyBreadcrump from '../components/MyBreadcrump'
import { DatePicker } from '@mui/x-date-pickers'
import dayjs, { Dayjs } from 'dayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { Box, Container, TextField } from '@mui/material'
import 'dayjs/locale/en-gb'
import { useGenerateFromGCroom } from '../hooks/useGenerateFromGoogleForms'

const MAX_YEAR = 2100

const GenerateFromGCroomPage = () => {
	const [date, setDate] = useState<Dayjs | null>(dayjs(Date.now()))
	const [isDateValid, setIsDateValid] = useState<boolean>(true)
	const [formId, setFormId] = useState<string>('')

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
			<MyBreadcrump parts={['generate', 'from-Google-Classroom']} />
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

			<Container maxWidth='sm'>
				<TextField
					id='Form id'
					label='Form id'
					placeholder='Form id'
					fullWidth
					sx={{ maxWidth: '100%', margin: 'auto', marginBottom: '-20%' }}
					onChange={(e) => setFormId(e.target.value)}
				/>
			</Container>
			<MyDropzone
				accept={{ 'text/csv': ['.csv'] }}
				maxFiles={1}
				useAction={() => useGenerateFromGCroom(date, formId)}
				valid={isDateValid && formId !== ''}
			/>
		</BaseLayout>
	)
}

export default GenerateFromGCroomPage
