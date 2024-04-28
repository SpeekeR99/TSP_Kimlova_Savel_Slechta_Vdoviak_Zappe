import React from 'react'
import BaseLayout from '../components/BaseLayout'
import DemoPaper from '@mui/material/Paper'
import { Typography } from '@mui/material'

const About = () => (
	<BaseLayout>
		<DemoPaper square={false} sx = {{margin: '5%'}}>
			<Typography variant="h3" paddingLeft={'3%'} paddingTop={'3%'}>
                About
			</Typography>
			<Typography  padding={'3%'}>
            Tento sw slouží jako nástroj pro generování písemkových testů a odpovědních 
            formulářů k nim. Nástroj umí vygenerovat unikátní písemkové testy pro každého studenta, 
            tak že vybere unikátní kombinaci testových otázek z platformy moodle. Tyto jednotlivé
            artefakty může pak uživatel vytisknout a rozdat svým studentům pro ověření jejich 
            znalostí. Vyplněné formuláře s odpověďmi se poté naskenují a tento nástroj je 
            automaticky vyhodnotí a odpovědi odešle na moodle. Nástroj je určen primárně 
            pro akademické pracovníky věnující se výuce. Nástroj byl vyvinut 
            za účelem úspory času a práce uživatelů při připravování i opravování 
            písemkových testů. Kromě toho ale zaručí i konzistentní a správné výsledky při 
            opravování těchto písemkových testů. Přináší užitek i studentům, kteří budou mít 
            výsledky rychleji. Také odpadá faktor lidské chyby při opravování
			</Typography>
		</DemoPaper>
	</BaseLayout>)

export default About
