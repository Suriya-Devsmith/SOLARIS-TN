import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/tamilnadu_solar_master.csv")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Create month
df["Month"] = df["Date"].dt.month

# Calculate district-month average
heatmap_data = df.pivot_table(
    values="ALLSKY_SFC_SW_DWN",
    index="District",
    columns="Month",
    aggfunc="mean"
)

print("\nDistrict × Month Solar Radiation:")
print(heatmap_data)

# Create heatmap
plt.figure(figsize=(14, 12))

plt.imshow(
    heatmap_data,
    aspect="auto"
)

plt.colorbar(
    label="Solar Radiation (kWh/m²/day)"
)

plt.xticks(
    range(12),
    [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]
)

plt.yticks(
    range(len(heatmap_data)),
    heatmap_data.index
)

plt.xlabel("Month")
plt.ylabel("District")
plt.title(
    "District-wise Monthly Solar Radiation Across Tamil Nadu"
)

plt.tight_layout()
plt.show()