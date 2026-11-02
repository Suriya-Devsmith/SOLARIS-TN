import requests
import pandas as pd
import time
import os

# NASA POWER API
BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Parameters we need
PARAMETERS = "ALLSKY_SFC_SW_DWN,T2M,RH2M,PRECTOTCORR,WS10M"

# Tamil Nadu district headquarters / representative coordinates
districts = {
    "Ariyalur": (11.1401, 79.0786),
    "Chengalpattu": (12.6819, 79.9671),
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Cuddalore": (11.7480, 79.7714),
    "Dharmapuri": (12.1211, 78.1582),
    "Dindigul": (10.3673, 77.9803),
    "Erode": (11.3410, 77.7172),
    "Kallakurichi": (11.7404, 78.9597),
    "Kancheepuram": (12.8342, 79.7036),
    "Karur": (10.9601, 78.0766),
    "Krishnagiri": (12.5186, 78.2137),
    "Madurai": (9.9252, 78.1198),
    "Mayiladuthurai": (11.1035, 79.6550),
    "Nagapattinam": (10.7672, 79.8449),
    "Namakkal": (11.2194, 78.1677),
    "Nilgiris": (11.4102, 76.6950),
    "Perambalur": (11.2320, 78.8800),
    "Pudukkottai": (10.3797, 78.8208),
    "Ramanathapuram": (9.3639, 78.8395),
    "Ranipet": (12.9249, 79.3333),
    "Salem": (11.6643, 78.1460),
    "Sivaganga": (9.8433, 78.4809),
    "Tenkasi": (8.9590, 77.3152),
    "Thanjavur": (10.7870, 79.1378),
    "Theni": (10.0104, 77.4768),
    "Thoothukudi": (8.7642, 78.1348),
    "Tiruchirappalli": (10.7905, 78.7047),
    "Tirunelveli": (8.7139, 77.7567),
    "Tirupathur": (12.4966, 78.5733),
    "Tiruppur": (11.1085, 77.3411),
    "Tiruvallur": (13.1439, 79.9081),
    "Tiruvarur": (10.7725, 79.6368),
    "Vellore": (12.9165, 79.1325),
    "Viluppuram": (11.9401, 79.4861),
    "Virudhunagar": (9.5851, 77.9579),
    "Kanyakumari": (8.0883, 77.5385),
    "Kallakurichi": (11.7404, 78.9597)
}

# Remove duplicate district
districts = dict(districts)

# Dates
START_DATE = "20010101"
END_DATE = "20250712"

# Output folder
os.makedirs("data", exist_ok=True)

all_data = []

for district, (latitude, longitude) in districts.items():

    print(f"\nDownloading: {district}")

    params = {
        "parameters": PARAMETERS,
        "community": "RE",
        "longitude": longitude,
        "latitude": latitude,
        "start": START_DATE,
        "end": END_DATE,
        "format": "JSON"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        # Extract NASA POWER data
        properties = data["properties"]
        parameter_data = properties["parameter"]

        # Convert dictionary to DataFrame
        df = pd.DataFrame(parameter_data)

        # Date is stored as index
        df.index.name = "Date"
        df.reset_index(inplace=True)

        # Convert NASA date format YYYYMMDD
        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%Y%m%d"
        )

        # Add district information
        df["District"] = district
        df["Latitude"] = latitude
        df["Longitude"] = longitude

        # Reorder columns
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

        all_data.append(df)

        print(
            f"✓ {district} downloaded "
            f"({len(df)} records)"
        )

    except Exception as e:
        print(f"✗ Error downloading {district}: {e}")

    # Small delay to avoid sending requests too quickly
    time.sleep(2)


# Combine all districts
if all_data:

    final_df = pd.concat(
        all_data,
        ignore_index=True
    )

    # Sort
    final_df = final_df.sort_values(
        ["District", "Date"]
    )

    # Save master dataset
    output_file = "data/tamilnadu_solar_master.csv"

    final_df.to_csv(
        output_file,
        index=False
    )

    print("\n===================================")
    print("🎉 DOWNLOAD COMPLETED!")
    print("===================================")

    print(f"Total records: {len(final_df)}")
    print(f"Total districts: {final_df['District'].nunique()}")
    print(f"Saved to: {output_file}")

    print("\nColumns:")
    print(final_df.columns.tolist())

else:

    print("\nNo data was downloaded.")