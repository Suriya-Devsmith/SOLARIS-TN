
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="SOLARIS-TN | Solar Analytics",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ SOLARIS-TN")
st.subheader("Solar Energy Potential Analysis and Prediction for Tamil Nadu")

st.markdown("""
Explore solar radiation, Peak Sun Hours, district rankings,
weather relationships and machine learning results across Tamil Nadu.
""")

# ---------------- DATA LOADING ----------------

def load_data(filename):
    locations = [
        Path(filename),
        Path("data") / filename
    ]

    for path in locations:
        if path.exists():
            try:
                return pd.read_csv(path)
            except Exception:
                st.warning(f"Could not read {filename}.")
                return None

    return None


district = load_data("district_average_psh.csv")
monthly = load_data("monthly_average_psh.csv")
ranking = load_data("solar_district_ranking.csv")
importance = load_data("solar_feature_importance.csv")
correlation = load_data("weather_correlation_matrix.csv")
performance = load_data("model_performance.csv")

# ---------------- SIDEBAR ----------------

st.sidebar.title("SOLARIS-TN")
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "District Analysis",
        "Monthly Analysis",
        "Machine Learning",
        "About Project"
    ]
)

# ---------------- OVERVIEW ----------------

if page == "Overview":

    st.header("Tamil Nadu Solar Overview")

    c1, c2, c3 = st.columns(3)

    if district is not None and not district.empty:
        st.info("District-wise PSH data loaded successfully.")
        c1.metric("District records", len(district))

    if monthly is not None and not monthly.empty:
        c2.metric("Monthly records", len(monthly))

    if ranking is not None and not ranking.empty:
        c3.metric("Ranked districts", len(ranking))

    st.markdown("---")

    st.subheader("Project Highlights")

    st.write("""
    - Solar radiation analysis across 38 Tamil Nadu districts.
    - Monthly and seasonal solar potential studies.
    - Peak Sun Hours estimation.
    - Weather correlation analysis.
    - Random Forest regression for solar radiation estimation.
    """)

    st.success("Welcome to the SOLARIS-TN Solar Analytics Dashboard!")

# ---------------- DISTRICT ANALYSIS ----------------

elif page == "District Analysis":

    st.header("District-wise Solar Analysis")

    if ranking is not None:
        st.dataframe(ranking, use_container_width=True)

        possible_columns = [
            "Average_Solar",
            "Average_PSH",
            "Average_PSH_Hours"
        ]

        value_column = next(
            (c for c in possible_columns if c in ranking.columns),
            None
        )

        if value_column and "District" in ranking.columns:
            fig = px.bar(
                ranking.sort_values(value_column, ascending=False),
                x="District",
                y=value_column,
                title="District-wise Solar Potential",
                color=value_column
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("District ranking data is not available.")

    if district is not None:
        st.subheader("District Average PSH")
        st.dataframe(district, use_container_width=True)

# ---------------- MONTHLY ANALYSIS ----------------

elif page == "Monthly Analysis":

    st.header("Monthly Solar Analysis")

    if monthly is not None:
        st.dataframe(monthly, use_container_width=True)

        st.info("Monthly solar radiation and PSH data.")

        numeric_columns = monthly.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_columns:
            value_column = st.selectbox(
                "Select a measurement",
                numeric_columns
            )

            fig = px.line(
                monthly,
                y=value_column,
                markers=True,
                title="Monthly Solar Trend"
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Monthly analysis data is not available.")

# ---------------- MACHINE LEARNING ----------------

elif page == "Machine Learning":

    st.header("Machine Learning Results")

    if performance is not None:
        st.subheader("Random Forest Model Performance")

        for _, row in performance.iterrows():
            st.metric(str(row["Metric"]), round(float(row["Value"]), 4))

    if importance is not None:
        st.subheader("Feature Importance")

        fig = px.bar(
            importance.sort_values(
                "Importance",
                ascending=True
            ).tail(15),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Important Features"
        )

        st.plotly_chart(fig, use_container_width=True)

    if correlation is not None:
        st.subheader("Weather Correlation Matrix")
        st.dataframe(correlation, use_container_width=True)

    st.caption(
        "The initial model estimates solar radiation using "
        "same-day weather and date/location features."
    )

# ---------------- ABOUT PROJECT ----------------

elif page == "About Project":

    st.header("About SOLARIS-TN")

    st.write("""
    SOLARIS-TN is a renewable energy analytics project
    developed to study solar energy potential across Tamil Nadu.

    **Data Source:** NASA POWER API

    **Programming Language:** Python

    **Machine Learning:** Random Forest Regression

    **Dashboard:** Streamlit

    **Study Region:** Tamil Nadu, India
    """)

    st.markdown("### Project Developer")
    st.write("Suriya Devsmith")

    st.markdown("### Project Domains")
    st.write(
        "Electrical Engineering | Renewable Energy | "
        "Data Analytics | Machine Learning"
    )

st.markdown("---")
st.caption("SOLARIS-TN | Exploring Tamil Nadu's Solar Energy Potential ☀️")
