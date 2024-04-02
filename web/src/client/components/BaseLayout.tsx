import React, { Fragment, ReactNode, useState } from 'react'
import { AppBar, Typography, Toolbar, Box } from '@mui/material'
import Menu from './Menu/Menu'
import { DrawerHeader, Main } from './Menu/styles'

interface BaseLayoutProps {
	children?: ReactNode
}

const Footer = () => (
	<Fragment>
		<AppBar position='fixed' color='primary' sx={{ top: 'auto', bottom: 0 }}>
			<Toolbar sx={{ height: '8vh' }}>
				<Typography
					variant='h6'
					sx={{
						zIndex: 1,
						margin: 'auto',
					}}
				>
					Copyright ©2024 The garbage collectors
				</Typography>
			</Toolbar>
		</AppBar>
	</Fragment>
)

const BaseLayout = ({ children }: BaseLayoutProps) => {
	const [open, setOpen] = useState<boolean>(false)

	return (
		<Box sx={{ display: 'flex' }}>
			<Menu open={open} setOpen={setOpen} />
			<Main open={open}>
				<DrawerHeader />
				{children}
			</Main>
			<Footer />
		</Box>
	)
}

export default BaseLayout
