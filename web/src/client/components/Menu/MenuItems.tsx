import React, { FC, Fragment } from 'react'
import {
	Box,
	Divider,
	ListItem,
	ListItemButton,
	ListItemIcon,
	ListItemText,
} from '@mui/material'
import FileUploadIcon from '@mui/icons-material/FileUpload'
import ConstructionIcon from '@mui/icons-material/Construction'
import InfoIcon from '@mui/icons-material/Info'
import { useNavigate } from 'react-router-dom'
import { ABOUT_PAGE, GENERATE_PAGE, MAIN_PAGE } from '../../constants'

interface MenuItem {
	name: string
	icon: JSX.Element
	divider?: JSX.Element
	link: string
}

const ListItems: MenuItem[] = [
	{
		name: 'Upload',
		icon: <FileUploadIcon />,
		link: MAIN_PAGE,
	},
	{
		name: 'Generation',
		icon: <ConstructionIcon />,
		divider: <Divider />,
		link: GENERATE_PAGE,
	},
	{
		name: 'About',
		icon: <InfoIcon />,
		link: ABOUT_PAGE,
	},
]

const MenuItems: FC = () => {
	const navigate = useNavigate()
	return (
		<>
			{ListItems.map(({ name, icon, divider, link }: MenuItem) => (
				<Fragment key={name}>
					<ListItem disablePadding onClick={() => navigate(link)}>
						<ListItemButton>
							<ListItemIcon>{icon}</ListItemIcon>
							<ListItemText primary={name} />
						</ListItemButton>
					</ListItem>
					{divider && divider}
				</Fragment>
			))}
		</>
	)
}

export default MenuItems
