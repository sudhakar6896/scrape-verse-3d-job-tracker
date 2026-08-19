import customtkinter as ctk
import requests
import webbrowser
from tkinter import filedialog
import json
import csv
import pandas as pd

# Set up the CustomTkinter appearance theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class JobDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("3D Artist Job Intelligence Dashboard")
        self.geometry("1050x750")

        self.api_token = "b5648e1096c6442f60a6c4bbbe73f8d2234d3d8324554bd6a7ec8f3f251f07df"  # Your token

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Global 3D Job Tracker", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(pady=15)

        # Search Control Frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=20, pady=10)

        self.search_input = ctk.CTkEntry(self.search_frame, width=260,
                                         placeholder_text="e.g., 3D Artist, Technical Artist...")
        self.search_input.pack(side="left", padx=10, pady=10)

        self.location_input = ctk.CTkEntry(self.search_frame, width=170, placeholder_text="Location...")
        self.location_input.pack(side="left", padx=10, pady=10)

        self.search_btn = ctk.CTkButton(self.search_frame, text="Trigger Scraper", width=140,
                                        command=self.trigger_scraper)
        self.search_btn.pack(side="left", padx=8, pady=10)

        self.upload_btn = ctk.CTkButton(self.search_frame, text="Upload Results", width=140, fg_color="purple",
                                        hover_color="darkmagenta", command=self.upload_file)
        self.upload_btn.pack(side="left", padx=8, pady=10)

        # Results Display Container (Scrollable Frame)
        self.results_container = ctk.CTkScrollableFrame(self, width=980, height=500)
        self.results_container.pack(padx=20, pady=10, fill="both", expand=True)

        self.show_message(
            "Trigger a scraper to send tasks to Bright Data, or click 'Upload Results' to open your downloaded JSON, CSV, or XLSX dataset.")

    def trigger_scraper(self):
        keyword = self.search_input.get()
        location_query = self.location_input.get()

        if not keyword:
            self.show_message("Please enter at least a job keyword.")
            return

        for widget in self.results_container.winfo_children():
            widget.destroy()

        loading = ctk.CTkLabel(self.results_container, text=f"Triggering scraper for '{keyword}'...",
                               font=ctk.CTkFont(size=14))
        loading.pack(pady=40)
        self.update()

        try:
            url = "https://api.brightdata.com/dca/trigger"
            headers = {
                "Authorization": f"Bearer 2ca976e5-89b6-45a8-89c9-3566adffe80c",
                "Content-Type": "application/json",
            }
            params = {
                "collector": "c_msyy3x4u2o1crnhdgf",
                "queue_next": "1",
            }
            data = [
                {
                    "job_titles": [keyword],
                    "location": location_query if location_query else "Global",
                    "url": "https://www.linkedin.com/jobs/",
                    "current_job_title_index": 0
                }
            ]

            response = requests.post(url, headers=headers, params=params, json=data)
            loading.destroy()

            if response.status_code == 200:
                res_data = response.json()
                collection_id = res_data.get("collection_id")
                self.show_message(
                    f"Scraper Triggered Successfully!\n\nCollection ID: {collection_id}\n\nYour task is running on Bright Data. You can download your snapshot from the dashboard and click 'Upload Results' to display them.")
            else:
                self.show_message(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
            loading.destroy()
            self.show_message(f"Connection Error: {str(e)}")

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Dataset File",
            filetypes=[("All Supported Files", "*.json *.csv *.ndjson *.xlsx *.xls"), ("JSON Files", "*.json *.ndjson"),
                       ("CSV/Excel Files", "*.csv *.xlsx *.xls")]
        )
        if not file_path:
            return

        for widget in self.results_container.winfo_children():
            widget.destroy()

        try:
            jobs = []
            if file_path.endswith('.csv'):
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    jobs = [row for row in reader]
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
                jobs = df.to_dict(orient='records')
            else:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    content = f.read().strip()
                    for line in content.split('\n'):
                        if line.strip():
                            try:
                                jobs.append(json.loads(line))
                            except:
                                jobs = json.loads(content)
                                break

            if not jobs:
                self.show_message("The selected file is empty or formatted incorrectly.")
                return

            for job in jobs:
                self.create_job_card(job)

        except Exception as e:
            self.show_message(f"Error reading file: {str(e)}")

    def create_job_card(self, job):
        card = ctk.CTkFrame(self.results_container, fg_color=("gray90", "gray16"))
        card.pack(fill="x", padx=10, pady=8, ipadx=10, ipady=10)

        title = job.get('job_title', 'N/A')
        company = job.get('company_name', 'N/Y')
        title_lbl = ctk.CTkLabel(card, text=f"{title} — {company}", font=ctk.CTkFont(size=16, weight="bold"))
        title_lbl.pack(anchor="w", padx=10, pady=2)

        loc = job.get('location', 'N/A')
        salary = job.get('salary_range', 'Not Specified')
        skills = job.get('required_software_skills', 'N/A')
        exp = job.get('experience_level', 'N/A')
        j_type = job.get('job_type', 'N/A')

        details_text = (
            f"📍 Location: {loc}   |   💰 Salary: {salary}\n"
            f"🛠️ Skills: {skills}\n"
            f"📈 Experience: {exp}   |   💼 Type: {j_type}"
        )
        details_lbl = ctk.CTkLabel(card, text=details_text, justify="left", font=ctk.CTkFont(size=12))
        details_lbl.pack(anchor="w", padx=10, pady=4)

        url = job.get('job_url', '')
        if url and url != 'N/A':
            btn = ctk.CTkButton(card, text="Apply / View Job", width=140, height=28,
                                command=lambda u=url: webbrowser.open(u))
            btn.pack(anchor="e", padx=10, pady=5)

    def show_message(self, message):
        for widget in self.results_container.winfo_children():
            widget.destroy()
        lbl = ctk.CTkLabel(self.results_container, text=message, font=ctk.CTkFont(size=14), justify="center")
        lbl.pack(pady=40)


if __name__ == "__main__":
    app = JobDashboard()
    app.mainloop()