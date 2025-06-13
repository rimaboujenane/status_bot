# Cloud Service Status Alert Bot ☁️🚨

A simple Python bot that monitors service status pages for **Cloudflare, Google Cloud, AWS, and Microsoft Azure**, and automatically sends notifications to a Microsoft Teams channel when incidents occur.

## ✨ Features

* Checks provider status pages automatically every 10 minutes.
* Sends real-time alerts to Microsoft Teams via webhook.
* Avoids duplicate alerts by tracking already-reported incidents.
* Easy to extend with additional cloud providers.

## ⚙️ Installation

### 1. Clone the repository:

```bash
git clone https://github.com/rimaboujenane/status_bot.git
cd status_bot
```

### 2. Create a Python virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Configuration

* Replace the placeholder webhook URL in the script (`YOUR_WEBHOOK_URL_HERE`) with your actual Teams webhook URL.

## 🚀 Running the Bot Manually

```bash
python check_cloudflare_status.py
```

## ⏰ Scheduling Automated Runs (Mac/Linux)

Use cron to schedule the script to run automatically every 10 minutes:

```bash
crontab -e
```

Then add this line (replace paths with your own):

```cron
*/10 * * * * /full/path/to/myenv/bin/python /full/path/to/status_bot/check_cloudflare_status.py >> /full/path/to/status_bot/bot.log 2>&1
```

## 📁 Project Structure

```
status_bot/
├── check_cloudflare_status.py  # main script
├── reported_incidents.txt      # stores previously reported incidents
├── requirements.txt            # Python dependencies
└── bot.log                     # cron job output log (generated automatically)
```

## 🛠 Dependencies

* `requests`
* `feedparser`


