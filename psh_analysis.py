
import pandas as pd
import matplotlib.pyplot as plt

print("Loading SOLARIS-TN dataset...")

df = pd.read_csv("data/tamilnadu_solar_master.csv")

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Convert daily solar radiation into Peak Sun Hours
df["PSH"] = df["ALLSKY_SFC_SW_DWN"]

# Extract month
df["Month"] = df["Date"].dt.month

# -----------------------------------
# 1. DISTRICT-WISE AVERAGE PSH
# -----------------------------------

district_psh = (
    df.groupby("District")["PSH"]
    .mean()
    .sort_values(ascending=False)
)

district_psh = district_psh.reset_index()
district_psh.columns = ["District", "Average_PSH"]

district_psh.to_csv(
    "data/district_average_psh.csv",
    index=False
)

print("\nDISTRICT-WISE AVERAGE PSH")
print(district_psh.to_string(index=False))

# -----------------------------------
# 2. MONTHLY AVERAGE PSH
# -----------------------------------

monthly_psh = df.groupby("Month")["PSH"].mean()

month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly_psh.index = month_names

monthly_psh.to_csv(
    "data/monthly_average_psh.csv",
    header=["Average_PSH"]
)

print("\nMONTHLY AVERAGE PSH")
print(monthly_psh)

# -----------------------------------
# 3. DISTRICT-WISE GRAPH
# -----------------------------------

plt.figure(figsize=(12, 9))

plt.barh(
    district_psh["District"],
    district_psh["Average_PSH"]
)

plt.xlabel("Average Peak Sun Hours (hours/day)")
plt.ylabel("District")
plt.title("Average Peak Sun Hours Across Tamil Nadu")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("data/district_psh_graph.png", dpi=300)
plt.show()

# -----------------------------------
# 4. MONTHLY TREND GRAPH
# -----------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    month_names,
    monthly_psh.values,
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Average PSH (hours/day)")
plt.title("Monthly Peak Sun Hours – Tamil Nadu")
plt.grid(True)

plt.tight_layout()

plt.savefig("data/monthly_psh_graph.png", dpi=300)
plt.show()

print("\nPSH ANALYSIS COMPLETED!")
print("Districts analysed:", df["District"].nunique())
print("Total records:", len(df))
print("Average PSH:", round(df["PSH"].mean(), 3))

print("\nFiles saved successfully!")
