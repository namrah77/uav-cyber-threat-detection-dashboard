import streamlit as st
import Home
import ThreatAnalysis

# Set Streamlit page config
st.set_page_config(
    page_title="UAV Cyber Threat Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            padding: 0px !important;
            width: 250px !important;
            background-color: inherit; /* Inherit dashboard background color */
            box-shadow: 3px 0 10px rgba(0, 0, 0, 0.15); /* Slightly more visible shadow */
        }

        .profile-section {
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid var(--secondary-background-color);
        }

        .profile-img {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            border: 2px solid var(--secondary-background-color);
        }

        .username {
            font-size: 16px;
            font-weight: bold;
            color: var(--text-color);
            margin-top: 8px;
        }

        .user-role {
            font-size: 13px;
            color: var(--text-color-secondary);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            margin-top: 10px;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            width: 100%;
            padding: 0.8rem 1.2rem;
            border-radius: 10px;
            font-size: 15px; /* Slightly larger font size */
            font-weight: 600; /* Bolder text */
            color: var(--text-color); /* Ensure text is readable */
            display: flex;
            align-items: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 5px;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #6B48FF !important; /* Deep purple for selected state */
            color: white !important;
            box-shadow: 0 2px 8px rgba(107, 72, 255, 0.3); /* Adjusted glow for new color */
        }
    </style>
    """, unsafe_allow_html=True)

    # Profile section
    st.markdown("""
        <div class="profile-section">
            <img class="profile-img" src="https://cdn-icons-png.flaticon.com/512/6858/6858504.png">
            <div class="username">Namra Tariq</div>
            <div class="user-role">UAV Operator</div>
        </div>
    """, unsafe_allow_html=True)

    # Radio-based navigation
    selected = st.radio(
        "Navigation",
        ["Home", "Threat Analysis"],
        label_visibility="collapsed",
        index=0
    )

# Load the selected page
if selected == "Home":
    Home.app()
elif selected == "Threat Analysis":
    ThreatAnalysis.app()
