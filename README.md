# IMT 542 - I4: Easy to Access

**Assignment:** I4 Easy to Access - Find 3 different information structures with different access technologies  
**Course:** IMT 542 A Sp 26 - Portable Information Structures  
**Author:** Sneha

---

## Overview

This notebook demonstrates three different ways to access information structures using Python. Each function fetches data using a different access technology and prints a sample of the output. Comments in the code explain the pros and cons of each approach.

| # | Information Structure | Access Technology | Data Source |
|---|----------------------|-------------------|-------------|
| 1 | JSON | REST API over HTTP | Open-Meteo weather API (no key needed) |
| 2 | CSV | HTTP file download | US state population dataset (GitHub) |
| 3 | HTML | Web scraping (BeautifulSoup) | Wikipedia table |

---

## How to Run

### Option 1: Google Colab (Recommended)

1. Click the **"Open in Colab"** badge at the top of the notebook
2. Go to **Runtime > Run all**
3. No setup needed - all libraries are pre-installed in Colab

### Option 2: Run Locally

1. Clone this repo: `git clone https://github.com/Sneha-8/IMT-547-A.git`
2. Install dependencies: `pip install requests beautifulsoup4`
3. Open and run the notebook: `jupyter notebook I4_Easy_to_Access.ipynb`

---

## Dependencies

- `requests` - for HTTP API calls and file downloads
- `beautifulsoup4` - for HTML parsing
- `csv`, `io` - Python standard library (no install needed)

All dependencies are pre-installed in Google Colab. No API keys required - all data sources are free and public.
