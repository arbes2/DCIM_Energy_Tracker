import pandas as pd
import numpy as np
import datetime
import time

# Configuration
racks = ["Rack1", "Rack2", "Rack3", "Rack4"]
records = []

# Simulate data for each rack
for i in range(50):  # 50 time points
    timestamp = datetime.datetime.now() + datetime.timedelta(seconds=i*10)
    for rack in racks:
        power = np.random.randint(200, 500)  # Random power usage in Watts
        records.append([timestamp, rack, power])

# Convert to DataFrame
df = pd.DataFrame(records, columns=["timestamp", "rack_id", "power_watts"])

# Save to CSV
df.to_csv("rack_data.csv", index=False)
print("Simulated rack data saved to rack_data.csv")
