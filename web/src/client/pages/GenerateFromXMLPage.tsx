import React from 'react'
import BaseLayout from '../components/BaseLayout'
import MyDropzone from '../components/MyDropZone'
import { useGenerateFromXML } from '../hooks/useGenerateFromXml'
import MyBreadcrump from '../components/MyBreadcrump'

const GenerateFromXMLPage = () => {
	return (
		<BaseLayout>
			<MyBreadcrump parts={['generate', 'from-XML']} />
			<MyDropzone
				accept={{ 'application/xml': ['.xml'], 'text/csv': ['.csv'] }}
				maxFiles={2}
				useAction={useGenerateFromXML}
			/>
		</BaseLayout>
	)
}

export default GenerateFromXMLPage
