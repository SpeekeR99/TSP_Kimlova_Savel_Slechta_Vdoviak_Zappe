---
sidebar_position: 2
sidebar_label: Zprovoznění GC generování
---

# Zprovoznění google classroom generování

Tento návod popisuje jednoduché kroky k vytvoření Google Apps Scriptu a jeho nasazení jako webové aplikace. URL této aplikace bude potřeba ke generování dotazníků za pomocí google forms.

---

## 1. Otevření Google Apps Script Editoru

1. Přejděte na [Google Apps Script](https://script.google.com/).
2. Klikněte na tlačítko **„Nový projekt“**.

---

## 2. Vložení kódu

1. Odstraňte všechen text, který je v editoru předvyplněný.
2. Vložte tento skript do editoru.

```javascript
const doPost = (e) => {
	if (!e) throw new Error('Form ID not present')
	const { formId } = JSON.parse(e.postData.contents)
	const res = exportFullFormDetails(formId)
	Logger.log(res)
	return ContentService.createTextOutput(
		JSON.stringify(res, null, 2)
	).setMimeType(ContentService.MimeType.JSON)
}

const exportFullFormDetails = (formId) => {
	const form = FormApp.openById(formId)
	if (!form) throw new Error('Form does not exist!')
	const items = form.getItems()
	const exportData = []

	items.forEach((item) => {
		const itemData = {
			text: item.getTitle(),
			type: item.getType().toString(),
			points: null,
			answers: [],
			image: null,
			id: null,
			subtext: item.getHelpText() || null,
		}

		try {
			if (item.getType() === FormApp.ItemType.MULTIPLE_CHOICE) {
				const mcQuestion = item.asMultipleChoiceItem()
				itemData.points = mcQuestion.getPoints()
				itemData.id = mcQuestion.getId()
				itemData.answers = mcQuestion.getChoices().map((choice) => ({
					value: choice.getValue(),
					isCorrect: choice.isCorrectAnswer ? choice.isCorrectAnswer() : false,
				}))
			} else if (
				item.getType() === FormApp.ItemType.TEXT ||
				item.getType() === FormApp.ItemType.PARAGRAPH_TEXT
			) {
				// No choices for text-based questions
				itemData.choices = []
			}
		} catch (e) {
			Logger.log(`Error processing item: ${item.getTitle()} - ${e.message}`)
		}

		exportData.push(itemData)
	})

	return JSON.stringify(exportData, null, 2)
}
```

3. Klikněte vlevo nahoře na **„Přejmenovat“** a pojmenujte si projekt podle vás.
4. Uložte změny pomocí **Ctrl + S** nebo kliknutím na ikonu disketky.

---

## 3. Nasazení skriptu jako webové aplikace

1. Klikněte na **Immplementovat** (vpravo nahoře) a vyberte možnost **„Nová implementace“**.
2. Klikněte na **Vyberte typ** a vyberte **Webová aplikace**.
3. Vyplňte nastavení:
   - **Popis nasazení:** Například „První verze“.
   - **Kdo má přístup:** Vyberte „Kdokoliv“.
4. Klikněte na **„Nasadit“**.

---

## 4. Získání URL adresy webové aplikace

1. Po nasazení se zobrazí dialogové okno s URL adresou vaší aplikace.
2. Zkopírujte tuto URL adresu a uložte si ji – tato adresa bude přidávat do aplikace.
