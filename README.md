# ☀️ SOLARIS-TN

### Solar Energy Potential Analysis and Prediction for Tamil Nadu

**SOLARIS-TN** is a data analytics and machine learning project designed to analyse solar energy potential across the 38 districts of Tamil Nadu using NASA POWER weather and solar radiation data.

The project explores regional and seasonal variations in solar radiation, estimates Peak Sun Hours (PSH), studies weather relationships and develops a machine learning model to estimate solar radiation.

## 🎯 Project Objectives

- Analyse solar radiation across 38 districts of Tamil Nadu.
- Identify districts with higher solar energy potential.
- Study monthly and seasonal solar radiation patterns.
- Estimate Peak Sun Hours (PSH).
- Analyse the relationship between solar radiation and weather parameters.
- Develop a Machine Learning model for solar radiation prediction.
- Build an interactive dashboard for visualising results.

## 📊 Dataset

**Data Source:** NASA POWER API

**Study Region:** Tamil Nadu, India

**Study Period:** 2001–2025 (available data through July 2025)

**Parameters:**

- Solar Radiation (ALLSKY_SFC_SW_DWN)
- Temperature (T2M)
- Relative Humidity (RH2M)
- Rainfall (PRECTOTCORR)
- Wind Speed (WS10M)

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Streamlit
- Plotly
- NASA POWER API

## ⚙️ Project Workflow

1. Data Collection – Retrieve solar and weather data using NASA POWER API.
2. Data Preprocessing – Clean and organise the collected dataset.
3. Exploratory Data Analysis – Examine solar radiation patterns and variations.
4. Seasonal Analysis – Compare solar potential across different seasons.
5. Peak Sun Hours Analysis – Estimate daily solar availability.
6. Weather Correlation – Study relationships between weather parameters and solar radiation.
7. Machine Learning – Train a Random Forest Regression model.
8. Interactive Dashboard – Develop a visual analytics platform using Streamlit.

## 🤖 Machine Learning Model

**Algorithm:** Random Forest Regression

Initial model evaluation results:

| Metric   | Result |
| -------- | -----: |
| MAE      |  0.635 |
| RMSE     |  0.812 |
| R² Score |  0.591 |

The model uses date, district and same-day weather observations to estimate solar radiation. These results represent an initial evaluation, not a future-weather forecasting system.

## 📈 Key Project Findings

- March and April show relatively high average solar radiation in the analysed dataset.
- November shows relatively low average solar radiation.
- Relative humidity is the most influential feature in the initial Random Forest model.
- Seasonal timing and rainfall also contribute to model predictions.

## 🚀 Project Status

- [x] NASA POWER data collection
- [x] Exploratory data analysis
- [x] District-wise solar ranking
- [x] Seasonal analysis
- [x] Peak Sun Hours analysis
- [x] Weather correlation analysis
- [x] Initial Machine Learning model
- [ ] Interactive Streamlit dashboard
- [ ] Public dashboard deployment

## 👨‍💻 Developed By

**Suriya Devsmith**

Project: SOLARIS-TN

Domain: Electrical and Electronics Engineering | Renewable Energy | Data Analytics | Machine Learning

---

*SOLARIS-TN – Exploring Tamil Nadu's Solar Energy Potential Through Data and Technology.* ☀️
