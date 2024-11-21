import React, { FC, Fragment } from 'react'
import {
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
import {
	ABOUT_PAGE,
	GENERATE_FROM_XML_PAGE,
	GENERATE_PAGE,
	MAIN_PAGE,
	STATISTICS_PAGE,
} from '../../constants'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import AnalyticsIcon from '@mui/icons-material/Analytics'

interface MenuItem {
	name: string
	icon: JSX.Element
	divider?: JSX.Element
	link: string
	disabled?: boolean
}

const ListItems: MenuItem[] = [
	{
		name: 'Upload arks',
		icon: <FileUploadIcon />,
		link: MAIN_PAGE,
	},
	{
		name: 'Generate from xml',
		icon: <UploadFileIcon />,
		link: GENERATE_FROM_XML_PAGE,
	},
	{
		name: 'Generation',
		icon: <ConstructionIcon />,
		divider: <Divider />,
		link: GENERATE_PAGE,
		disabled: true,
	},
	{
		name: 'Statistics',
		icon: <AnalyticsIcon />,
		divider: <Divider />,
		link: STATISTICS_PAGE,
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
			{ListItems.map(({ name, icon, divider, link, disabled }: MenuItem) => (
				<Fragment key={name}>
					<ListItem disablePadding onClick={() => !disabled && navigate(link)}>
						<ListItemButton disabled={disabled}>
							<ListItemIcon>{icon}</ListItemIcon>
							<ListItemText primary={name} style={{ marginLeft: '-20px' }} />
						</ListItemButton>
					</ListItem>
					{divider && divider}
				</Fragment>
			))}
		</>
	)
}

export default MenuItems
