import React from 'react'
import { useTheme, Theme } from '@mui/material/styles'
import Box from '@mui/material/Box'
import Drawer from '@mui/material/Drawer'
import CssBaseline from '@mui/material/CssBaseline'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import IconButton from '@mui/material/IconButton'
import MenuIcon from '@mui/icons-material/Menu'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import MenuItems from './MenuItems'
import { AppBar, DrawerHeader } from './styles'

const drawerWidth = 240

interface HeaderProps {
	open: boolean
	handleDrawerOpen: () => void
}

interface MenuProps {
	open: boolean
	setOpen: (boolean) => void
}

const Header = ({ open, handleDrawerOpen }: HeaderProps) => (
	<AppBar open={open} sx={{ height: '8vh' }}>
		<Toolbar>
			<IconButton
				color='inherit'
				aria-label='open drawer'
				onClick={handleDrawerOpen}
				edge='start'
				sx={{ mr: 2, ...(open && { display: 'none' }) }}
			>
				<MenuIcon />
			</IconButton>
			<Typography variant='h5' component='div' sx={{ flexGrow: 1 }}>
				ADT exam tool
			</Typography>
		</Toolbar>
	</AppBar>
)

const Menu = ({ open, setOpen }: MenuProps) => {
	const theme: Theme = useTheme()

	const handleDrawerOpen = () => {
		setOpen(true)
	}

	const handleDrawerClose = () => {
		setOpen(false)
	}

	return (
		<>
			<CssBaseline />
			<Header open={open} handleDrawerOpen={handleDrawerOpen} />
			<Drawer
				sx={{
					width: drawerWidth,
					flexShrink: 0,
					'& .MuiDrawer-paper': {
						width: drawerWidth,
						boxSizing: 'border-box',
					},
				}}
				variant='persistent'
				anchor='left'
				open={open}
			>
				<DrawerHeader>
					<IconButton onClick={handleDrawerClose}>
						{theme.direction === 'ltr' ? (
							<ChevronLeftIcon />
						) : (
							<ChevronRightIcon />
						)}
					</IconButton>
				</DrawerHeader>
				<Divider />
				<MenuItems />
				<Divider />
			</Drawer>
		</>
	)
}

export default Menu
