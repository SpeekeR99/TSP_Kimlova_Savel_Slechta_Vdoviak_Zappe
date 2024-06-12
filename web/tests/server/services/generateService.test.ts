import { MulterFile } from 'multer'
import {
	parseQuizXMLFile,
	parseStudentCSVFile,
} from '../../../src/server/service/generateService'

// Mock implementation to avoid TypeScript errors
const mockMulterFile = (buffer: Buffer) => ({ buffer } as MulterFile)

describe('generateService', () => {
	beforeEach(() => {
		jest.clearAllMocks()
	})

	// parse function

	it('Parse valid xml file -> Returns xml data as formatted json', async () => {
		const xml = `
      <?xml version="1.0" encoding="UTF-8"?>
      <quiz>
        <question type="category">
          <category>
            <text>$module$/top/Výchozí v Testovací test</text>
          </category>
          <info format="moodle_auto_format">
            <text><![CDATA[Výchozí kategorie pro úlohy sdílené v kontextu "Testovací test".]]></text>
          </info>
          <idnumber></idnumber>
        </question>
        <question type="multichoice">
          <name>
            <text>question</text>
          </name>
          <questiontext format="html">
            <text><![CDATA[<p dir="ltr" style="text-align: left;">question is question</p>]]></text>
          </questiontext>
          <generalfeedback format="html">
            <text></text>
          </generalfeedback>
          <defaultgrade>1.0000000</defaultgrade>
          <penalty>0.3333333</penalty>
          <hidden>0</hidden>
          <idnumber>1</idnumber>
          <single>true</single>
          <shuffleanswers>true</shuffleanswers>
          <answernumbering>abc</answernumbering>
          <showstandardinstruction>0</showstandardinstruction>
          <correctfeedback format="html">
            <text>Your answer is correct.</text>
          </correctfeedback>
          <partiallycorrectfeedback format="html">
            <text>Your answer is partially correct.</text>
          </partiallycorrectfeedback>
          <incorrectfeedback format="html">
            <text>Your answer is incorrect.</text>
          </incorrectfeedback>
          <shownumcorrect/>
          <answer fraction="0" format="html">
            <text><![CDATA[<p dir="ltr" style="text-align: left;">res1</p>]]></text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
          <answer fraction="100" format="html">
            <text><![CDATA[<p dir="ltr" style="text-align: left;">res2</p>]]></text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
          <answer fraction="0" format="html">
            <text><![CDATA[<p dir="ltr" style="text-align: left;">res3</p>]]></text>
            <feedback format="html">
              <text><![CDATA[<p dir="ltr" style="text-align: left;">res4</p>]]></text>
            </feedback>
          </answer>
        </question>
        <question type="truefalse">
          <name>
            <text>question 2</text>
          </name>
          <questiontext format="html">
            <text><![CDATA[<p dir="ltr" style="text-align: left;">is today monday?</p>]]></text>
          </questiontext>
          <generalfeedback format="html">
            <text></text>
          </generalfeedback>
          <defaultgrade>2.0000000</defaultgrade>
          <penalty>1.0000000</penalty>
          <hidden>0</hidden>
          <idnumber>2</idnumber>
          <answer fraction="100" format="moodle_auto_format">
            <text>true</text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
          <answer fraction="0" format="moodle_auto_format">
            <text>false</text>
            <feedback format="html">
              <text></text>
            </feedback>
          </answer>
        </question>
      </quiz>
    `
		const file = mockMulterFile(Buffer.from(xml))
		const result = await parseQuizXMLFile(file)

		expect(result).toEqual([
			{
				type: 'multichoice',
				id: '1',
				text: '<p dir="ltr" style="text-align: left;">question is question</p>',
				answers: [
					{
						text: '<p dir="ltr" style="text-align: left;">res1</p>',
						fraction: '0',
					},
					{
						text: '<p dir="ltr" style="text-align: left;">res2</p>',
						fraction: '100',
					},
					{
						text: '<p dir="ltr" style="text-align: left;">res3</p>',
						fraction: '0',
					},
				],
				defaultGrade: '1.0000000',
				penalty: '0.3333333',
				name: ['question'],
			},
			{
				type: 'truefalse',
				id: '2',
				text: '<p dir="ltr" style="text-align: left;">is today monday?</p>',
				answers: [
					{ text: 'true', fraction: '100' },
					{ text: 'false', fraction: '0' },
				],
				defaultGrade: '2.0000000',
				penalty: '1.0000000',
				name: ['question 2'],
			},
		])
	})

	it('should reject with error if XML parsing fails', async () => {
		const file = mockMulterFile(
			Buffer.from(
				'<?xml version="1.0" encoding="UTF-8"?><invalid>xml</invalid>'
			)
		)

		await expect(parseQuizXMLFile(file)).rejects.toThrow(
			'XML file does not contain quiz!'
		)
	})

	it('should reject with error if quiz does not contain questions', async () => {
		const xml = '<?xml version="1.0" encoding="UTF-8"?><quiz></quiz>'
		const file = mockMulterFile(Buffer.from(xml))

		await expect(parseQuizXMLFile(file)).rejects.toThrow(
			'XML file does not contain questions!'
		)
	})

	it('should ignore questions with invalid types', async () => {
		const xml = `
	  <quiz>
	    <question type="invalid">
	      <idnumber>1</idnumber>
	      <questiontext>
	        <text>Invalid question type</text>
	      </questiontext>
	      <name>
	        <text>Invalid Question</text>
	      </name>
	      <answer>invalid</answer>
	      <defaultgrade>1</defaultgrade>
	      <penalty>0.1</penalty>
	    </question>
	  </quiz>
	`
		const file = mockMulterFile(Buffer.from(xml))
		const result = await parseQuizXMLFile(file)

		expect(result).toEqual([])
	})

	// csv function

	it('should parse a CSV file and return an array of objects', async () => {
		const csvFile = `"osCislo";"jmeno";"prijmeni";"titulPred";"titulZa";"stav";"userName";"stprIdno";"nazevSp";"fakultaSp";"kodSp";"formaSp";"typSp";"typSpKey";"mistoVyuky";"rocnik";"financovani";"oborKomb";"oborIdnos";"email";"maxDobaDatum";"simsP58";"simsP59";"cisloKarty";"pohlavi";"rozvrhovyKrouzek";"studijniKruh";"evidovanBankovniUcet";"statutPredmetu";"casPrihlaseni";"omluven"
        "A12B1230P";"Pepa";"Vlas";"Bc.";"";"S";"myUsername";"762";"Softwarove inzenyrstvi";"FAV";"N3902";"P";"N";"0";"P";"3";"1";"SWInp";"2166";"random@students.zcu.cz";"";"";"";"3123123123";"M";"";"";"";"A";"5.1.2024 11:18";"N"
        "X98Y7654T";"Alice";"Smith";"Mgr.";"";"S";"aliceSmith";"123";"Computer Science";"FCI";"C1234";"P";"N";"0";"P";"2";"1";"CompSci";"1234";"alice.smith@example.com";"";"";"";"1234567890";"F";"";"";"";"A";"6.11.2023 09:45";"N"
        "Z12W3456R";"Bob";"Johnson";"Ing.";"";"S";"bobJohnson";"456";"Electrical Engineering";"FEE";"E5678";"P";"N";"0";"P";"4";"1";"ElecEng";"5678";"bob.johnson@example.com";"";"";"";"0987654321";"M";"";"";"";"A";"8.5.2022 14:30";"N"`

		const file = mockMulterFile(Buffer.from(csvFile))
		const result = await parseStudentCSVFile(file)

		expect(Array.isArray(result)).toBe(true)
		expect(result.length).toBeGreaterThan(0)
	})

	it('should handle errors gracefully', async () => {
		const file = mockMulterFile(Buffer.from('invalid csv data'))

		await expect(await parseStudentCSVFile(file)).toEqual([])
	})
})
