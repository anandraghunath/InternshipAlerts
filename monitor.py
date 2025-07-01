import os
import smtplib
import requests
import difflib
from email.mime.text import MIMEText
import datetime
from zoneinfo import ZoneInfo 

# Config
REPO_RAW_URL = "https://raw.githubusercontent.com/vanshb03/Summer2026-Internships/main/README.md"
STORED_FILE = "last_readme.md"

EMAIL_ADDRESS = os.getenv("FROM_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("FROM_EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL_ADDRESS")  # you can change this if needed

def fetch_readme():
    response = requests.get(REPO_RAW_URL)
    response.raise_for_status()
    return response.text

def send_push():

    requests.post("https://ntfy.sh/anand_intern_alerts",
    data="New internship listing found: https://github.com/vanshb03/Summer2026-Internships".encode(encoding='utf-8'))

def check_for_updates():
    latest = fetch_readme()

    if not os.path.exists(STORED_FILE):
        with open(STORED_FILE, "w", encoding="utf-8") as f:
            f.write(latest)
        print("First run: stored current README.")
        return

    with open(STORED_FILE, "r", encoding="utf-8") as f:
        previous = f.read()

    if latest != previous:
        diff = difflib.unified_diff(
            previous.splitlines(), latest.splitlines(), lineterm=""
        )
        new_lines = [line[1:] for line in diff if line.startswith("+") and not line.startswith("+++")]
        body = (
            "New internship listing(s) added:\n\n"
            + "\n".join(new_lines)
            + "\n\nView them here: https://github.com/vanshb03/Summer2026-Internships"
        )
        send_push()
        print("Change detected and email sent.")
        with open(STORED_FILE, "w", encoding="utf-8") as f:
            f.write(latest)
    else:
        print("No changes detected.")

def send_test_email():
    send_push()
    print("Test email sent!")

if __name__ == "__main__":
    #send_test_email()  # Uncomment to send a test email
    check_for_updates()
