import os
import time
import json
import requests
from splunklib import client as splunk_client
from splunklib import results as splunk_results

# ----- per‑application config -----
APPS = {
 "orders-service": {
 "search": """
 search index=orders sourcetype=order_logs (error OR exception)
 | table _time, host, error_code, error_message
 | sort -_time
 """,
 "token": os.getenv("TOKEN_ORDERS"), # Splunk token for this app
 "webhook": os.getenv("SLACK_WEBHOOK_ORDERS"),# Slack webhook (optional)
 },
 "billing-service": {
 "search": """
 search index=billing sourcetype=billing_logs (error OR failure)
 | table _time, host, err_code, err_msg
 | sort -_time
 """,
 "token": os.getenv("TOKEN_BILLING"),
 "webhook": os.getenv("SLACK_WEBHOOK_BILLING"),
 },
 # add more apps as needed …
}
POLL_INTERVAL = 300 # seconds
#connect sith token

def splunk_service(token: str) -> splunk_client.Service:
 # Minimal connection – host and port are still required
 return splunk_client.Service(
 host=os.getenv("SPLUNK_HOST", "splunk.example.com"),
 port=int(os.getenv("SPLUNK_PORT", 8089)),
 scheme="https",
 token=token # <-- this tells the SDK to use the token
 )
##Core loop – run each app’s query and push to Slack

def send_to_slack(webhook_url: str, text: str):
 payload = {"text": text}
 requests.post(webhook_url, json=payload).raise_for_status()

def fetch_errors(svc: splunk_client.Service, query: str):
 job = svc.jobs.create(query,
 exec_mode="normal",
 earliest_time="-5m",
 latest_time="now")
 while not job.is_done():
 time.sleep(0.5)

 events = []
 for result in splunk_results.ResultsReader(job.results()):
 if isinstance(result, dict):
 events.append(result)
 return events

def main():
 while True:
 for app_name, cfg in APPS.items():
 try:
 svc = splunk_service(cfg)
 errors = fetch_errors(svc, cfg)

 if not errors:
 continue

 lines = []
 for ev in errors:
 ts = ev.get("_time", "N/A")
 host = ev.get("host", "unknown")
 code = ev.get("error_code") or ev.get("err_code", "N/A")
 msg = ev.get("error_message") or ev.get("err_msg", "N/A")
 lines.append(f"`{host}` – *{code}*: {msg}")

 slack_msg = f"*⚠️ {app_name} recent errors*:\n" + "\n".join(lines)
 webhook = cfg.get("webhook")
 if webhook:
 send_to_slack(webhook, slack_msg)
 else:
 print(f" No webhook configured – printed locally")
 print(slack_msg)

 except Exception as exc:
 # Log but keep the loop alive
 print(f"Error processing {app_name}: {exc}")

 time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
 main()
