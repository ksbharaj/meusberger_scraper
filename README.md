# Automated Scraping of CAD parts from "meusburger.com"

This repo contains scripts to scrape 3D CAD (.STP) files from Meusburger.com using Chromedriver. 
Meusberger is a leading manufacturer of Mold Making components (please visit https://www.meusburger.com/ for more details). 

# Installation
## Step 1: Clone the repo
```sh
git clone https://github.com/ksbharaj/meusberger_scraper.git
cd meusberger_scraper
```

## Step 2: Install Chromedriver
Download Chromedriver from [here](https://googlechromelabs.github.io/chrome-for-testing/) and ensure it's compatible with your Chrome version. Add it to your system PATH.

## Step 3: Install Packages
Ideally using Python 3.11, install the attached requirements file

```sh
pip install -r requirements.txt
```

## Step 4: Meusberger_Scraper_v1.py
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
- "E Parts": Miscellaneous Components

PLEASE NOTE: "E Parts" currently takes quite a while to run- up to 3 hours, as it contains at least 2000+ parts (this can/will be optimized).

### Example Usage:

```sh
python Meusberger_Scraper_v1.py "FW Parts" 
```

## Step 3: Extract All Step Files from the single .stp downloading

All the CAD models downloaded from Meusberger are stored in a single STEP file. This script extracts all the individual STEP files, storing them in a location of your choice. 

### Example Usage:

```sh
python extract_stp_file.py path/to/your/step_file.stp path/to/output_directory
```

## Dependencies
- Python 3.8 or higher
- Chromedriver (compatible with your Chrome version)
- Required Python packages (see requirements.txt)

## Error Handling and Limitations
- Scraper may encounter issues if the website structure changes.
- As previously mentioned, long runtime for "E Parts" scraping due to the large number of parts.



