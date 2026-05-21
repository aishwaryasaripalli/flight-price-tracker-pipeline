import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from datetime import datetime


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Airfare Intelligence Platform",
    page_icon="✈️",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0B1020;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #121A33;
        border-right: 1px solid #1E2A52;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 95%;
    }

    .metric-card {
        background: #151B36;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #1E2A52;
        box-shadow: 0px 2px 12px rgba(0,0,0,0.25);
    }

    .metric-title {
        color: #B0B8D1;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 700;
        color: white;
    }

    .section-card {
        background: #151B36;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #1E2A52;
        margin-bottom: 16px;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 700 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

engine = create_engine(
    "postgresql+psycopg2://airflow:airflow@localhost:5433/airflow"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

query = "SELECT * FROM flight_prices"

with engine.connect() as conn:
    df = pd.read_sql_query(query, conn)

# standardize columns
df.columns = df.columns.str.lower()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("✈ Airfare Analytics")

selected_airline = st.sidebar.multiselect(
    "Airline",
    sorted(df["airline"].unique()),
    default=sorted(df["airline"].unique())[:3]
)

selected_source = st.sidebar.multiselect(
    "Source City",
    sorted(df["source_city"].unique()),
    default=sorted(df["source_city"].unique())[:2]
)

selected_destination = st.sidebar.multiselect(
    "Destination City",
    sorted(df["destination_city"].unique()),
    default=sorted(df["destination_city"].unique())[:2]
)

price_range = st.sidebar.slider(
    "Price Range",
    int(df["price"].min()),
    int(df["price"].max()),
    (
        int(df["price"].min()),
        int(df["price"].max())
    )
)

st.sidebar.markdown("---")

st.sidebar.success(
    f"Live • {datetime.now().strftime('%H:%M:%S')}"
)

# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------

filtered_df = df[
    (df["airline"].isin(selected_airline)) &
    (df["source_city"].isin(selected_source)) &
    (df["destination_city"].isin(selected_destination)) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("Airfare Intelligence Platform")

st.caption(
    "Operational dashboard for airline pricing analytics and route monitoring"
)

# -------------------------------------------------
# KPI ROW
# -------------------------------------------------

avg_price = round(filtered_df["price"].mean(), 2)
max_price = filtered_df["price"].max()
min_price = filtered_df["price"].min()
flight_count = len(filtered_df)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>Flights Tracked</div>
            <div class='metric-value'>{flight_count:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>Average Fare</div>
            <div class='metric-value'>₹ {avg_price}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>Highest Fare</div>
            <div class='metric-value'>₹ {max_price}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>Lowest Fare</div>
            <div class='metric-value'>₹ {min_price}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("##")

# -------------------------------------------------
# DASHBOARD GRID
# -------------------------------------------------

left, center, right = st.columns([1.2, 1.8, 1.2])

# -------------------------------------------------
# LEFT PANEL
# -------------------------------------------------

with left:

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Airline Share")

    airline_share = (
        filtered_df["airline"]
        .value_counts()
        .reset_index()
    )

    airline_share.columns = ["airline", "count"]

    pie_fig = px.pie(
        airline_share,
        names="airline",
        values="count",
        hole=0.6,
        template="plotly_dark"
    )

    pie_fig.update_layout(
        paper_bgcolor="#151B36",
        height=320,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Peak Departure Window")

    dep_df = (
        filtered_df["departure_time"]
        .value_counts()
        .reset_index()
    )

    dep_df.columns = ["departure_time", "count"]

    dep_fig = px.bar(
        dep_df,
        x="departure_time",
        y="count",
        template="plotly_dark"
    )

    dep_fig.update_layout(
        paper_bgcolor="#151B36",
        plot_bgcolor="#151B36",
        height=280,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(
        dep_fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# CENTER PANEL
# -------------------------------------------------

with center:

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Fare Trend Analysis")

    trend_df = (
        filtered_df.groupby("source_city")["price"]
        .mean()
        .reset_index()
    )

    line_fig = px.line(
        trend_df,
        x="source_city",
        y="price",
        markers=True,
        template="plotly_dark"
    )

    line_fig.update_layout(
        paper_bgcolor="#151B36",
        plot_bgcolor="#151B36",
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(
        line_fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Top Revenue Routes")

    route_df = (
        filtered_df.groupby(
            ["source_city", "destination_city"]
        )["price"]
        .mean()
        .reset_index()
        .sort_values(by="price", ascending=False)
        .head(10)
    )

    route_fig = px.bar(
        route_df,
        x="source_city",
        y="price",
        color="destination_city",
        template="plotly_dark"
    )

    route_fig.update_layout(
        paper_bgcolor="#151B36",
        plot_bgcolor="#151B36",
        height=320,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(
        route_fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# RIGHT PANEL
# -------------------------------------------------

with right:

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Operational Status")

    st.success("ETL Pipeline Running")
    st.success("Database Connected")
    st.info("Refresh Interval • 30 sec")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Fare Distribution")

    hist_fig = px.histogram(
        filtered_df,
        x="price",
        nbins=25,
        template="plotly_dark"
    )

    hist_fig.update_layout(
        paper_bgcolor="#151B36",
        plot_bgcolor="#151B36",
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(
        hist_fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)

    st.subheader("Flight Records")

    st.dataframe(
        filtered_df[
            [
                "airline",
                "flight",
                "source_city",
                "destination_city",
                "price"
            ]
        ].head(8),
        use_container_width=True,
        height=320
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")

st.caption(
    "Airfare Intelligence Platform • Enterprise Analytics Dashboard"
)