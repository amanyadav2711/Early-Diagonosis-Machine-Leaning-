import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wellness — Health Assistant",
    layout="wide",
    page_icon="✦",
    initial_sidebar_state="expanded"
)

# ── Custom CSS (wellness theme) ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Global ── */
*, *::before, *::after { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp { background-color: #edeae3; }

#MainMenu, footer, header { visibility: hidden; }

/* Remove default top padding */
.block-container { padding-top: 1.5rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(170deg, #232b18 0%, #2e3d1e 60%, #3a4e26 100%);
    border-right: none;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18);
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] .stMarkdown p { color: rgba(255,255,255,0.7) !important; }

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 28px 0;
}
.sidebar-icon {
    background: #8a9e5e;
    border-radius: 50%;
    width: 38px; height: 38px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(138,158,94,0.4);
}
.sidebar-name {
    font-size: 22px;
    font-weight: 800;
    color: white !important;
    letter-spacing: -0.5px;
}

.health-tip-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 16px;
    margin-top: 24px;
}
.health-tip-title {
    font-size: 13px; font-weight: 700;
    color: #a8c070 !important;
    margin-bottom: 6px;
}
.health-tip-body {
    font-size: 12px; line-height: 1.6;
    color: rgba(255,255,255,0.65) !important;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #ddd9ce 0%, #cdc8ba 40%, #bfb9a8 100%);
    border-radius: 28px;
    padding: 52px 56px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    min-height: 220px;
}
.hero::before {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(138,158,94,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    background: rgba(45,51,28,0.12);
    color: #2d331c;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 12px; font-weight: 700;
    letter-spacing: 0.5px;
    display: inline-block;
    margin-bottom: 18px;
    text-transform: uppercase;
}
.hero-title {
    font-size: 50px;
    font-weight: 900;
    color: #1a1a12;
    line-height: 1.08;
    margin-bottom: 18px;
    letter-spacing: -1.5px;
}
.hero-title-sm {
    font-size: 36px;
    font-weight: 900;
    color: #1a1a12;
    line-height: 1.1;
    margin-bottom: 14px;
    letter-spacing: -1px;
}
.hero-sub {
    font-size: 15px;
    color: #4a4840;
    max-width: 460px;
    line-height: 1.65;
    font-weight: 400;
}

/* ── Stat cards ── */
.stats-row {
    display: flex;
    gap: 14px;
    margin-bottom: 26px;
}
.stat-card {
    background: white;
    border-radius: 20px;
    padding: 22px 20px;
    flex: 1;
    text-align: center;
    box-shadow: 0 2px 14px rgba(0,0,0,0.055);
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.10); }
.stat-value {
    font-size: 30px; font-weight: 900;
    color: #2d3320; letter-spacing: -1px;
}
.stat-label { font-size: 11px; color: #999; margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Feature cards (home) ── */
.feature-card {
    background: white;
    border-radius: 22px;
    padding: 28px 26px;
    height: 100%;
    box-shadow: 0 2px 14px rgba(0,0,0,0.055);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.feature-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.10); }
