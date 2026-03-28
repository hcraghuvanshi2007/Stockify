import streamlit as st
from frontend.layout import inject_css

def show_home():
    """Display home page with hero section and value propositions."""
    inject_css()
    
    # Hero section
    st.markdown("""
    <div class='glass-card' style='padding: 60px 32px; text-align: center; margin-bottom: 40px;'>
        <div class='hero-title'>Stockify</div>
        <div class='hero-sub'>Smart Inventory for Retailers</div>
        <div style='margin-top: 20px; font-size: 15px; color: #475569; max-width: 600px; margin-left: auto; margin-right: auto;'>
            Stop relying on guesswork. Make data-driven decisions with AI-powered inventory insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA Button
    st.markdown("<div class='center-button'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Start Analyzing Data", use_container_width=True):
            st.switch_page("pages/upload.py")
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Value propositions section
    st.markdown("""
    <div style='text-align: center; margin: 48px 0 32px 0;'>
        <h2 style='color: #0f172a; margin: 0;'>Why Choose Stockify</h2>
        <div style='color: #475569; margin-top: 8px;'>Built for smart retailers who want to optimize inventory</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card' style='height: 100%; display: flex; flex-direction: column; align-items: center; text-align: center;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 16px;">
                <line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <div style='font-weight: 600; font-size: 16px; color: #1d4ed8; margin-bottom: 8px;'>Real-time Monitoring</div>
            <div style='color: #475569; font-size: 14px;'>Track inventory levels and sales in real-time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card' style='height: 100%; display: flex; flex-direction: column; align-items: center; text-align: center;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 16px;">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>
            </svg>
            <div style='font-weight: 600; font-size: 16px; color: #0e7490; margin-bottom: 8px;'>Demand Forecasting</div>
            <div style='color: #475569; font-size: 14px;'>Predict future demand with intelligent analytics</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='card' style='height: 100%; display: flex; flex-direction: column; align-items: center; text-align: center;'>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 16px;">
                <line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><polygon points="21 16 21 8 12 3 3 8 3 16 12 21 21 16"></polygon><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
            <div style='font-weight: 600; font-size: 16px; color: #4f46e5; margin-bottom: 8px;'>Smart Reorder</div>
            <div style='color: #475569; font-size: 14px;'>Automatic reorder recommendations</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Features section
    st.markdown("""
    <div style='text-align: center; margin: 48px 0 32px 0;'>
        <h2 style='color: #0f172a; margin: 0;'>Powerful Features</h2>
        <div style='color: #475569; margin-top: 8px;'>Everything you need to optimize inventory</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <div style='font-weight: 600; font-size: 16px; color: #0f172a; margin-bottom: 12px;'>Easy Data Upload</div>
            <div style='color: #475569; font-size: 14px; line-height: 1.6;'>
                Simply drag and drop your inventory and sales CSV/Excel files. Our intelligent system automatically validates and processes your data.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card' style='margin-top: 16px;'>
            <div style='font-weight: 600; font-size: 16px; color: #0f172a; margin-bottom: 12px;'>Data-Driven Analytics</div>
            <div style='color: #475569; font-size: 14px; line-height: 1.6;'>
                Get actionable insights on product demand, sales trends, and profitability based on your actual data.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <div style='font-weight: 600; font-size: 16px; color: #0f172a; margin-bottom: 12px;'>Visual Dashboards</div>
            <div style='color: #475569; font-size: 14px; line-height: 1.6;'>
                Interactive charts and visualizations make it easy to understand your inventory performance at a glance.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card' style='margin-top: 16px;'>
            <div style='font-weight: 600; font-size: 16px; color: #0f172a; margin-bottom: 12px;'>Smart Recommendations</div>
            <div style='color: #475569; font-size: 14px; line-height: 1.6;'>
                Receive intelligent alerts and reorder recommendations to prevent stockouts and overstock situations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Getting started section
    st.markdown("""
    <div style='text-align: center; margin: 48px 0; padding: 40px; background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(148,210,255,0.35); border-radius: 16px;'>
        <h3 style='color: #0f172a; margin-top: 0;'>Ready to Get Started</h3>
        <div style='color: #475569; margin-bottom: 24px;'>Upload your inventory and sales data to begin analyzing</div>
    </div>
    """, unsafe_allow_html=True)