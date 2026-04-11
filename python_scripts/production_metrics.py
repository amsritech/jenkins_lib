import time
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -------------------- Config --------------------
PROMETHEUS_URL = "http://your-prometheus:9090/api/v1/query"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"

CPU_THRESHOLD = 80.0
MEM_THRESHOLD = 75.0
LATENCY_THRESHOLD = 0.5
ERROR_RATE_THRESHOLD = 0.01

QUERY_INTERVAL = 30
ALERT_COOLDOWN = 300  # 5 min cooldown
# -------------------------------------------------

# -------------------- Logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------- HTTP Session --------------------
session = requests.Session()
retries = Retry(total=3, backoff_factor=1)
session.mount("http://", HTTPAdapter(max_retries=retries))


# -------------------- Alert State --------------------
last_alert_time = {}


def should_alert(metric_key):
    now = time.time()
    if metric_key not in last_alert_time or now - last_alert_time[metric_key] > ALERT_COOLDOWN:
        last_alert_time[metric_key] = now
        return True
    return False


# -------------------- Prometheus Query --------------------
def prom_query(query):
    try:
        resp = session.get(PROMETHEUS_URL, params={"query": query}, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "success":
            logging.error("Prometheus query failed")
            return []

        return data.get("data", {}).get("result", [])

    except Exception as e:
        logging.error(f"Prometheus query error: {e}")
        return []


# -------------------- Slack Alert --------------------
def send_slack_alert(message, severity="warning"):
    emoji = ":warning:" if severity == "warning" else ":rotating_light:"
    payload = {
        "text": f"{emoji} *SRE Alert ({severity.upper()})*\n{message}"
    }

    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Slack alert failed: {e}")


# -------------------- Metric Checks --------------------
def check_cpu():
    alerts = []
    query = '100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))'
    results = prom_query(query)

    for r in results:
        instance = r["metric"].get("instance", "unknown")
        value = float(r["value"][1])

        logging.info(f"CPU {instance}: {value:.2f}%")

        if value > CPU_THRESHOLD and should_alert(f"cpu_{instance}"):
            alerts.append(f"{instance} CPU high: {value:.1f}%")

    return alerts


def check_memory():
    alerts = []
    query = '100 * (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes'
    results = prom_query(query)

    for r in results:
        instance = r["metric"].get("instance", "unknown")
        value = float(r["value"][1])

        logging.info(f"Memory {instance}: {value:.2f}%")

        if value > MEM_THRESHOLD and should_alert(f"mem_{instance}"):
            alerts.append(f"{instance} Memory high: {value:.1f}%")

    return alerts


def check_latency():
    alerts = []
    query = 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))'
    results = prom_query(query)

    for r in results:
        value = float(r["value"][1])

        logging.info(f"Latency: {value:.3f}s")

        if value > LATENCY_THRESHOLD and should_alert("latency"):
            alerts.append(f"Latency high: {value:.3f}s")

    return alerts


def check_error_rate():
    alerts = []
    query = 'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'
    results = prom_query(query)

    for r in results:
        value = float(r["value"][1])

        logging.info(f"Error rate: {value:.4f}")

        if value > ERROR_RATE_THRESHOLD and should_alert("error_rate"):
            alerts.append(f"Error rate high: {value:.2%}")

    return alerts


# -------------------- Main Check --------------------
def check_metrics():
    alerts = []

    alerts.extend(check_cpu())
    alerts.extend(check_memory())
    alerts.extend(check_latency())
    alerts.extend(check_error_rate())

    if alerts:
        message = "\n".join(alerts)
        send_slack_alert(message, severity="critical")


# -------------------- Main Loop --------------------
if __name__ == "__main__":
    logging.info("Starting monitoring script...")

    while True:
        try:
            check_metrics()
        except Exception as e:
            logging.error(f"Monitoring script error: {e}")
            send_slack_alert(f"Script failure: {e}", severity="critical")

        time.sleep(QUERY_INTERVAL)