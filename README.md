# Automated Scraping of CAD parts from "meusburger.com"

This repo contains scripts to scrape 3D CAD (.STP) files from Meusburger.com using Chromedriver. 
Meusburger is a leading manufacturer of Mold Making components (scraped from their shopping portal: https://ecom.meusburger.com/index/index.asp). 

I'll continue to update this repo to expand on the number of parts extracted. Please feel free to reach out if you have any questions and/or feedback :) 

### Latest Update (25th July)
Scraping speeds increased. Totaly individual parts extractable are ~6000 now. Tqdm introduced for better management. Approx. scraping times and parts extracted shown below.

# Installation
## Step 1: Clone the repo
```sh
git clone https://github.com/ksbharaj/meusburger_scraper.git
cd meusburger_scraper
```

## Step 2: Install Chromedriver
Download Chromedriver from [here](https://googlechromelabs.github.io/chrome-for-testing/) and ensure it's compatible with your Chrome version. Add it to your system PATH.

## Step 3: Install Packages
Ideally using Python 3.11, install the attached requirements file

```sh
pip install -r requirements.txt
```

## Step 4: Meusburger_Scraper_v1.py
Run this script using CLI to scrape the STEP Files. All parts are saved within a single STEP file in the Chrome Browser's default download location. 

Currently, you can choose to scrape from the following sections:
- "F/P Length": Mould plates for lengthwise mould types
- "F/P Cross": Mould plates for crosswise mould types
- "FB/P Blocks": Blocks for sliding core moulds 
- "FB/P Plates": Plates for sliding core moulds
- "FW Plates": Plates for change moulds
- "FW Parts": Parts for change moulds
- "FM Parts": Parts for micro moulds
- "H Parts": H 1000 Clamping system

### Example Usage:

```sh
python Meusburger_Scraper_v1.py "FM Parts" 
```

### Example Output:
Found in "Sample Data Output/Meusburger_Scraper output"

## Step 5: extract_stp_file.py

This script extracts all the individual STEP files from the STEP file produced by Step 4, and stores them in a folder location of your choice. 

### Example Usage:

```sh
python extract_stp_file.py path/to/your/step_file.stp path/to/output_directory
```
### Example Output:
Found in "Sample Data Output/extract_stp_file output"

## Dependencies
- Python 3.8 or higher (3.11 ideally)
- Chromedriver (compatible with your Chrome version)
- Required Python packages (see requirements.txt)

## Error Handling and Limitations
- Scraper may encounter issues if the website structure changes.
- As previously mentioned, long runtime for "E Parts" scraping due to the large number of parts.



