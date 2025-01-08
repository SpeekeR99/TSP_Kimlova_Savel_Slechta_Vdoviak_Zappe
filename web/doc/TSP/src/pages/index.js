import clsx from 'clsx'

import Layout from '@theme/Layout'

import Heading from '@theme/Heading'
import styles from './index.module.css'

function HomepageHeader() {
	return (
		<header className={clsx('hero hero--primary', styles.heroBanner)}>
			<div className='container'>
				<Heading as='h1' className='hero__title'>
					TSP - Exam tool
				</Heading>
				<p className='hero__subtitle'>Garbage collectors</p>
			</div>
		</header>
	)
}

export default function Home() {
	return (
		<Layout>
			<HomepageHeader />
			<main className={styles.centeredText}>
				This sw is used as a tool for generating tests and answer forms for
				them. The tool can generate unique test papers for each student by
				selecting a unique combination of test questions from the moodle
				platform. These individual artifacts can then be printed by the user and
				distributed to their students to test their knowledge. The completed
				answer sheets are then scanned and the tool automatically evaluates them
				and uploads the answers to moodle. The tool is designed primarily for
				academics involved in teaching. The tool has been developed to save
				users time and effort in preparing and correcting tests. In addition, it
				will also guarantee consistent and correct results when correcting these
				tests. It also benefits the students who will get the results faster. It
				also eliminates the factor of human error in correcting.
			</main>
		</Layout>
	)
}
