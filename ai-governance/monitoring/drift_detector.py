from prometheus_client import Gauge, start_http_server
import numpy as np
from scipy.stats import ks_2samp
import time
import os

# Chemin vers le fichier baseline
BASELINE_PATH = os.getenv('BASELINE_PATH', '/data/baseline_feature.npy')

if os.path.exists(BASELINE_PATH):
    BASELINE = np.load(BASELINE_PATH)
else:
    BASELINE = np.random.normal(0, 1, 1024)

# Gauge Prometheus
g_drift = Gauge('model_input_drift_pvalue', 'KS p-value for feature drift')

# Start Prometheus metrics server
start_http_server(9000)
print("Prometheus metrics server started on port 9000")

while True:
    # In prod, pull recent batch of input features from metric store / Kinesis / Kafka
    sample = np.random.normal(0, 1, 256)
    
    # KS test
    stat, p = ks_2samp(BASELINE, sample)
    
    # Set Prometheus metric
    g_drift.set(p)
    
    if p < 0.01:
        print(f'Drift detected, p={p}')
        # TODO: push an alert to Alertmanager or SIEM via webhook
    
    time.sleep(30)
