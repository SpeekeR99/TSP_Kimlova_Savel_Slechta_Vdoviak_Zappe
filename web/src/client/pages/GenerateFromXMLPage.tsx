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

const GenerateFromXMLPage = () => {
	const [date, setDate] = useState<Dayjs | null>(dayjs(Date.now()))

	return (
		<BaseLayout>
			<MyBreadcrump parts={['generate', 'from-XML']} />
			<Box display='flex' justifyContent='flex-end'>
				<LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale='en-gb'>
					<DatePicker
						label='Exam date'
						value={date}
						onChange={(newValue) => setDate(newValue)}
					/>
				</LocalizationProvider>
			</Box>
			<MyDropzone
				accept={{ 'application/xml': ['.xml'], 'text/csv': ['.csv'] }}
				maxFiles={2}
				useAction={() => useGenerateFromXML(date.toISOString())}
			/>
		</BaseLayout>
	)
}

export default GenerateFromXMLPage
