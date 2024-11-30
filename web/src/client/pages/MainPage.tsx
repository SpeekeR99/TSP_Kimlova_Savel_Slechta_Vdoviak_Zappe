import React from 'react'
import BaseLayout from '../components/BaseLayout'
import MyDropzone from '../components/MyDropZone'
import { useUploadArks } from '../hooks/useUploadArks'
import MyBreadcrump from '../components/MyBreadcrump'

const MainPage = () => (
	<BaseLayout>
		<MyBreadcrump parts={['upload', 'Sheets']} />
		<MyDropzone
			accept={{ 'application/pdf': ['.pdf'] }}
			maxFiles={1}
			useAction={useUploadArks}
			valid={true}
		/>
	</BaseLayout>
)
export default MainPage
