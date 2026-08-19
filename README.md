# 🌐 Global 3D Job Tracker & Intelligence Dashboard

> Built for the **Into the Scrape-Verse** Hackathon (WeMakeDevs & Bright Data Collaboration).

A native desktop intelligence dashboard built with Python and CustomTkinter that aggregates, structures, and visualizes global job openings for 3D Artists, Technical Artists, and 3D Generalists using custom web data powered by **Bright Data Scraper Studio**.

---

## 🚀 Project Overview
Finding specialized roles in the 3D graphics and gaming industry often requires navigating fragmented portals. This project provides a streamlined desktop application that triggers targeted custom web scrapers, handles structured datasets (JSON, CSV, Excel), and renders interactive job cards equipped with direct application routing.

---

## ✨ Key Features
* **Custom Scraper Integration:** Connects seamlessly with Bright Data Scraper Studio via API to trigger targeted job extraction on LinkedIn.
* **Self-Healing Architecture:** Utilizes Bright Data's robust infrastructure to automatically adapt and self-heal when target website layouts shift, ensuring uninterrupted data pipelines.
* **Modern Desktop GUI:** Built with **CustomTkinter** for a clean, responsive, and dark-mode-optimized native user experience.
* **Multi-Format Dataset Support:** Instantly parse and render structured outputs from `.json`, `.ndjson`, `.csv`, `.xlsx`, and `.xls` files using the built-in file uploader.
* **Direct Application Routing:** Each rendered job card displays key attributes (location, salary, required software skills, experience level) and an **"Apply / View Job"** button that opens listings directly in your browser.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **GUI Framework:** CustomTkinter
* **Data Extraction:** Bright Data Scraper Studio & Datasets API (`requests`)
* **Data Processing:** Pandas, CSV, JSON

---

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/sudhakar6896/scrape-verse-3d-job-tracker.git](https://github.com/sudhakar6896/scrape-verse-3d-job-tracker.git)
   cd scrape-verse-3d-job-tracker

Install required dependencies:

Bash
pip install customtkinter requests pandas openpyxl
Configure your API Token:
Open scrapper.py and replace the placeholder string with your Bright Data API token:

Python
self.api_token = "YOUR_API_TOKEN"
Run the Application:

Python
python scrapper.py
📱 How to Use
Trigger Search: Enter your target job keyword (e.g., 3D Artist) and location, then click "Trigger Scraper" to dispatch the task to your Bright Data collector.

View Results: Download your processed snapshot dataset from the Bright Data dashboard, click "Upload Results", and instantly view your structured job intelligence cards!

---