.feature-emoji { font-size: 38px; margin-bottom: 14px; }
.feature-title { font-size: 18px; font-weight: 800; color: #1a1a12; margin-bottom: 10px; }
.feature-desc { font-size: 13px; color: #777; line-height: 1.65; margin-bottom: 16px; }
.feature-tag {
    background: #eef4e2;
    color: #4a6630;
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 12px; font-weight: 700;
    display: inline-block;
}
.feature-accent {
    position: absolute;
    bottom: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: rgba(138,158,94,0.08);
}

/* ── Input section card ── */
.input-section {
    background: white;
    border-radius: 24px;
    padding: 32px 36px;
    margin-bottom: 24px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.055);
}
.section-label {
    font-size: 11px; font-weight: 700;
    color: #8a9e5e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.section-title {
    font-size: 20px; font-weight: 800;
    color: #1a1a12;
    margin-bottom: 4px;
}
.section-divider {
    height: 3px;
    width: 48px;
    background: linear-gradient(90deg, #8a9e5e, #b8cc8a);
    border-radius: 4px;
    margin: 10px 0 24px 0;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 1.5px solid #e4e1d8 !important;
    padding: 11px 15px !important;
    font-size: 14px !important;
    background: #fafaf7 !important;
    color: #1a1a12 !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #8a9e5e !important;
    box-shadow: 0 0 0 3px rgba(138,158,94,0.18) !important;
    background: white !important;
}
.stTextInput label {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #4a4840 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(135deg, #2d3320 0%, #4a5c30 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 40px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 18px rgba(45,51,28,0.32) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(45,51,28,0.42) !important;
    background: linear-gradient(135deg, #3a4428 0%, #5a6e38 100%) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result cards ── */
.result-danger {
    background: linear-gradient(135deg, #fff0f0 0%, #ffe4e4 100%);
    border: 1.5px solid #fecaca;
    border-left: 5px solid #ef4444;
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 22px;
}
.result-safe {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border: 1.5px solid #bbf7d0;
    border-left: 5px solid #22c55e;
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 22px;
}
.result-icon { font-size: 28px; margin-bottom: 8px; }
.result-heading { font-size: 18px; font-weight: 800; color: #1a1a12; margin-bottom: 6px; }
.result-body { font-size: 14px; color: #555; line-height: 1.6; }

/* ── Warning override ── */
.stWarning { border-radius: 14px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #c8c3b0; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Load models ────────────────────────────────────────────────────────────────
working_dir = os.path.dirname(os.path.abspath(__file__))

import warnings
warnings.filterwarnings("ignore")

diabetes_model      = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model    = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-icon">✦</div>
        <div class="sidebar-name">Wellness</div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=['Home', 'Diabetes', 'Heart Disease', "Parkinson's"],
        icons=['house-heart-fill', 'droplet-half', 'heart-pulse-fill', 'person-arms-up'],
        default_index=0,
        styles={
            "container":       {"padding": "0", "background-color": "transparent"},
            "icon":            {"color": "#a0b870", "font-size": "15px"},
            "nav-link": {
                "font-size": "14px",
                "color": "rgba(255,255,255,0.72)",
                "padding": "11px 16px",
                "border-radius": "14px",
                "margin": "3px 0",
                "font-weight": "500",
            },
            "nav-link-selected": {
                "background": "rgba(138,158,94,0.22)",
                "color": "white",
                "font-weight": "700",
            },
        }
    )

    # Health tip
    tips = {
        'Home':         ("💧", "Stay hydrated — drink at least 8 glasses of water daily to support organ function."),
        'Diabetes':     ("🥗", "A diet rich in fibre and low in refined sugars helps maintain healthy glucose levels."),
        'Heart Disease':("🚶", "30 minutes of moderate walking daily can significantly reduce cardiovascular risk."),
        "Parkinson's":  ("🧘", "Regular exercise and mindfulness practices may help slow Parkinson's progression."),
    }
    icon, tip = tips.get(selected, tips['Home'])
    st.markdown(f"""
    <div class="health-tip-card">
        <div class="health-tip-title">{icon} Health Tip</div>
        <div class="health-tip-body">{tip}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if selected == 'Home':

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ AI-Powered Health Screening</div>
        <div class="hero-title">Balance your mind.<br>Fuel your life.</div>
        <div class="hero-sub">
            <strong>Discover personalised</strong> health insights designed to help you
            achieve balance, clarity, and lasting well-being.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">3</div>
            <div class="stat-label">Disease Models</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">ML</div>
            <div class="stat-label">Powered</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">Free</div>
            <div class="stat-label">Always</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">Fast</div>
            <div class="stat-label">Instant Results</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-emoji">🩺</div>
            <div class="feature-title">Diabetes Screening</div>
            <div class="feature-desc">Predict diabetes risk using glucose levels, BMI, insulin, and other clinical biomarkers with high accuracy.</div>
            <div class="feature-tag">8 parameters →</div>
            <div class="feature-accent"></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-emoji">❤️</div>
            <div class="feature-title">Heart Disease Check</div>
            <div class="feature-desc">Assess cardiovascular risk using cholesterol, blood pressure, ECG data, and exercise-induced metrics.</div>
            <div class="feature-tag">13 parameters →</div>
            <div class="feature-accent"></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-emoji">🧠</div>
            <div class="feature-title">Parkinson's Analysis</div>
            <div class="feature-desc">Detect early signs of Parkinson's disease through voice frequency patterns and acoustic signal measurements.</div>
            <div class="feature-tag">22 parameters →</div>
            <div class="feature-accent"></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:white;border-radius:22px;padding:28px 32px;box-shadow:0 2px 14px rgba(0,0,0,0.055);">
        <div style="font-size:11px;font-weight:700;color:#8a9e5e;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">⚠️ Disclaimer</div>
        <div style="font-size:13px;color:#777;line-height:1.7;">
            This tool is for <strong>educational and informational purposes only</strong>. 
            It is not a substitute for professional medical advice, diagnosis, or treatment. 
            Always consult a qualified healthcare professional for medical decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DIABETES PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == 'Diabetes':

    st.markdown("""
    <div class="hero" style="min-height:180px; padding:40px 52px;">
        <div class="hero-badge">🩺 Diabetes Screening</div>
        <div class="hero-title-sm">Diabetes Prediction</div>
        <div class="hero-sub" style="margin-bottom:0;">Enter your clinical measurements below for an AI-powered diabetes risk assessment.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="input-section">
        <div class="section-label">Step 1</div>
        <div class="section-title">Clinical Parameters</div>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1: Pregnancies            = st.text_input('Number of Pregnancies',        placeholder='e.g. 2')
        with col2: Glucose                = st.text_input('Glucose Level (mg/dL)',         placeholder='e.g. 120')
        with col3: BloodPressure          = st.text_input('Blood Pressure (mm Hg)',        placeholder='e.g. 70')
        with col1: SkinThickness          = st.text_input('Skin Thickness (mm)',           placeholder='e.g. 20')
        with col2: Insulin                = st.text_input('Insulin Level (μU/mL)',         placeholder='e.g. 85')
        with col3: BMI                    = st.text_input('BMI Value',                     placeholder='e.g. 28.5')
        with col1: DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function', placeholder='e.g. 0.47')
        with col2: Age                    = st.text_input('Age',                           placeholder='e.g. 35')

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, _ = st.columns([1, 2])
    with btn_col:
        if st.button('🔍  Run Diabetes Screening'):
            try:
                user_input = [float(x) for x in [
                    Pregnancies, Glucose, BloodPressure, SkinThickness,
                    Insulin, BMI, DiabetesPedigreeFunction, Age
                ]]
                pred = diabetes_model.predict([user_input])
                if pred[0] == 1:
                    st.markdown("""
                    <div class="result-danger">
                        <div class="result-icon">⚠️</div>
                        <div class="result-heading">Diabetes Detected</div>
                        <div class="result-body">The analysis indicates a <strong>positive result</strong> for diabetes. Please consult a qualified healthcare professional for a complete diagnosis and personalised treatment plan.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-heading">No Diabetes Detected</div>
                        <div class="result-body">The analysis shows <strong>no significant indicators</strong> of diabetes. Keep maintaining your healthy diet and active lifestyle!</div>
                    </div>""", unsafe_allow_html=True)
            except ValueError:
                st.warning("⚠️  Please fill in all 8 fields with valid numeric values before running the screening.")


# ══════════════════════════════════════════════════════════════════════════════
#  HEART DISEASE PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == 'Heart Disease':

    st.markdown("""
    <div class="hero" style="min-height:180px; padding:40px 52px;">
        <div class="hero-badge">❤️ Cardiovascular Screening</div>
        <div class="hero-title-sm">Heart Disease Prediction</div>
        <div class="hero-sub" style="margin-bottom:0;">Provide your cardiac measurements for an AI-powered cardiovascular risk assessment.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="input-section">
        <div class="section-label">Step 1</div>
        <div class="section-title">Cardiac Parameters</div>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: age      = st.text_input('Age',                              placeholder='e.g. 52')
    with col2: sex      = st.text_input('Sex  (1 = Male, 0 = Female)',      placeholder='e.g. 1')
    with col3: cp       = st.text_input('Chest Pain Type  (0 – 3)',         placeholder='e.g. 1')
    with col1: trestbps = st.text_input('Resting Blood Pressure',           placeholder='e.g. 130')
    with col2: chol     = st.text_input('Serum Cholesterol (mg/dL)',        placeholder='e.g. 245')
    with col3: fbs      = st.text_input('Fasting Blood Sugar > 120 mg/dL', placeholder='1=Yes  0=No')
    with col1: restecg  = st.text_input('Resting ECG Results  (0 – 2)',     placeholder='e.g. 1')
    with col2: thalach  = st.text_input('Max Heart Rate Achieved',          placeholder='e.g. 150')
    with col3: exang    = st.text_input('Exercise Induced Angina',          placeholder='1=Yes  0=No')
    with col1: oldpeak  = st.text_input('ST Depression (Exercise)',         placeholder='e.g. 1.5')
    with col2: slope    = st.text_input('Slope of Peak ST Segment',         placeholder='e.g. 2')
    with col3: ca       = st.text_input('Major Vessels Coloured  (0 – 3)',  placeholder='e.g. 0')
    with col1: thal     = st.text_input('Thal  (0=Normal 1=Fixed 2=Reversible)', placeholder='e.g. 2')

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, _ = st.columns([1, 2])
    with btn_col:
        if st.button('🔍  Run Heart Disease Screening'):
            try:
                user_input = [float(x) for x in [
                    age, sex, cp, trestbps, chol, fbs,
                    restecg, thalach, exang, oldpeak, slope, ca, thal
                ]]
                pred = heart_disease_model.predict([user_input])
                if pred[0] == 1:
                    st.markdown("""
                    <div class="result-danger">
                        <div class="result-icon">⚠️</div>
                        <div class="result-heading">Heart Disease Detected</div>
                        <div class="result-body">The analysis indicates <strong>cardiovascular risk factors</strong>. Please consult a cardiologist promptly for a thorough evaluation and personalised care plan.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-heading">No Heart Disease Detected</div>
                        <div class="result-body">The analysis shows <strong>no significant cardiovascular risk indicators</strong>. Keep up your heart-healthy habits — exercise, diet, and regular check-ups!</div>
                    </div>""", unsafe_allow_html=True)
            except ValueError:
                st.warning("⚠️  Please fill in all 13 fields with valid numeric values before running the screening.")


# ══════════════════════════════════════════════════════════════════════════════
#  PARKINSON'S PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif selected == "Parkinson's":

    st.markdown("""
    <div class="hero" style="min-height:180px; padding:40px 52px;">
        <div class="hero-badge">🧠 Neurological Screening</div>
        <div class="hero-title-sm">Parkinson's Prediction</div>
        <div class="hero-sub" style="margin-bottom:0;">Enter voice and acoustic measurements for an AI-powered neurological risk assessment.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="input-section">
        <div class="section-label">Step 1</div>
        <div class="section-title">Voice & Acoustic Parameters</div>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: fo            = st.text_input('MDVP : Fo (Hz)')
    with col2: fhi           = st.text_input('MDVP : Fhi (Hz)')
    with col3: flo           = st.text_input('MDVP : Flo (Hz)')
    with col4: Jitter_percent= st.text_input('MDVP : Jitter (%)')
    with col5: Jitter_Abs    = st.text_input('MDVP : Jitter (Abs)')
    with col1: RAP           = st.text_input('MDVP : RAP')
    with col2: PPQ           = st.text_input('MDVP : PPQ')
    with col3: DDP           = st.text_input('Jitter : DDP')
    with col4: Shimmer       = st.text_input('MDVP : Shimmer')
    with col5: Shimmer_dB    = st.text_input('MDVP : Shimmer (dB)')
    with col1: APQ3          = st.text_input('Shimmer : APQ3')
    with col2: APQ5          = st.text_input('Shimmer : APQ5')
    with col3: APQ           = st.text_input('MDVP : APQ')
    with col4: DDA           = st.text_input('Shimmer : DDA')
    with col5: NHR           = st.text_input('NHR')
    with col1: HNR           = st.text_input('HNR')
    with col2: RPDE          = st.text_input('RPDE')
    with col3: DFA           = st.text_input('DFA')
    with col4: spread1       = st.text_input('spread1')
    with col5: spread2       = st.text_input('spread2')
    with col1: D2            = st.text_input('D2')
    with col2: PPE           = st.text_input('PPE')

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col, _ = st.columns([1, 2])
    with btn_col:
        if st.button("🔍  Run Parkinson's Screening"):
            try:
                user_input = [float(x) for x in [
                    fo, fhi, flo, Jitter_percent, Jitter_Abs,
                    RAP, PPQ, DDP, Shimmer, Shimmer_dB,
                    APQ3, APQ5, APQ, DDA, NHR,
                    HNR, RPDE, DFA, spread1, spread2, D2, PPE
                ]]
                pred = parkinsons_model.predict([user_input])
                if pred[0] == 1:
                    st.markdown("""
                    <div class="result-danger">
                        <div class="result-icon">⚠️</div>
                        <div class="result-heading">Parkinson's Detected</div>
                        <div class="result-body">The analysis indicates <strong>signs of Parkinson's disease</strong>. Please consult a neurologist for a comprehensive evaluation and early intervention options.</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-heading">No Parkinson's Detected</div>
                        <div class="result-body">The analysis shows <strong>no significant indicators</strong> of Parkinson's disease. Continue maintaining your healthy and active lifestyle!</div>
                    </div>""", unsafe_allow_html=True)
            except ValueError:
                st.warning("⚠️  Please fill in all 22 fields with valid numeric values before running the screening.")
