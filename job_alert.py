import feedparser
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL")

cities = ["Hyderabad", "Chennai", "Bangalore", "Remote"]
keyword = "Data Analyst Intern"

SENT_FILE = "sent_jobs.txt"

def get_sent_jobs():
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_sent_jobs(sent_jobs):
    with open(SENT_FILE, "w") as f:
        for job in sent_jobs:
            f.write(job + "\n")

def fetch_jobs():
    sent_jobs = get_sent_jobs()
    new_jobs = []
    updated_sent_jobs = set(sent_jobs)

    for city in cities:
        url = f"https://in.indeed.com/rss?q={keyword.replace(' ', '+')}&l={city.replace(' ', '+')}"
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            if entry.link not in sent_jobs:
                job = f"""
Title: {entry.title}
Company: {entry.author}
Location: {city}
Apply Here: {entry.link}
----------------------------------------
"""
                new_jobs.append(job)
                updated_sent_jobs.add(entry.link)

    save_sent_jobs(updated_sent_jobs)
    return new_jobs

def send_email(content):
    subject = f"New Data Analyst Intern Jobs - {datetime.now().date()}"
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())

if __name__ == "__main__":
    jobs = fetch_jobs()

    if jobs:
        email_content = "\n".join(jobs)
        send_email(email_content)
        print("New jobs sent successfully!")
    else:
        print("No new jobs today.")
