import streamlit as st

def set_layout():
    """Initialize page config and apply global Ice Blue light theme."""
    st.set_page_config(
        page_title="Stockify",
        page_icon="📦",
        layout="wide"
    )
    inject_css()


def inject_css():
    """Inject comprehensive Ice Blue light theme CSS with animations and frosted glass styling."""
    st.markdown("""
    <style>
    /* ========== ANIMATIONS ========== */
    @keyframes gradientShift {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(-30px); }
    }
    
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    @keyframes shimmer {
      0% { background-position: -1000px 0; }
      100% { background-position: 1000px 0; }
    }
    
    @keyframes pulse-glow {
      0%, 100% { box-shadow: 0 4px 24px rgba(59,130,246,0.08); }
      50% { box-shadow: 0 8px 32px rgba(59,130,246,0.18); }
    }
    
    /* ========== ROOT & APP STYLING ========== */
    .stApp {
      background: transparent !important;
      color: #0f172a;
    }
    
    [data-testid="stAppViewContainer"] {
      background: transparent;
    }
    
    [data-testid="stHeader"] {
      background: transparent;
    }
    
    /* Floating background orbs */
    .stApp::before {
      content: '';
      position: fixed;
      top: -200px;
      left: -200px;
      width: 500px;
      height: 500px;
      background: #93c5fd;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.12;
      pointer-events: none;
      animation: float 8s ease-in-out infinite alternate;
      z-index: -1;
    }
    
    .stApp::after {
      content: '';
      position: fixed;
      top: 50%;
      right: -300px;
      width: 600px;
      height: 600px;
      background: #67e8f9;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.12;
      pointer-events: none;
      animation: float 10s ease-in-out infinite alternate 1s;
      z-index: -1;
    }
    
    html::before {
      content: '';
      position: fixed;
      bottom: -250px;
      left: 30%;
      width: 400px;
      height: 400px;
      background: #a5f3fc;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.12;
      pointer-events: none;
      animation: float 12s ease-in-out infinite alternate 2s;
      z-index: -1;
    }
    
    /* ========== SIDEBAR STYLING ========== */
    section[data-testid="stSidebar"] {
      background: rgba(240,249,255,0.85) !important;
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-right: 1px solid rgba(148,210,255,0.35);
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
      color: #0f172a;
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
      color: #0f172a;
    }
    
    section[data-testid="stSidebar"] label {
      color: #0f172a;
    }
    
    section[data-testid="stSidebar"] [role="radio"] {
      color: #0f172a;
    }
    
    section[data-testid="stSidebar"] [role="radio"]:hover {
      background-color: rgba(59,130,246,0.1);
      border-radius: 6px;
      transform: translateX(4px);
      transition: all 0.3s ease;
    }
    
    /* ========== GLOBAL GLASS-CARD STYLING ========== */
    .glass-card {
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(148,210,255,0.35);
      border-radius: 16px;
      box-shadow: 0 4px 24px rgba(59,130,246,0.08);
      transition: all 0.3s ease;
    }
    
    .glass-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(59,130,246,0.18);
      border-color: rgba(59,130,246,0.4);
    }
    
    /* ========== METRIC CARDS ========== */
    [data-testid="metric-container"] {
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(148,210,255,0.35);
      border-left: 3px solid #3b82f6;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 4px 24px rgba(59,130,246,0.08);
      transition: all 0.3s ease;
      animation: fadeInUp 0.4s ease;
    }
    
    [data-testid="metric-container"]:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(59,130,246,0.18);
      border-color: rgba(59,130,246,0.4);
      animation: pulse-glow 2s ease infinite;
    }
    
    [data-testid="metric-container"] .metric-label {
      color: #64748b;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }
    
    [data-testid="metric-container"] .metric-value {
      color: #1d4ed8;
      font-weight: 700;
    }
    
    /* ========== DATAFRAME STYLING ========== */
    [data-testid="dataframe"] {
      border-radius: 12px;
      overflow: hidden;
    }
    
    [data-testid="dataframe"] thead {
      background: #dbeafe;
      color: #1e3a5f;
      font-weight: 600;
    }
    
    [data-testid="dataframe"] tbody tr {
      border-bottom: 1px solid rgba(219,234,254,0.5);
    }
    
    [data-testid="dataframe"] tbody tr:hover {
      background: rgba(59,130,246,0.06);
    }
    
    [data-testid="dataframe"] tbody tr:nth-child(odd) {
      background: white;
    }
    
    [data-testid="dataframe"] tbody tr:nth-child(even) {
      background: #f8fbff;
    }
    
    /* ========== BUTTON STYLING ========== */
    .stButton > button {
      background: linear-gradient(135deg, #3b82f6, #06b6d4);
      color: white;
      border-radius: 10px;
      border: none;
      padding: 10px 20px;
      font-weight: 600;
      transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
      transform: scale(1.03);
      box-shadow: 0 8px 20px rgba(59,130,246,0.3);
    }
    
    .stButton > button:active {
      transform: scale(0.97);
    }
    
    /* ========== INFO/WARNING/SUCCESS BOXES ========== */
    [data-testid="stAlert"] {
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-radius: 12px;
      border-left: 3px solid #3b82f6;
      animation: fadeInUp 0.4s ease;
    }
    
    /* ========== PAGE HEADER ========== */
    .page-header {
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(148,210,255,0.35);
      border-left: 4px solid #3b82f6;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 24px rgba(59,130,246,0.08);
      animation: fadeInUp 0.4s ease;
    }
    
    .page-header-title {
      font-size: 32px;
      font-weight: 700;
      color: #0f172a;
      background: linear-gradient(135deg, #1d4ed8, #06b6d4);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 10px 0 5px 0;
    }
    
    .page-header-subtitle {
      font-size: 14px;
      color: #475569;
      margin: 0;
    }
    
    /* ========== HERO SECTION ========== */
    .hero-title {
      font-size: 48px;
      font-weight: 800;
      text-align: center;
      background: linear-gradient(135deg, #1d4ed8, #06b6d4);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin: 30px 0 15px 0;
      letter-spacing: 0.5px;
      animation: fadeInUp 0.5s ease;
    }
    
    .hero-sub {
      text-align: center;
      color: #475569;
      font-size: 18px;
      margin-bottom: 30px;
      animation: fadeInUp 0.6s ease;
    }
    
    .center-button {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
    
    /* ========== CARD STYLING ========== */
    .card {
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      padding: 24px;
      border-radius: 16px;
      border: 1px solid rgba(148,210,255,0.35);
      box-shadow: 0 4px 24px rgba(59,130,246,0.08);
      color: #0f172a;
      transition: all 0.3s ease;
      animation: fadeInUp 0.4s ease;
    }
    
    .card:hover {
      border-color: rgba(59,130,246,0.4);
      box-shadow: 0 12px 40px rgba(59,130,246,0.18);
      transform: translateY(-4px);
    }
    
    /* ========== TEXT & CONTENT ========== */
    h1, h2, h3, h4, h5, h6 {
      color: #0f172a !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
      color: #0f172a !important;
    }
    
    [data-testid="stCaption"] {
      color: #475569 !important;
    }
    
    /* ========== DIVIDERS ========== */
    hr {
      border-color: rgba(148,210,255,0.3) !important;
      opacity: 0.8 !important;
    }
    
    /* ========== INPUT FIELDS ========== */
    input, textarea, select {
      background-color: rgba(255,255,255,0.7) !important;
      color: #0f172a !important;
      border: 1px solid rgba(148,210,255,0.35) !important;
      border-radius: 10px !important;
    }
    
    input:focus, textarea:focus, select:focus {
      border-color: #3b82f6 !important;
      box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
    }
    
    /* ========== EXPANDER ========== */
    [data-testid="stExpander"] {
      background: rgba(255,255,255,0.55) !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      border: 1px solid rgba(148,210,255,0.35) !important;
      border-radius: 12px !important;
    }
    
    [data-testid="stExpander"] button {
      color: #0f172a !important;
    }
    
    /* ========== FILE UPLOADER ========== */
    [data-testid="fileUploadDropzone"] {
      background: rgba(219,234,254,0.3) !important;
      border-color: #93c5fd !important;
      border-radius: 12px !important;
    }
    
    [data-testid="fileUploadDropzone"]:hover {
      background: rgba(219,234,254,0.5) !important;
      border-color: #3b82f6 !important;
    }
    
    /* ========== TAB STYLING ========== */
    [data-testid="stTabs"] [role="tablist"] button {
      color: #0f172a !important;
      border-bottom: 2px solid transparent !important;
    }
    
    [data-testid="stTabs"] [role="tablist"] button[aria-selected="true"] {
      border-bottom-color: #3b82f6 !important;
    }
    
    [data-testid="stTabs"] [role="tablist"] button:hover {
      color: #3b82f6 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # Load Three.js at document level
    st.markdown(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
        unsafe_allow_html=True
    )
    
    # Inject particle sphere background at document level
    st.markdown("""
    <div id="stockify-sphere-bg" style="
        position: fixed;
        top: 0;
        right: 0;
        width: 55%;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.4;
        overflow: hidden;
    "></div>

    <script>
    (function() {
        if (window._stockifySphereInit) return;
        window._stockifySphereInit = true;

        function loadSphere() {
            const container = document.getElementById('stockify-sphere-bg');
            if (!container || typeof THREE === 'undefined') {
                setTimeout(loadSphere, 200);
                return;
            }

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(
                60, container.offsetWidth / container.offsetHeight, 0.1, 2000
            );
            camera.position.set(0, 0, 280);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.offsetWidth, container.offsetHeight);
            renderer.setClearColor(0x000000, 0);
            container.appendChild(renderer.domElement);

            const count = 15000;
            const positions = new Float32Array(count * 3);
            const colors = new Float32Array(count * 3);

            for (let idx = 0; idx < count; idx++) {
                const phi = Math.acos(-1 + (2 * idx) / count);
                const theta = Math.sqrt(count * Math.PI) * phi;
                const r = 160;
                positions[idx*3]   = r * Math.cos(theta) * Math.sin(phi);
                positions[idx*3+1] = r * Math.sin(theta) * Math.sin(phi);
                positions[idx*3+2] = r * Math.cos(phi);
                const norm = (Math.cos(phi) + 1) / 2;
                colors[idx*3]   = 0.23 + norm * 0.1;
                colors[idx*3+1] = 0.51 + norm * 0.3;
                colors[idx*3+2] = 0.96;
            }

            const geo = new THREE.BufferGeometry();
            geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            const mat = new THREE.PointsMaterial({
                size: 1.4, vertexColors: true,
                transparent: true, opacity: 1.0, sizeAttenuation: true
            });
            const sphere = new THREE.Points(geo, mat);
            scene.add(sphere);

            let t = 0;
            function animate() {
                requestAnimationFrame(animate);
                t += 0.003;
                sphere.rotation.y = t * 0.6;
                sphere.rotation.x = Math.sin(t * 0.3) * 0.12;
                sphere.scale.setScalar(1 + 0.03 * Math.sin(t * 1.5));
                renderer.render(scene, camera);
            }
            animate();

            window.addEventListener('resize', () => {
                if (!container) return;
                camera.aspect = container.offsetWidth / container.offsetHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.offsetWidth, container.offsetHeight);
            });
        }
        loadSphere();
    })();
    </script>
    """, unsafe_allow_html=True)