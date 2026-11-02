import requests
import pandas as pd

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M,PRECTOTCORR,WS10M",
    "community": "RE",
    "longitude": 79.0747,
    "latitude": 12.2253,
    "start": "20010101",
    "end": "20250712",
    "format": "JSON"
}

print("Downloading Tiruvannamalai...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

df = pd.DataFrame(data["properties"]["parameter"])

df.index.name = "Date"
df.reset_index(inplace=True)

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%Y%m%d"
)

df["District"] = "Tiruvannamalai"
df["Latitude"] = 12.2253
df["Longitude"] = 79.0747

df = df[
    [
        "Date",
        "District",
        "Latitude",
        "Longitude",
        "ALLSKY_SFC_SW_DWN",
        "T2M",
        "RH2M",
        "PRECTOTCORR",
        "WS10M"
    ]
]

# Load existing master dataset
master_file = "data/tamilnadu_solar_master.csv"

master = pd.read_csv(master_file)

master["Date"] = pd.to_datetime(master["Date"])

# Add Tiruvannamalai
master = pd.concat(
    [master, df],
    ignore_index=True
)

# Sort
master = master.sort_values(
    ["District", "Date"]
)

# Save
master.to_csv(
    master_file,
    index=False
)

print("===================================")
print("Tiruvannamalai added successfully!")
print("===================================")
print("Total records:", len(master))
print("Total districts:", master["District"].nunique())
print("Saved to:", master_file)