import React from 'react'
import BaseLayout from '../components/BaseLayout'
import MyDropzone from '../components/MyDropZone'
import { useUploadArks } from '../hooks/useUploadArks'
import MyBreadcrump from '../components/MyBreadcrump'

const MainPage = () => (
	<BaseLayout>
		<MyBreadcrump parts={['upload', 'Arks']} />
		<MyDropzone
			accept={{ 'application/pdf': ['.pdf'] }}
			maxFiles={1}
			useAction={useUploadArks}
		/>
	</BaseLayout>
)
export default MainPage
