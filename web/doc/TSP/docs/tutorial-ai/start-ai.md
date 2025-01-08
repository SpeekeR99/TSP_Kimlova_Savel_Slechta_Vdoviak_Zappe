---
sidebar_position: 2
sidebar_label: Spuštění ai aplikace
---

# Zprovoznění ai aplikace

## Prerekvizity

- **Python verze 3+** (testováno na nejméně **Python 3.7+**)
- Manažer python balíčků **pip** (většinou je nainstalován spolu s pythonem)

## Jednoduchá verze

- Ve složce **ai/** je připraven skript **run.bat**
- Tento skript automaticky zakládá virtuální prostředí, instaluje potřebné závislosti a spouští aplikaci
- Příkaz: `run.bat`

## Složitější DYI verze

### Příprava

#### Vytvoření virtuálního prostředí

- Nejprve je nutné si prostředí vůbec vytvořit
- Příkaz: `python -m venv cesta/k/novemu/virtualnimu/prostredi `
- Následně je nutné si ho aktivovat
- Příkaz: `cesta/k/novemu/virtualnimu/prostredi/Scripts/activate`

#### Instalace závislostí

- Ve složce **ai/** je připraven soubor **requirements.txt**
- Příkaz: `pip install -r requirements.txt`

### Spuštění

- Aplikace se spouští pomocí spuštění **API**, které naslouchá na daném portu (momentálně **5000**)
- Příkaz: `python src/api_gateway.py`

## Basic usage:

#### ![](https://placehold.it/80x30/ffffff/ff0000?text=POZOR) !!!

- Existuje konfigurační soubor **ai/src/config.json**, ve kterém je nutné upravovat a dynamicky měnit klíč **number_of_questions** na základě testu, který je generován / evaluován!!!
- (Bude automatizováno v budoucnosti s příchodem DB + nadřazeného test ID)

## Vygenerování .pdf souborů na základě moodle dat

- API na adrese http://localhost:5000/get_print_data čeká na **.json** soubor v podobě pole objektů, kde jednotlivé objekty jsou jednotlivé otázky v předem daném formátu (podle moodle)
- Vrací **.zip** soubor s dvěma .pdf soubory - jedná se o **mergnuté .pdf** soubory jednotlivých otázkových souborů (resp. záznamových archů)
- **Adresa: /get_print_data**
- **Metoda: POST**
- **Vstup: .json (export moodle)**
- **Výstup: .zip (mergnuté .pdf)**

## Vyhodnocení naskenovaného .pdf testu

- API na adrese http://localhost:5000/test_evaluation čeká na **.pdf** soubor, který je následně zpracován a vyhodnocen jako naskenovaný vyplněný test
- Vrací **.json** odpověď (**momentálně** v podobě slovníku, kde na klíči "student_id" je ID daného studenta a na klíči "answers" je seřazené pole (dle původního .pdf souboru), kde ke každé otázce je vráceno pole odpovědí 1/0 (zaškrtnuto / nezaškrtnuto)
- **Adresa: /test_evaluation**
- **Metoda: POST**
- **Vstup: .pdf (naskenovaný test)**
- **Výstup: .json (vyhodnocení)**
