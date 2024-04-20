import { Breadcrumbs, Typography } from '@mui/material'
import React from 'react'

interface MyBreadcrumpProps {
	parts: string[]
}

const MyBreadcrump = ({ parts }: MyBreadcrumpProps) => {
	return (
		<div role='presentation'>
			<Breadcrumbs aria-label='breadcrumb'>
				{parts.map((part, i, arr) => {
					if (i === arr.length - 1)
						return (
							<Typography key={`${part}${i}`} color='text.primary'>
								{part}
							</Typography>
						)
					return (
						<div key={`${part}${i}`} color='inherit'>
							{part}
						</div>
					)
				})}
			</Breadcrumbs>
		</div>
	)
}

export default MyBreadcrump
