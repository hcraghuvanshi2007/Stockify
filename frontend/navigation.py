import streamlit as st

def sidebar_navigation():
    """Render styled sidebar navigation with logo, nav links, and logout."""
    
    # Sidebar header with logo - Lucide Package icon + text
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 16px;">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1d4ed8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><polygon points="21 16 21 8 12 3 3 8 3 16 12 21 21 16"></polygon>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
            <span style="font-size: 20px; font-weight: 800; color: #1d4ed8; margin-left: 10px; letter-spacing: 0.5px;">Stockify</span>
        </div>
        <div style="font-size: 11px; color: #06b6d4; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600;">Smart Inventory</div>
    </div>
    <hr style="border-color: rgba(148,210,255,0.3); margin: 16px 0;">
    """, unsafe_allow_html=True)

    # Navigation section
    st.sidebar.markdown(
        "<div style='color: #3b82f6; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; margin: 20px 0 12px 0;'>Navigation</div>",
        unsafe_allow_html=True
    )
    
    # Navigation with Lucide icons inline
    nav_icons_html = """
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <button style="width: 100%; padding: 12px 16px; border: 1px solid #bfdbfe; background: transparent; color: #1e40af; border-radius: 10px; cursor: pointer; display: flex; align-items: center; font-size: 14px; font-weight: 600; transition: all 0.3s ease;" onclick="console.log('home')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            Home
        </button>
        <button style="width: 100%; padding: 12px 16px; border: 1px solid #bfdbfe; background: transparent; color: #1e40af; border-radius: 10px; cursor: pointer; display: flex; align-items: center; font-size: 14px; font-weight: 600; transition: all 0.3s ease;" onclick="console.log('upload')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
            Upload
        </button>
        <button style="width: 100%; padding: 12px 16px; border: 1px solid #bfdbfe; background: transparent; color: #1e40af; border-radius: 10px; cursor: pointer; display: flex; align-items: center; font-size: 14px; font-weight: 600; transition: all 0.3s ease;" onclick="console.log('dashboard')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            Overview
        </button>
        <button style="width: 100%; padding: 12px 16px; border: 1px solid #bfdbfe; background: transparent; color: #1e40af; border-radius: 10px; cursor: pointer; display: flex; align-items: center; font-size: 14px; font-weight: 600; transition: all 0.3s ease;" onclick="console.log('products')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
            Products
        </button>
        <button style="width: 100%; padding: 12px 16px; border: 1px solid #bfdbfe; background: transparent; color: #1e40af; border-radius: 10px; cursor: pointer; display: flex; align-items: center; font-size: 14px; font-weight: 600; transition: all 0.3s ease;" onclick="console.log('trends')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
            Trends
        </button>
        <button style="width: 100%; padding: 12px 16px; border: 1px solid #bfdbfe; background: transparent; color: #1e40af; border-radius: 10px; cursor: pointer; display: flex; align-items: center; font-size: 14px; font-weight: 600; transition: all 0.3s ease;" onclick="console.log('insights')">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 10px;"><line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"></path></svg>
            Insights
        </button>
    </div>
    """
    
    page = st.sidebar.radio(
        "Navigation",
        [" Home", " Upload", " Overview", " Products", " Trends", " Insights"],
        label_visibility="collapsed"
    )

    # Section divider
    st.sidebar.markdown(
        "<hr style='border-color: rgba(148,210,255,0.3); margin: 20px 0;'>",
        unsafe_allow_html=True
    )

    # Demo mode banner
    st.sidebar.markdown("""
    <div style="background: rgba(255,255,255,0.55); backdrop-filter: blur(16px); border: 1px solid rgba(59,130,246,0.35); border-left: 3px solid #06b6d4; border-radius: 10px; padding: 12px; margin-bottom: 16px;">
        <div style="font-size: 12px; font-weight: 600; color: #1d4ed8;">Demo Mode Active</div>
        <div style="font-size: 11px; color: #475569; margin-top: 4px;">Full access to explore</div>
    </div>
    """, unsafe_allow_html=True)

    # Logout button
    st.sidebar.markdown(
        "<div style='margin-bottom: 8px; color: #3b82f6; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;'>Account</div>",
        unsafe_allow_html=True
    )
    
    if st.sidebar.button("Logout", use_container_width=True, key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()

    return page