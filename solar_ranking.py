import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/tamilnadu_solar_master.csv")

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Solar radiation column
solar = "ALLSKY_SFC_SW_DWN"

# District statistics
ranking = df.groupby("District")[solar].agg(
    Average_Solar="mean",
    Solar_Std="std",
    Minimum_Solar="min",
    Maximum_Solar="max"
)

# Coefficient of Variation
ranking["CV"] = (
    ranking["Solar_Std"] / ranking["Average_Solar"]
) * 100

# Percentage of days with solar radiation >= 5
good_days = (
    df.groupby("District")[solar]
    .apply(lambda x: (x >= 5).mean() * 100)
)

ranking["Good_Solar_Days_%"] = good_days

# Normalize average solar radiation
solar_min = ranking["Average_Solar"].min()
solar_max = ranking["Average_Solar"].max()

ranking["Solar_Score"] = (
    (ranking["Average_Solar"] - solar_min)
    / (solar_max - solar_min)
) * 100

# Normalize consistency
cv_min = ranking["CV"].min()
cv_max = ranking["CV"].max()

ranking["Consistency_Score"] = (
    (cv_max - ranking["CV"])
    / (cv_max - cv_min)
) * 100

# Final Solar Potential Score
ranking["Solar_Potential_Score"] = (
    0.70 * ranking["Solar_Score"]
    + 0.30 * ranking["Consistency_Score"]
)

# Sort
ranking = ranking.sort_values(
    "Solar_Potential_Score",
    ascending=False
)

# Round values
print("\n========== SOLAR DISTRICT RANKING ==========\n")

print(
    ranking[
        [
            "Average_Solar",
            "CV",
            "Good_Solar_Days_%",
            "Solar_Potential_Score"
        ]
    ].round(2)
)

# Save ranking
ranking.to_csv(
    "data/solar_district_ranking.csv"
)

# Top 10 districts
top10 = ranking.head(10)

print("\n========== TOP 10 DISTRICTS ==========\n")

print(
    top10[
        [
            "Average_Solar",
            "CV",
            "Good_Solar_Days_%",
            "Solar_Potential_Score"
        ]
    ].round(2)
)

# Plot top 10
plt.figure(figsize=(10, 6))

plt.barh(
    top10.index[::-1],
    top10["Solar_Potential_Score"][::-1]
)

plt.xlabel("Solar Potential Score")
plt.ylabel("District")
plt.title("Top 10 Solar Potential Districts in Tamil Nadu")

plt.tight_layout()
plt.show()