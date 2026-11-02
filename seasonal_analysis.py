import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/tamilnadu_solar_master.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# Get month
df["Month"] = df["Date"].dt.month

# Create seasons
def get_season(month):
    if month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    elif month in [10, 11]:
        return "Post-Monsoon"
    else:
        return "Winter"

df["Season"] = df["Month"].apply(get_season)

# Set order
season_order = [
    "Summer",
    "Monsoon",
    "Post-Monsoon",
    "Winter"
]

# Calculate average solar radiation
seasonal_solar = (
    df.groupby("Season")["ALLSKY_SFC_SW_DWN"]
    .mean()
    .reindex(season_order)
)

print("\n========== SEASONAL SOLAR RADIATION ==========\n")
print(seasonal_solar.round(3))

# Find highest and lowest season
highest = seasonal_solar.idxmax()
lowest = seasonal_solar.idxmin()

print("\nHighest solar season:", highest)
print("Lowest solar season:", lowest)

# Plot
plt.figure(figsize=(9, 6))

plt.bar(
    seasonal_solar.index,
    seasonal_solar.values
)

plt.xlabel("Season")
plt.ylabel("Average Solar Radiation (kWh/m²/day)")
plt.title("Seasonal Solar Radiation Across Tamil Nadu")

plt.tight_layout()
plt.show()