import time
import requests
import json

# -------------------- Config --------------------
PROMETHEUS_URL = "http://your‑prometheus:9090/api/v1/query"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

# Thresholds (tune these!)
CPU_THRESHOLD = 80.0 # percent
MEM_THRESHOLD = 75.0 # percent
LATENCY_THRESHOLD = 0.5 # seconds (500 ms)
ERROR_RATE_THRESHOLD = 0.01 # 1 % error rate
QUERY_INTERVAL = 30 # seconds
# -------------------------------------------------

def prom_query(query):
 """Run a Prometheus instant query and return the first value."""
 resp = requests.get(PROMETHEUS_URL, params={"query": query})
 resp.raise_for_status()
 data = resp.json()
 if data != "success" or not data:
 return None
 # Assuming a single time‑series result
 return float(data)

def send_slack_alert(message):
 payload = {"text": message}
 requests.post(SLACK_WEBHOOK_URL, json=payload)

def check_metrics():
 alerts = []

 # 1️⃣ CPU usage (%)
 cpu_q = '100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"})))'
 cpu = prom_query(cpu_q)
 if cpu is not None and cpu > CPU_THRESHOLD:
 alerts.append(f"*CPU* usage high: {cpu:.1f}% (threshold {CPU_THRESHOLD}%)")

 # 2️⃣ Memory usage (%)
 mem_q = '100 * (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes'
 mem = prom_query(mem_q)
 if mem is not None and mem > MEM_THRESHOLD:
 alerts.append(f"*Memory* usage high: {mem:.1f}% (threshold {MEM_THRESHOLD}%)")

 # 3️⃣ Request latency (seconds) – 95th percentile
 latency_q = 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket)) by (le))'
 latency = prom_query(latency_q)
 if latency is not None and latency > LATENCY_THRESHOLD:
 alerts.append(f"*Latency* 95th‑pct: {latency:.3f}s (threshold {LATENCY_THRESHOLD}s)")

 # 4️⃣ Error rate (ratio)
 err_q = 'sum(rate(http_requests_total{status=~"5.."})) / sum(rate(http_requests_total))'
 err_rate = prom_query(err_q)
 if err_rate is not None and err_rate > ERROR_RATE_THRESHOLD:
 alerts.append(f"*Error rate* high: {err_rate:.2%} (threshold {ERROR_RATE_THRESHOLD:.2%})")

 # Send alert if anything crossed a threshold
 if alerts:
 alert_msg = "\n".join(alerts)
 send_slack_alert(f":warning: *SRE Alert*\n{alert_msg}")

if __name__ == "__main__":
 while True:
 try:
 check_metrics()
 except Exception as e:
 # You might want to alert on script failures as well
 send_slack_alert(f":x: Monitoring script error: {e}")
 time.sleep(QUERY_INTERVAL)
