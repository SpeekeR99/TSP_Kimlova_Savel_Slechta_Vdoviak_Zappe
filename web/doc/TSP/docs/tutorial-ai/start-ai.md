---
sidebar_position: 2
sidebar_label: Spuštění ai aplikace
---

# Zprovoznění ai aplikace

## Prerekvizity

- `Python verze 3+` (testováno na nejméně `Python 3.7`) 
- Manažer python balíčků `pip` (většinou je nainstalován spolu s `Pythonem`)

## Jednoduchá verze

- Ve složce `/ai/` je připraven skript `run.sh` (pro **Linux**) nebo `run.bat` (pro **Windows**)
- Tento skript automaticky zakládá virtuální prostředí, instaluje potřebné závislosti a spouští aplikaci 
- Příkaz: `./run.sh` nebo `run.bat`

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

- Existuje konfigurační soubor `/ai/config.json`, ve kterém je možné nastavit např. barvy a texty, které se budou generovat do výsledných **.pdf**.
Dále je v tomto konfiguračním souboru možné nastavit `Google Classroom multiplikátor` záporných bodů za špatnou odpověď (default: 0.25).

### Vygenerování .pdf souborů na základě Moodle dat

- API na adrese http://localhost:5000/get_print_data čeká na **.json** soubor v podobě pole objektů, kde jednotlivé objekty jsou jednotlivé otázky v předem daném formátu (podle Moodle) 
- Vrací **.zip** soubor s dvěma .pdf soubory - jedná se o **mergnuté .pdf** soubory jednotlivých otázkových souborů (resp. záznamových archů) 
- **Adresa: /get_print_data**
- **Metoda: POST**
- **Vstup: .json (export Moodle)**
- **Výstup: .zip (mergnuté .pdf)**

### Vygenerování .pdf souborů na základě Google Classroom dat

- API na adrese http://localhost:5000/generate-gf-data čeká na **.json** soubor v podobě pole objektů, kde jednotlivé objekty jsou jednotlivé otázky v předem daném formátu (podle Google Classroom)
- Prakticky se interně převádí na formát, který je následně zpracován stejně jako **Moodle data**
- Vrací **.zip** soubor s dvěma .pdf soubory - jedná se o **mergnuté .pdf** soubory jednotlivých otázkových souborů (resp. záznamových archů)
- **Adresa: /generate-gf-data**
- **Metoda: POST**
- **Vstup: .json (export Google Classroom)**
- **Výstup: .zip (mergnuté .pdf)**

### Vyhodnocení naskenovaného .pdf testu 

- API na adrese http://localhost:5000/test_evaluation čeká na **.pdf** soubor, který je následně zpracován a vyhodnocen jako naskenovaný vyplněný test 
- Vrací **.json** odpověď (**momentálně** v podobě slovníku, kde na klíči "student_id" je ID daného studenta a na klíči "answers" je seřazené pole (dle původního .pdf souboru), kde ke každé otázce je vráceno pole odpovědí 1/0 (zaškrtnuto / nezaškrtnuto) 
- **Adresa: /test_evaluation**
- **Metoda: POST**
- **Vstup: .pdf (naskenovaný test)**
- **Výstup: .json (vyhodnocení)**