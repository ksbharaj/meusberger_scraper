# Automated Scraping from CAD parts from "meusburger.com"

This repo contains code that uses Chromedriver to scrape sections of Meusberger.com to download 3D CAD (.STP) files related to injection mold tools. Please follow the instructions below to tailor it for your usage.

## Step 1: Install Packages
Ideally using Python 3.11, install the attached requirements file

```sh
pip install -r requirements.txt
```

## Step 2: Meusberger_Scraper_v1.py
Run this script using CLI to extract 3D CAD data using Chromedriver, and store it in your Chrome Browser's default Download location. 

Currently, you can choose to scrape for the following options:
- "F/P Length": Mould plates for lengthwise mould types
- "F/P Cross": Mould plates for crosswise mould types
- "FB/P Blocks": Blocks for sliding core moulds 
- "FB/P Plates": Plates for sliding core moulds
- "FW Plates": Plates for change moulds
- "FW Parts": Parts for change moulds
- "FM Parts": Parts for micro moulds
- "H Parts": H 1000 Clamping system
- "E Parts": Components

NOTE: "E Parts" currently takes a considerable amount of time to run- up to 3 hours, as it contains atealst 2000+ parts (this can/will be optimized).

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



