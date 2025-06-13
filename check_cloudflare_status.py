import requests
import feedparser

# -------- Deduplication Helpers --------

def load_reported_ids(filename="reported_incidents.txt"):
    try:
        with open(filename, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_reported_id(incident_id, filename="reported_incidents.txt"):
    with open(filename, "a") as f:
        f.write(f"{incident_id}\n")

# -------- Teams Notification --------

def send_to_teams(message, webhook_url):
    payload = {
        "text": message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print("Message sent to Teams!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# -------- Providers --------

def check_cloudflare(webhook_url, reported_ids):
    url = "https://www.cloudflarestatus.com/api/v2/summary.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"Error fetching Cloudflare status: {e}")
        return

    new_alert = False
    if data['incidents']:
        for incident in data['incidents']:
            incident_id = "cloudflare_" + incident['id']
            if incident_id not in reported_ids:
                message = "🚨 Cloudflare incident detected:\n"
                message += f"- {incident['name']} (Status: {incident['status']}, Impact: {incident['impact']})\n"
                message += f"  Link: {incident['shortlink']}\n"
                send_to_teams(message, webhook_url)
                save_reported_id(incident_id)
                new_alert = True
    if not new_alert:
        print("No new Cloudflare incidents. Not sending message.")

def check_google_cloud(webhook_url, reported_ids):
    url = "https://status.cloud.google.com/incidents.json"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"Error fetching Google Cloud status: {e}")
        return

    ongoing_incidents = [i for i in data if i['end'] is None]

    new_alert = False
    for incident in ongoing_incidents:
        incident_id = "google_" + str(incident['number'])
        if incident_id not in reported_ids:
            message = "🚨 Google Cloud incident detected:\n"
            message += f"- {incident['number']} | {incident['service_name']} | {incident['external_desc'].strip()}\n"
            message += f"  Begin: {incident['begin']} | Link: {incident['url']}\n"
            send_to_teams(message, webhook_url)
            save_reported_id(incident_id)
            new_alert = True
    if not new_alert:
        print("No new Google Cloud incidents. Not sending message.")

def check_aws(webhook_url, reported_ids):
    url = "https://status.aws.amazon.com/rss/all.rss"
    feed = feedparser.parse(url)

    new_alert = False
    for entry in feed.entries[:5]:  # Check the latest 5 entries
        incident_id = "aws_" + entry.title + entry.published
        if "service is operating normally" not in entry.title.lower() and incident_id not in reported_ids:
            message = "🚨 AWS incident detected:\n"
            message += f"- {entry.title}\n  Published: {entry.published}\n  {entry.summary}\n  Link: {entry.link}\n"
            send_to_teams(message, webhook_url)
            save_reported_id(incident_id)
            new_alert = True
    if not new_alert:
        print("No new AWS incidents. Not sending message.")

def check_azure(webhook_url, reported_ids):
    url = "https://status.azure.com/en-us/status/feed/"
    feed = feedparser.parse(url)

    new_alert = False
    for entry in feed.entries[:5]:
        incident_id = "azure_" + entry.title + entry.published
        if ("resolved" not in entry.title.lower() and
            "is now healthy" not in entry.title.lower() and
            incident_id not in reported_ids):
            message = "🚨 Microsoft Azure incident detected:\n"
            message += f"- {entry.title}\n  Published: {entry.published}\n  {entry.summary}\n  Link: {entry.link}\n"
            send_to_teams(message, webhook_url)
            save_reported_id(incident_id)
            new_alert = True
    if not new_alert:
        print("No new Azure incidents. Not sending message.")

# -------- Main --------

if __name__ == "__main__":
    webhook_url = "YOUR_WEBHOOK_URL_HERE"  # <-- replace with your Teams webhook
    reported_ids = load_reported_ids()

    check_cloudflare(webhook_url, reported_ids)
    check_google_cloud(webhook_url, reported_ids)
    check_aws(webhook_url, reported_ids)
    check_azure(webhook_url, reported_ids)
