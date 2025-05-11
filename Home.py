import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import f1_score
import folium
from streamlit_folium import st_folium
from utils.load_model import load_isolation_forest, load_classifier, load_data, load_training_data, load_unscaled
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from sklearn.inspection import permutation_importance

# Detect theme mode
base_theme = st.get_option("theme.base") or "light"

# Set theme-specific colors
if base_theme == "dark":
    benign_bg = "#4CAF50"
    malicious_bg = "#FF5733"
    spoofed_bg = "#FFC300"
    jammed_bg = "#800080"
    header_bg = "#4682B4"
    feature_bar_colors = ['#4B000F', '#FF4500', '#FFB300']
    rf_colors = ['#001f3f', '#0074D9', '#7FDBFF']
    plot_template = "plotly_dark"
else:
    benign_bg = "#007A45"
    malicious_bg = "#C9302C"
    spoofed_bg = "#E8B000"
    jammed_bg = "#5A005A"
    header_bg = "#4682B4"
    feature_bar_colors = ['#800010', '#FF6F00', '#FFC000']
    rf_colors = ['#002244', '#3366CC', '#99CCFF']  # Darker for light theme
    plot_template = "plotly_white"

# Function to create metric boxes
def render_metric_box(label, count, bg_color):
    return f'<div class="metric-box {label}">Total {label.capitalize()} Signals<br><h2>{count}</h2></div>'

# Set up Streamlit page config
def app():
    st.markdown("<h1 class='big-font'> UAV Cyber Threat Detection Dashboard Overview</h1>", unsafe_allow_html=True)
    st.write("Monitoring UAV GPS navigation threats detected by AI-based models.")

    # Load Data & Models
    isolation_forest = load_isolation_forest()
    classifier = load_classifier()
    df = load_data()
    df2 = load_unscaled()
    data = load_training_data()

    def isolation_forest_scorer(estimator, X, y):
        predictions = estimator.predict(X)
        pred_binary = (predictions == -1).astype(int)
        return f1_score(y, pred_binary, average='binary')

    # Custom Styling
    st.markdown(f"""
        <style>
            .big-font {{ font-size:24px !important; font-weight: bold; }}
            .medium-font {{ font-size:20px !important; font-weight: bold; }}
            .small-font {{ font-size:16px !important; }}
            .metric-box {{ 
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                color: white;
            }}
            .benign {{ background-color: {benign_bg}; }}
            .malicious {{ background-color: {malicious_bg}; }}
            .spoofed {{ background-color: {spoofed_bg}; }}
            .jammed {{ background-color: {jammed_bg}; }}
            .dataset-details {{ font-size: 16px; font-weight: bold; }}
            .dataframe-container {{
                padding: 0px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                background-color: transparent;
            }}
            .dataframe-header {{
                background-color: {header_bg};
                color: white;
                font-weight: bold;
                text-align: center;
                padding: 20px;
                border-radius: 10px 10px 0 0;
            }}
        </style>
        """, unsafe_allow_html=True)

    # Display metrics for the signal counts
    if not df.empty:
        benign_count = df[df["label"] == 0].shape[0]
        malicious_count = df[df["label"] == 1].shape[0]
        spoofing_count = df[(df["label"] == 1) & (df["source"] == 1)].shape[0]
        jamming_count = df[(df["label"] == 1) & (df["source"] == 2)].shape[0]
    else:
        benign_count = malicious_count = spoofing_count = jamming_count = 0

    # Layout for metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric_box("benign", benign_count, benign_bg), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_box("malicious", malicious_count, malicious_bg), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_box("spoofed", spoofing_count, spoofed_bg), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_box("jammed", jamming_count, jammed_bg), unsafe_allow_html=True)

    st.write("---")

    # Dataset Details
    st.markdown("<h1 class='big-font'>UAV Attack Dataset Details</h1>", unsafe_allow_html=True)
    st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
    st.markdown("<div class='dataframe-header'>Feature Overview</div>", unsafe_allow_html=True)
    st.dataframe(df2.head(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h1 class='big-font'>Feature Importance of Trained Models</h1>", unsafe_allow_html=True)

    # Feature Importance (Isolation Forest)
    features = pd.read_csv("C:/Users/PMLS/uav_dashboard/Feature Importance IF.csv")
    top_10 = features.sort_values(by='Importance', ascending=False).head(10)
    fig = px.bar(top_10, x='Feature', y='Importance', title="Top 10 Feature Importances (Isolation Forest)", 
                 color='Importance', color_continuous_scale=feature_bar_colors, template=plot_template)
    st.plotly_chart(fig)

    # Feature Importance (Random Forest)
    rf_features = pd.read_csv("C:/Users/PMLS/uav_dashboard/Feature Importance RF.csv")
    top_10_rf = rf_features.sort_values(by='Importance', ascending=False).head(10)
    fig_rf = px.scatter(top_10_rf, x='Feature', y='Importance', size='Importance', color='Importance', 
                        color_continuous_scale=rf_colors, title="Top 10 Feature Importances (Random Forest)", 
                        template=plot_template, size_max=30)
    fig_rf.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')))
    fig_rf.update_layout(xaxis_tickangle=0)
    st.plotly_chart(fig_rf)

    st.write("---")
