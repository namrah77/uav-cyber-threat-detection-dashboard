## **UAV Cyber Threat Detection Dashboard**

### **Overview**:
The UAV Cyber Threat Detection Dashboard is a real-time monitoring and threat detection system for Unmanned Aerial Vehicles (UAVs). It uses machine learning models to identify potential cybersecurity threats, such as GPS Spoofing and GPS Jamming attacks, based on UAV signal data. The system is built using Streamlit for a real-time interactive user interface and Plotly for dynamic data visualization.

### **Dashboard Features**:
- **Real-Time Threat Detection**
  - Detects **GPS Spoofing** and **GPS Jamming** attacks in UAV GPS data.
  - Uses **Column Transfomer** for pre-processing incoming data.
  - Uses **Isolation Forest** for anomaly detection.
  - A **Random Forest Classifier** model identifies the specific type of threat.

- **Live Visualizations**
  - Real-time charts update as new data batches stream in.
  - Display of current signal status: **Benign** or **Malicious**.
  - Visual metrics for **Speed**, **Signal**, and **Noise** levels.

- **Threat Logs**
  - Timestamped logs of every detection event.
  - Logs downloadable as CSV files.

- **User Controls**
  - Start / Stop / Reset buttons for controlling the stream.
  - Adjustable **batch size** and **contamination threshold**.

- **Data Upload**
  - Upload your own UAV GPS dataset (CSV format) for analysis.

- **Theme Adaptive UI**
  - Custom-styled buttons, sliders, and components.
  - Automatically adapts to **dark or light mode**.

## ⚡ Installation

Follow these steps to set up and run the UAV Cyber Threat Detection Dashboard on your local machine.

### 1. Clone the Repository

Begin by cloning the repository to your local system:

```bash
git clone https://github.com/namrah77/uav-cyber-threat-detection-dashboard.git
cd uav-cyber-threat-detection-dashboard
```
### 2. Set Up a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
### 4. Running Dashboard
```bash
streamlit run app.py
```
## 🏠 Home Page – Dashboard Overview

The **Home Page** offers a summary of the UAV cyber threat detection system, focusing on the training data and model insights.

### Key Features:

- **Dataset Preview**: Displays the UAV GPS dataset used for model training, with both scaled and unscaled features.
- **Signal Metrics**: Summary of signal types:
  - ✅ **Benign**
  - 🚨 **Malicious**
  - 🛰️ **Spoofed**
  - 📡 **Jammed**
- **Feature Importance**:
  - Top 10 features for **Isolation Forest** (Anomaly Detection Model)
  - Top 10 features for **Random Forest Classifier** (Attack classification Model)


## 🛡️ Threat Analysis Page Workflow

The **Threat Analysis** page detects real-time UAV GPS threats using a structured approach:

#### 1. **Data Pre-processing**
   - Data is streamed in real-time from a CSV file.
   - It undergoes **pre-processing** to handle missing values, scaling, and transformations using a trained **ColumnTransformer**.
   - The pre-processed data is ready for anomaly detection.

#### 2. **Isolation Forest Detection**
   - The pre-processed data is passed to the **Isolation Forest** model.
   - **Anomalies** are detected. If the data point is classified as **malicious**, further classification occurs.
   - **Benign signals** are ignored in the next steps.

#### 3. **Attack Classification**
   - For **malicious signals**, a **Classifier** (e.g., Random Forest) determines whether the threat is a **Spoofing** or **Jamming** attack based on additional signal features.
   - **Spoofing** and **Jamming** are the two primary attack types detected by the classifier.

#### 4. **Real-Time Visualizations**
   - **Status boxes** show real-time counts of **Benign**, **Malicious**, **Spoofed**, and **Jammed** signals.
   - **Charts** dynamically update with each batch of data, highlighting the detection results and threat types.
   
#### 5. **Threat Logs**
   - **Logs** are generated with timestamps for each detection event (Benign/Malicious).
   - Users can **download these logs as CSV** files for further analysis.

#### 6. **Metrics Overview**
   - Continuous updates to **signal counts** are displayed for easy tracking of detection results (Benign, Malicious, Spoofed, Jammed).

### ⚙️Technologies Used

- Streamlit: A framework for creating interactive web applications.

- Plotly: Used for creating interactive charts and visualizations.

- scikit-learn: For implementing machine learning models like Isolation Forest and classification models.

- Pandas and NumPy: For data manipulation and processing.

- CSS: For custom styling and theme management (light and dark mode).

### 🤝**Contributions**:
Feel free to report bugs, suggest features, or submit pull requests!

### 📜**License**:
This project is licensed under the MIT License -[MIT License](LICENSE) see the  file for details.

