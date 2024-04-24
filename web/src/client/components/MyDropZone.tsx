import React, { useCallback, useEffect, useState } from 'react'
import { Box, Button, Container, Typography } from '@mui/material'
import {
	useDropzone,
	DropzoneRootProps,
	DropzoneInputProps,
} from 'react-dropzone'
import { Stack } from '@mui/system'
import { useBackDropContext } from '../hooks/useBackDropContext'
import { UseMutationResult } from 'react-query'

interface MyDropzoneProps {
	mimeType: string
	extension: string
	useAction: () => UseMutationResult
}

const MyDropzone = ({ mimeType, extension, useAction }: MyDropzoneProps) => {
	const { mutate, isLoading, isSuccess } = useAction()
	const [file, setFile] = useState<File | null>(null)
	const { setOpenBackDrop } = useBackDropContext()

	useEffect(() => {
		setOpenBackDrop(isLoading)
	}, [isLoading])

	useEffect(() => {
		if (isSuccess) setFile(null)
	}, [isSuccess])

	const onDrop = useCallback((acceptedFiles: File[]) => {
		if (acceptedFiles.length > 0) setFile(acceptedFiles[0])
	}, [])

	const {
		getRootProps,
		getInputProps,
		isDragActive,
	}: {
		getRootProps: () => DropzoneRootProps
		getInputProps: () => DropzoneInputProps
		isDragActive: boolean
	} = useDropzone({
		onDrop,
		accept: {
			[mimeType]: [extension],
		},
		maxFiles: 1,
	})

	return (
		<Container maxWidth='sm'>
			<Box
				height='30vh'
				marginTop='15%'
				border='dashed 2px #0c4b63'
				borderRadius='10px'
				sx={{ bgcolor: '#daeff7' }}
				alignContent='center'
				textAlign='center'
				marginBottom='2%'
				{...getRootProps()}
			>
				<input {...getInputProps()} />
				{isDragActive ? (
					<Typography variant='h6' color='#0c4b63'>
						Drop the files here ...
					</Typography>
				) : (
					<>
						<Typography variant='h6' color='#0c4b63'>
							Drag 'n' drop or select your file...
						</Typography>
						<em>(Allowed types: {extension})</em>
					</>
				)}
			</Box>
			<Stack
				direction='row'
				justifyContent='space-between'
				alignItems='center'
				spacing={2}
			>
				<Box
					sx={{
						flexGrow: 0,
						flexShrink: 0,
					}}
				>
					{file && (
						<Typography variant='body1' color='textSecondary'>
							File selected: {file.name}
						</Typography>
					)}
				</Box>
				<Button
					variant='contained'
					disabled={!file}
					onClick={() => mutate(file)}
				>
					Upload file
				</Button>
			</Stack>
		</Container>
	)
}

export default MyDropzone
