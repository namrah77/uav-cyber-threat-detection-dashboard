import streamlit as st

def topbar():
    st.markdown("""
        <style>
            /* Top Bar */
            .topbar-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #2A6DF4;
                padding: 10px 20px;
                border-radius: 6px;
            }

            .topbar-left {
                display: flex;
                align-items: center;
            }

            .logo {
                font-size: 20px;
                font-weight: bold;
                color: white;
                margin-right: 15px;
            }

            .welcome-text {
                font-size: 16px;
                color: white;
            }

            .topbar-right {
                display: flex;
                align-items: center;
            }

            .icon {
                width: 25px;
                height: 25px;
                margin-left: 15px;
                cursor: pointer;
            }
        </style>

        <div class="topbar-container">
            <div class="topbar-left">
                <span class="logo">🔵 Logo</span>
                <span class="welcome-text">Welcome name!</span>
            </div>
            <div class="topbar-right">
                <img src="https://cdn-icons-png.flaticon.com/512/1827/1827379.png" class="icon" title="Notifications">
                <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png" class="icon" title="User Profile">
            </div>
        </div>
    """, unsafe_allow_html=True)
