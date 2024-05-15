import React, { useEffect, useState } from 'react'
import { Box, Button, Container, Tooltip, Typography } from '@mui/material'
import {
	useDropzone,
	DropzoneRootProps,
	DropzoneInputProps,
} from 'react-dropzone'
import { Stack } from '@mui/system'
import { useBackDropContext } from '../hooks/useBackDropContext'
import { UseMutationResult } from 'react-query'
import { useSnackbarContext } from '../hooks/useSnackbarContext'
import { SnackbarContextType } from '../context/snackbarContext/interface'
import { setSnackbarOpen } from '../context/snackbarContext/snackbarActions'

interface MyDropzoneProps {
	accept: {
		[mimeType: string]: string[]
	}
	maxFiles: number
	useAction: () => UseMutationResult,
	valid: boolean
}

const MyDropzone = ({ accept, useAction, maxFiles, valid }: MyDropzoneProps) => {
	const { mutate, isLoading, isSuccess } = useAction()
	const [files, setFiles] = useState<File[]>([])
	const { setOpenBackDrop } = useBackDropContext()
	const { dispatch }: SnackbarContextType = useSnackbarContext()
	const openSnackbar = (message: string, severity: string = 'success') =>
		dispatch(setSnackbarOpen(message, severity))

	useEffect(() => {
		setOpenBackDrop(isLoading)
	}, [isLoading])

	useEffect(() => {
		if (isSuccess) setFiles([])
	}, [isSuccess])

	const findSameType = (acceptedFileType: string): number => {
		return files.findIndex(({ type }) => type === acceptedFileType)
	}

	const getFileInfo = (file: File): { name: string; ext: string } => {
		const { name: fileName } = file
		const lastDotIndex = fileName.lastIndexOf('.')
		const name = fileName.substring(0, lastDotIndex)
		const ext = fileName.substring(lastDotIndex)
	
		return { name, ext }
	}
	

	const onDropAccepted = (acceptedFiles: File[]) => {
		const newFiles = [...files]

		acceptedFiles.forEach((acceptedFile) => {
			const sameTypeIndex = findSameType(acceptedFile.type)

			if (sameTypeIndex === -1) newFiles.push(acceptedFile)
			else newFiles[sameTypeIndex] = acceptedFile
		})

		setFiles(newFiles)
	}

	const onDropRejected = () => openSnackbar('Invalid file type!', 'warning')

	const {
		getRootProps,
		getInputProps,
		isDragActive,
	}: {
		getRootProps: () => DropzoneRootProps
		getInputProps: () => DropzoneInputProps
		isDragActive: boolean
	} = useDropzone({
		onDropAccepted,
		onDropRejected,
		accept,
		maxFiles,
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
						<em>
							(Allowed types:{' '}
							{Object.values(accept)
								.flatMap((exts) => exts)
								.join(', ')}
							)
						</em>
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
					{files.map((file, i) => {
						const { name, ext } = getFileInfo(file)
						const fileNameLengthRestriction = 25
						return (
							<Tooltip title={file.name} key={`tooltip${i}`}>
								<Typography
									variant='body1'
									color='textSecondary'
									key={`file${i}`}
								>
									File selected:{' '}
									<>
										{file.name.length > fileNameLengthRestriction
											? `${name.substring(
												0,
												fileNameLengthRestriction
											)}...${ext}`
											: file.name}
									</>
								</Typography>
							</Tooltip>
						)
					})}
				</Box>
				<Button
					variant='contained'
					disabled={files.length !== maxFiles || !valid}
					onClick={() => mutate(files)}
				>
					Upload file
				</Button>
			</Stack>
		</Container>
	)
}

export default MyDropzone
