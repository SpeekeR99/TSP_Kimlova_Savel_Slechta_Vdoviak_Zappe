import React, { Fragment, ReactNode } from 'react'
import { AppBar, Typography, Toolbar, Box } from '@mui/material'

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

const Header = () => (
	<Box sx={{ flexGrow: 1, height: '8vh' }}>
		<AppBar component='nav'>
			<Toolbar sx={{ height: '8vh' }}>
				<Typography variant='h5' component='div' sx={{ flexGrow: 1 }}>
					ADT exam tool
				</Typography>
			</Toolbar>
		</AppBar>
	</Box>
)

const BaseLayout = ({ children }: BaseLayoutProps) => (
	<>
		{<Header />}
		{children}
		<Footer />
	</>
)

export default BaseLayout
