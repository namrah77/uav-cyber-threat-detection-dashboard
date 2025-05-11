import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib
import plotly.graph_objs as go
from collections import deque
from utils.load_model import load_classifier, load_data, load_isolation_forest, load_scaler_function

def app():
    # Load models and preprocessing
    isolation_forest = load_isolation_forest()
    classifier = load_classifier()
    transformer = load_scaler_function()
    data = pd.read_csv('C:/Users/PMLS/uav_dashboard/datasets/synthetic_data_stream.csv')

    features = ['noise_per_ms', 'eph', 'timestamp', 's_variance_m_s', 'epv', 'lat_x',
                'epv_x', 'evh', 'alt_ellipsoid_x', 'alt_ellipsoid_y', 'vel_m_s',
                'satellites_used', 'hdop', 'vdop', 'y', 'vel_d_m_s', 'delta_heading',
                'c_variance_rad', 'vel_n_m_s', 'z', 'heading_y', 'vy', 'vx',
                'vel_e_m_s', 'q[2]', 'jamming_indicator', 'cog_rad', 'z_deriv', 'vz',
                'ay', 'az', 'ax', 'q[1]', 'terrain_alt_valid']

    # --- Custom Styling for Dark Theme ---
    # Detect current theme
    theme = st.get_option("theme.base")

    # Define theme-specific styles
    css = """
        <style>
            /* Base styles */
            .big-font { 
                font-size: 28px !important; 
                font-weight: bold; 
                text-align: center; 
                padding: 10px;
                border-radius: 8px;
            }
            .button-row { 
                display: flex; 
                justify-content: center; 
                gap: 20px; 
                margin-top: 15px; 
            }
            .stDownloadButton > button, .stFileUploader > div > button {
                background-color: #007bff !important;
                color: white !important;
                font-weight: bold;
                border-radius: 8px !important;
                padding: 0.5em 1em;
            }
            /* Button styles */
            div[data-testid="stButton"] button[kind="secondary"] {
                font-weight: bold !important;
                border-radius: 8px !important;
                padding: 0.5em 1.5em !important;
                border: none !important;
                color: white !important;
            }
            div[data-testid="stButton"] button[kind="secondary"]:nth-child(1) {
                background-color: #28a745 !important; /* Start: Green */
            }
            div[data-testid="stButton"] button[kind="secondary"]:nth-child(2) {
                background-color: #c0392b !important; /* Stop: Red */
            }
            div[data-testid="stButton"] button[kind="secondary"]:nth-child(3) {
                background-color: #3498db !important; /* Reset: Blue */
            }
            .status-box {
                text-align: center;
                padding: 15px;
                border-radius: 10px;
                margin: 10px auto;
                width: 80%;
                font-size: 20px;
                font-weight: bold;
            }
            .metrics-center { 
                text-align: center; 
                font-size: 18px; 
                margin-top: 10px; 
            }
            .slider-style .stSlider > div > div {
                background: linear-gradient(to right, #00b4d8, #90e0ef);
            }
            .download-container {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                margin-top: 20px;
                width: 100%;
            }
            .log-heading {
                text-align: center !important;
                font-size: 24px !important;
                font-weight: bold !important;
                margin-bottom: 10px;
                width: 100%;
            }
            .stDownloadButton {
                display: flex;
                justify-content: center;
                width: 100%;
            }
    """

    # Theme-specific styles
    if theme == "light":
        css += """
            /* Light theme styles */
            .big-font {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            .status-box.benign {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            .status-box.malicious {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            .status-box.completed {
                background-color: #333333 !important;
                color: #FFFFFF !important;
            }
            .metrics-center {
                color: #333333 !important;
            }
            .log-heading {
                color: #333333 !important;
            }
        """
    else:  # dark theme
        css += """
            /* Dark theme styles */
            .big-font {
                background-color: transparent !important;
                color: #FFFFFF !important;
            }
            .status-box.benign {
                background-color: rgba(0, 128, 0, 0.3) !important;
                color: #90ee90 !important;
            }
            .status-box.malicious {
                background-color: rgba(255, 0, 0, 0.3) !important;
                color: #ff7f7f !important;
            }
            .status-box.completed {
                background-color: rgba(30, 144, 255, 0.2) !important;
                color: #87cefa !important;
            }
            .metrics-center {
                color: #FFFFFF !important;
            }
            .log-heading {
                color: #FFFFFF !important;
            }
        """

    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("<h1 class='big-font'>Real-Time UAV Cyber Threat Detection</h1>", unsafe_allow_html=True)
    st.write("This module streams UAV GPS signals and detects **Spoofing** and **Jamming** attacks in real-time.")

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'stream_active' not in st.session_state:
        st.session_state.stream_active = False
    if 'threat_logs' not in st.session_state:
        st.session_state.threat_logs = []
    if 'benign_count' not in st.session_state:
        st.session_state.benign_count = 0
    if 'malicious_count' not in st.session_state:
        st.session_state.malicious_count = 0

    batch_size = st.number_input("Batch Size (rows per stream):", min_value=1, max_value=100, value=12)
    with st.container():
        st.markdown("<div class='slider-style'>", unsafe_allow_html=True)
        contamination_threshold = st.slider("Contamination Threshold (adjust if needed):", 0.0, 1.0, 0.20, 0.01)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Buttons Row ---
    st.markdown("<div class='button-row'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start"):
            st.session_state.stream_active = True
    with col2:
        if st.button("Stop"):
            st.session_state.stream_active = False
    with col3:
        if st.button("Reset"):
            st.session_state.current_index = 0
            st.session_state.stream_active = False
            st.session_state.threat_logs = []
            st.session_state.benign_count = 0
            st.session_state.malicious_count = 0
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    status_placeholder = st.empty()
    chart_placeholder = st.empty()
    log_placeholder = st.empty()
    progress_placeholder = st.empty()
    counter_placeholder = st.empty()

    max_len = 30
    speed_hist = deque(maxlen=max_len)
    signal_hist = deque(maxlen=max_len)
    noise_hist = deque(maxlen=max_len)
    time_hist = deque(maxlen=max_len)

    # Define Plotly colors based on theme
    if theme == "light":
        speed_color = "#4682B4"  # Darker skyblue
        signal_color = "#D2691E"  # Darker orange
        noise_color = "#32CD32"  # Darker lightgreen
        plotly_template = "plotly"
    else:
        speed_color = "skyblue"
        signal_color = "orange"
        noise_color = "lightgreen"
        plotly_template = "plotly_dark"

    if st.session_state.stream_active and st.session_state.current_index < len(data):
        batch = data.iloc[st.session_state.current_index:st.session_state.current_index+batch_size].copy()
        X_batch = transformer.transform(batch[features])
        scores = isolation_forest.decision_function(X_batch)
        threshold = np.percentile(scores, contamination_threshold * 100)
        is_malicious = (scores < threshold).astype(int)

        for i, row in batch.iterrows():
            if not st.session_state.stream_active:
                break

            row_scaled = X_batch[i - st.session_state.current_index]
            timestamp = str(row["timestamp"])
            pred = is_malicious[i - st.session_state.current_index]

            speed_hist.append(row['vel_m_s'])
            signal_hist.append(row['jamming_indicator'])
            noise_hist.append(row['noise_per_ms'])
            time_hist.append(timestamp)

            if pred == 0:
                st.session_state.benign_count += 1
                status_placeholder.markdown("""
                    <div class='status-box benign'>Normal Signal Detected</div>
                """, unsafe_allow_html=True)
                st.session_state.threat_logs.append({"Time": timestamp, "Signal Type": "Benign"})
            else:
                attack_type = "Spoofing" if classifier.predict([row_scaled])[0] == 0 else "Jamming"
                st.session_state.malicious_count += 1
                status_placeholder.markdown(f"""
                    <div class='status-box malicious'>Malicious Detected: {attack_type}</div>
                """, unsafe_allow_html=True)
                st.session_state.threat_logs.append({"Time": timestamp, "Signal Type": attack_type})

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(time_hist), y=list(speed_hist), name="Speed", line=dict(color=speed_color)))
            fig.add_trace(go.Scatter(x=list(time_hist), y=list(signal_hist), name="Jamming Indicator", line=dict(color=signal_color)))
            fig.add_trace(go.Scatter(x=list(time_hist), y=list(noise_hist), name="Noise/ms", line=dict(color=noise_color)))
            fig.update_layout(title="Live UAV Metrics", template=plotly_template, xaxis_title="Timestamp", yaxis_title="Value")
            chart_placeholder.plotly_chart(fig, use_container_width=True)

            counter_placeholder.markdown(
                f"<div class='metrics-center'><b>Benign Signals:</b> {st.session_state.benign_count}     "
                f"<b>Malicious Signals:</b> {st.session_state.malicious_count}</div>",
                unsafe_allow_html=True
            )

            time.sleep(0.4)

        st.session_state.current_index += batch_size
        progress = st.session_state.current_index / len(data)
        progress_placeholder.progress(min(progress, 1.0))

        if st.session_state.current_index >= len(data):
            status_placeholder.markdown("<div class='status-box completed'>Stream Completed</div>", unsafe_allow_html=True)
            st.session_state.stream_active = False

    if st.session_state.threat_logs:
        log_df = pd.DataFrame(st.session_state.threat_logs)
        st.markdown("<h3 class='log-heading'>Signal Detection Log</h3>", unsafe_allow_html=True)
        log_placeholder.dataframe(log_df, use_container_width=True)
        csv = log_df.to_csv(index=False).encode('utf-8')
        st.markdown("<div class='download-container'>", unsafe_allow_html=True)
        st.download_button("Download Detection Log", data=csv, file_name="detection_logs.csv", mime="text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Upload New Data Section ---
    st.markdown("---")
    st.markdown("<h1 class='big-font'>Upload New Data for Streaming</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully!")
        st.write(data.head())

if __name__ == "__main__":
    app()