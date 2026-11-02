import pandas as pd
import matplotlib.pyplot as plt

# Load feature importance data
df = pd.read_csv("data/solar_feature_importance.csv")

# Select the 15 most important features
df = df.sort_values(
    by="Importance",
    ascending=True
).tail(15)

# Create graph
plt.figure(figsize=(11, 7))

plt.barh(df["Feature"], df["Importance"])

plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.title("Solar Radiation Prediction - Feature Importance")

plt.tight_layout()

# Save graph
plt.savefig(
    "data/feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Feature importance graph saved successfully!")