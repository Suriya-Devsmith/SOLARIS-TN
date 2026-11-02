
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib

print("======================================")
print("       SOLARIS-TN MACHINE LEARNING")
print("======================================")

# 1. LOAD DATASET

df = pd.read_csv("data/tamilnadu_solar_master.csv")

df["Date"] = pd.to_datetime(df["Date"])

print("\nDataset loaded!")
print("Total records:", len(df))

# 2. DATA PREPARATION

features = [
    "District",
    "T2M",
    "RH2M",
    "PRECTOTCORR",
    "WS10M"
]

target = "ALLSKY_SFC_SW_DWN"

# Extract date-related features
df["Month"] = df["Date"].dt.month
df["DayOfYear"] = df["Date"].dt.dayofyear
df["Year"] = df["Date"].dt.year

# Cyclical features help represent seasonal patterns
df["Month_Sin"] = np.sin(2 * np.pi * df["Month"] / 12)
df["Month_Cos"] = np.cos(2 * np.pi * df["Month"] / 12)

df["Day_Sin"] = np.sin(2 * np.pi * df["DayOfYear"] / 365.25)
df["Day_Cos"] = np.cos(2 * np.pi * df["DayOfYear"] / 365.25)

features = features + [
    "Year",
    "Month_Sin",
    "Month_Cos",
    "Day_Sin",
    "Day_Cos"
]

# Remove rows with missing required values
df = df.dropna(subset=features + [target]).copy()

df = df.sort_values("Date").reset_index(drop=True)

X = df[features]
y = df[target]

# 3. CHRONOLOGICAL TRAIN-TEST SPLIT

# Use earlier 80% of dates for training
# Keep latest 20% of dates for testing

unique_dates = np.sort(df["Date"].unique())

split_index = int(len(unique_dates) * 0.8)
split_date = unique_dates[split_index]

train_mask = df["Date"] < split_date
test_mask = df["Date"] >= split_date

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]

print("\nTRAINING RECORDS:", len(X_train))
print("TESTING RECORDS:", len(X_test))
print("Test period starts:", pd.Timestamp(split_date).date())

# 4. BUILD MACHINE LEARNING PIPELINE

categorical_features = ["District"]

numerical_features = [
    "T2M",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "Year",
    "Month_Sin",
    "Month_Cos",
    "Day_Sin",
    "Day_Cos"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "district",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numerical_features
        )
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=100,
                max_depth=18,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

# 5. TRAIN THE MODEL

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

print("Training completed!")

# 6. MAKE PREDICTIONS

predictions = model.predict(X_test)

# 7. EVALUATE MODEL PERFORMANCE

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\n======================================")
print("       MODEL PERFORMANCE")
print("======================================")

print("MAE:", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R2 Score:", round(r2, 4))

# 8. SAVE PREDICTIONS

results = pd.DataFrame({
    "Date": df.loc[test_mask, "Date"].values,
    "District": df.loc[test_mask, "District"].values,
    "Actual_Solar": y_test.values,
    "Predicted_Solar": predictions
})

results.to_csv(
    "data/solar_predictions.csv",
    index=False
)

# 9. SAVE TRAINED MODEL

joblib.dump(model, "data/solar_random_forest.pkl")

# 10. FEATURE IMPORTANCE

trained_forest = model.named_steps["regressor"]

feature_names = (
    model.named_steps["preprocessor"].get_feature_names_out()
)

importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": trained_forest.feature_importances_
})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

importance.to_csv(
    "data/solar_feature_importance.csv",
    index=False
)

print("\nTOP 10 IMPORTANT FEATURES")
print(importance.head(10).to_string(index=False))

# 11. ACTUAL VS PREDICTED GRAPH

plt.figure(figsize=(9, 6))

plt.scatter(
    y_test,
    predictions,
    alpha=0.2,
    s=8
)

minimum = min(y_test.min(), predictions.min())
maximum = max(y_test.max(), predictions.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel("Actual Solar Radiation")
plt.ylabel("Predicted Solar Radiation")
plt.title("SOLARIS-TN: Actual vs Predicted Solar Radiation")
plt.tight_layout()

plt.savefig("data/actual_vs_predicted.png", dpi=300)
plt.show()

# 12. SAVE PERFORMANCE METRICS

metrics = pd.DataFrame({
    "Metric": ["MAE", "RMSE", "R2"],
    "Value": [mae, rmse, r2]
})

metrics.to_csv(
    "data/model_performance.csv",
    index=False
)

print("\n======================================")
print("MACHINE LEARNING COMPLETED!")
print("======================================")
print("Predictions saved.")
print("Trained model saved.")
print("Performance metrics saved.")
print("Feature importance saved.")
