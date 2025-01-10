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
import GoogleIcon from '@mui/icons-material/Google'
import DescriptionIcon from '@mui/icons-material/Description'
import InfoIcon from '@mui/icons-material/Info'
import { useNavigate } from 'react-router-dom'
import {
	ABOUT_PAGE,
	GENERATE_FROM_GCROOM_PAGE,
	GENERATE_FROM_XML_PAGE,
	GENERATE_PAGE,
	MAIN_PAGE,
	STATISTICS_PAGE,
} from '../../consts/constants'
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
		name: 'Upload sheets',
		icon: <FileUploadIcon />,
		link: MAIN_PAGE,
	},
	{
		name: 'Generate from xml',
		icon: <UploadFileIcon />,
		link: GENERATE_FROM_XML_PAGE,
	},
	{
		name: 'Generate from Google Classroom',
		icon: <GoogleIcon />,
		link: GENERATE_FROM_GCROOM_PAGE,
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
		name: 'Doc',
		icon: <DescriptionIcon />,
		link: 'http://localhost:3000',
	},
	{
		name: 'About',
		icon: <InfoIcon />,
		link: ABOUT_PAGE,
	},
]

const MenuItems: FC = () => {
	const navigate = useNavigate()

	const handleClick = ({ link, disabled }) => {
		if (disabled) return
		if (link.startsWith('http://')) window.location.href = link
		else navigate(link)
	}

	return (
		<>
			{ListItems.map(({ name, icon, divider, link, disabled }: MenuItem) => (
				<Fragment key={name}>
					<ListItem
						disablePadding
						onClick={() => handleClick({ link, disabled })}
					>
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
