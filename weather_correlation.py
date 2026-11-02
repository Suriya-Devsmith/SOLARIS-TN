
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Loading SOLARIS-TN dataset...")

df = pd.read_csv("data/tamilnadu_solar_master.csv")

# Select weather and solar parameters
columns = [
    "ALLSKY_SFC_SW_DWN",
    "T2M",
    "RH2M",
    "PRECTOTCORR",
    "WS10M"
]

data = df[columns]

# Calculate correlation matrix
correlation = data.corr()

print("\nWEATHER CORRELATION MATRIX")
print(correlation.round(3))

# Correlation with solar radiation
solar_correlation = (
    correlation["ALLSKY_SFC_SW_DWN"]
    .drop("ALLSKY_SFC_SW_DWN")
    .sort_values(ascending=False)
)

print("\nCORRELATION WITH SOLAR RADIATION")
print(solar_correlation.round(3))

# Save correlation results
correlation.to_csv("data/weather_correlation_matrix.csv")
solar_correlation.to_csv("data/solar_weather_correlation.csv")

# Draw correlation heatmap
plt.figure(figsize=(10, 7))

plt.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)

plt.colorbar(label="Correlation coefficient")

labels = [
    "Solar Radiation",
    "Temperature",
    "Humidity",
    "Rainfall",
    "Wind Speed"
]

plt.xticks(range(len(labels)), labels, rotation=30, ha="right")
plt.yticks(range(len(labels)), labels)

for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(
            j, i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.title("Weather and Solar Radiation Correlation – Tamil Nadu")
plt.tight_layout()

plt.savefig("data/weather_correlation_heatmap.png", dpi=300)
plt.show()

# Individual scatter plots
weather_columns = ["T2M", "RH2M", "PRECTOTCORR", "WS10M"]
titles = ["Temperature", "Relative Humidity", "Rainfall", "Wind Speed"]

for column, title in zip(weather_columns, titles):
    plt.figure(figsize=(8, 5))

    plt.scatter(
        df[column],
        df["ALLSKY_SFC_SW_DWN"],
        alpha=0.15,
        s=5
    )

    plt.xlabel(title)
    plt.ylabel("Solar Radiation")
    plt.title(f"{title} vs Solar Radiation")
    plt.tight_layout()

    filename = f"data/{column}_solar_scatter.png"
    plt.savefig(filename, dpi=300)
    plt.show()

print("\nWEATHER CORRELATION ANALYSIS COMPLETED!")
print("Total records analysed:", len(df))
print("Files saved in data folder.")
