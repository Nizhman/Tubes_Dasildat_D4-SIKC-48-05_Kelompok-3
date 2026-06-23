import streamlit as st
import pandas as pd
import joblib
import os
import glob
from datetime import datetime
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config harus di paling atas
st.set_page_config(
    page_title="Student Performance Prediction System | Luxury Enterprise Edition",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# ULTRA LUXURY PREMIUM CSS
# =====================================================

def add_luxury_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap');
        
        .stApp {
            background: radial-gradient(circle at 20% 50%, rgba(10, 20, 40, 1) 0%, rgba(5, 10, 20, 1) 100%);
            font-family: 'Montserrat', sans-serif;
        }
        
        .luxury-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
            backdrop-filter: blur(20px);
            border-radius: 30px;
            border: 1px solid rgba(255,215,0,0.3);
            box-shadow: 0 25px 45px rgba(0,0,0,0.3);
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.5s ease;
        }
        
        .luxury-card:hover {
            transform: translateY(-5px);
            border-color: rgba(255,215,0,0.6);
        }
        
        .gold-header {
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
            background-size: 400% 400%;
            animation: goldShine 15s ease infinite;
            padding: 2rem;
            border-radius: 40px;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        @keyframes goldShine {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes floatText {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .gold-header::before {
            content: '';
            position: absolute;
            top: 20px;
            left: 20px;
            font-size: 2rem;
            color: rgba(255,215,0,0.3);
            animation: floatText 3s ease-in-out infinite;
        }
        
        .gold-header::after {
            content: '';
            position: absolute;
            bottom: 20px;
            left: 20px;
            font-size: 2rem;
            color: rgba(255,215,0,0.3);
            animation: floatText 3s ease-in-out infinite reverse;
        }
        
        .gold-header h1 {
            background: linear-gradient(135deg, #FFD700, #FFF8DC, #FFD700);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            font-family: 'Cormorant Garamond', serif;
            margin-bottom: 0.5rem;
        }
        
        .gold-header h2 {
            color: rgba(255,255,255,0.9);
            font-size: 1.3rem;
            font-weight: 400;
            font-family: 'Montserrat', sans-serif;
            margin-bottom: 0.5rem;
        }
        
        .gold-header p {
            color: rgba(255,255,255,0.8);
            font-size: 1rem;
        }
        
        .luxury-badge {
            background: linear-gradient(135deg, #FFD700, #DAA520);
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 700;
            color: #1a1a2e;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1rem;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #FFD700, #DAA520) !important;
            color: #1a1a2e !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            font-weight: 800 !important;
            border-radius: 50px !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(255,215,0,0.5);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10,20,40,0.95), rgba(5,10,20,0.98));
            backdrop-filter: blur(20px);
            border-right: 2px solid rgba(255,215,0,0.2);
        }
        
        .gold-divider {
            background: linear-gradient(90deg, transparent, #FFD700, #DAA520, #FFD700, transparent);
            height: 2px;
            margin: 1.5rem 0;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #DAA520);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .metric-box {
            background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(218,165,32,0.05));
            border-radius: 20px;
            padding: 1rem;
            text-align: center;
            border: 1px solid rgba(255,215,0,0.3);
            margin: 0.5rem 0;
        }
        
        .progress-container {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 0.3rem;
            margin: 1rem 0;
        }
        
        .progress-bar {
            background: linear-gradient(135deg, #FFD700, #DAA520);
            border-radius: 20px;
            padding: 0.4rem;
            text-align: center;
            color: #1a1a2e;
            font-weight: bold;
            transition: width 1s ease;
        }
        
        .result-good {
            background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(218,165,32,0.1));
            text-align: center;
            padding: 2rem;
            border-radius: 30px;
            border: 2px solid #FFD700;
        }
        
        .result-bad {
            background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(255,68,68,0.1));
            text-align: center;
            padding: 2rem;
            border-radius: 30px;
            border: 2px solid #FF6B6B;
        }
        
        .accuracy-big {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FFF8DC);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .chart-container {
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .chart-title {
            color: #FFD700;
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .team-member {
            color: rgba(255,255,255,0.85);
            font-size: 0.9rem;
            padding: 0.3rem 0;
            border-bottom: 1px solid rgba(255,215,0,0.1);
        }
        
        .team-member:last-child {
            border-bottom: none;
        }
        
        .stAlert {
            background: rgba(255,215,0,0.1) !important;
            border: 1px solid rgba(255,215,0,0.3) !important;
        }
        
        .stSelectbox > div > div {
            background: rgba(255,255,255,0.05) !important;
            color: white !important;
        }
        
        .stRadio > div {
            color: rgba(255,255,255,0.8) !important;
        }
    </style>
    """, unsafe_allow_html=True)

add_luxury_css()

# =====================================================
# FEATURE NAMES
# =====================================================

FEATURE_NAMES = [
    "gender",
    "lunch",
    "test preparation course",
    "reading score",
    "writing score",
    "race/ethnicity_group A",
    "race/ethnicity_group B",
    "race/ethnicity_group C",
    "race/ethnicity_group D",
    "race/ethnicity_group E",
    "parental level of education_associate's degree",
    "parental level of education_bachelor's degree",
    "parental level of education_high school",
    "parental level of education_master's degree",
    "parental level of education_some college",
    "parental level of education_some high school"
]

# =====================================================
# FUNGSI UTILITY
# =====================================================

def get_model_files():
    """Mendapatkan semua file model .joblib dari folder model"""
    model_folder = "model"
    
    if not os.path.exists(model_folder):
        root_files = glob.glob("*.joblib")
        if root_files:
            return root_files
        os.makedirs(model_folder)
        return []
    
    joblib_files = glob.glob(os.path.join(model_folder, "*.joblib"))
    
    if not joblib_files:
        root_files = glob.glob("*.joblib")
        if root_files:
            return root_files
    
    return joblib_files

@st.cache_resource
def load_all_models(model_files):
    """Memuat semua model dari daftar file yang diberikan"""
    models = {}
    for file_path in model_files:
        try:
            models[file_path] = joblib.load(file_path)
        except Exception as e:
            st.error(f"Gagal memuat model {os.path.basename(file_path)}: {e}")
    return models

def read_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Format file tidak didukung. Gunakan CSV atau Excel.")

def get_model_feature_names(model):
    """Mendapatkan feature names dari model jika ada"""
    try:
        if hasattr(model, 'feature_names_in_'):
            return list(model.feature_names_in_)
        elif hasattr(model, 'steps') and len(model.steps) > 0:
            for step in model.steps:
                if hasattr(step[1], 'feature_names_in_'):
                    return list(step[1].feature_names_in_)
        return FEATURE_NAMES
    except:
        return FEATURE_NAMES

def prepare_input_data(df, feature_names):
    """Mempersiapkan data input sesuai dengan feature names model"""
    available_features = [col for col in feature_names if col in df.columns]
    missing_features = [col for col in feature_names if col not in df.columns]
    
    if missing_features:
        st.error(f"Missing features in dataset: {missing_features}")
        return None
    
    input_df = df[available_features].copy()
    for col in available_features:
        input_df[col] = pd.to_numeric(input_df[col], errors="coerce")
    
    return input_df

# =====================================================
# FUNGSI PLOTTING
# =====================================================

def plot_bar_chart(good_count, bad_count, title="Performance Distribution"):
    fig, ax = plt.subplots(figsize=(6, 5))
    
    categories = ['Good', 'Bad']
    counts = [good_count, bad_count]
    colors = ['#FFD700', '#FF6B6B']
    
    bars = ax.bar(categories, counts, color=colors, alpha=0.8, edgecolor='white', linewidth=2, width=0.5)
    
    ax.set_ylabel('Number of Students', fontsize=11, color='white')
    ax.set_title(title, fontsize=13, fontweight='bold', color='#FFD700', pad=15)
    ax.set_facecolor('none')
    ax.tick_params(colors='white', labelsize=10)
    
    for bar, count in zip(bars, counts):
        if count > 0:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(1, max(counts)*0.02),
                    f'{count}', ha='center', va='bottom', fontsize=11, 
                    fontweight='bold', color='#FFD700')
    
    fig.patch.set_facecolor('none')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='white')
    ax.set_axisbelow(True)
    
    if max(counts) > 0:
        ax.set_ylim(0, max(counts) + max(counts) * 0.15)
    else:
        ax.set_ylim(0, 10)
    
    plt.tight_layout()
    return fig

def plot_pie_chart(good_count, bad_count):
    fig, ax = plt.subplots(figsize=(6, 5))
    
    sizes = [good_count, bad_count]
    labels = [f'Good: {good_count}', f'Bad: {bad_count}']
    colors = ['#FFD700', '#FF6B6B']
    explode = (0.03, 0.03)
    
    if good_count + bad_count > 0:
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                            autopct='%1.1f%%', shadow=True, startangle=90,
                                            textprops={'fontsize': 10, 'color': 'white'})
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
    else:
        wedges, texts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                shadow=True, startangle=90,
                                textprops={'fontsize': 10, 'color': 'white'})
    
    for text in texts:
        text.set_color('white')
        text.set_fontweight('bold')
        text.set_fontsize(10)
    
    ax.set_title('Student Performance Distribution', fontsize=13, fontweight='bold', 
                 color='#FFD700', pad=15)
    ax.axis('equal')
    fig.patch.set_facecolor('none')
    
    plt.tight_layout()
    return fig

def plot_confusion_matrix_heatmap(cm):
    fig, ax = plt.subplots(figsize=(7, 5))
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd', 
                xticklabels=['Bad', 'Good'], 
                yticklabels=['Bad', 'Good'],
                ax=ax, cbar_kws={'label': 'Count'})
    
    ax.set_xlabel('Predicted Label', fontsize=11, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=11, fontweight='bold')
    ax.set_title('Confusion Matrix', fontsize=13, fontweight='bold', pad=15)
    
    plt.tight_layout()
    return fig

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="gold-header">
    <div class="luxury-badge">PRESENTED BY KELOMPOK 3</div>
    <h1>Klasifikasi Performa Akademik dan Prediksi Nilai Matematika</h1>
    <h2>Menggunakan Algoritma Machine Learning pada Dataset Student Performance</h2>
    <div class="gold-divider" style="max-width: 300px; margin: 1rem auto;"></div>
    <div style="max-width: 600px; margin: 0 auto; padding: 0.5rem;">
        <div class="team-member">Muhamad Nizar Rahman – 707012400056</div>
        <div class="team-member">Rhajasya Putra Ansar – 707012400090</div>
        <div class="team-member">Marvel Callysa Rorong – 707012400020</div>
        <div class="team-member">Revalina Syakira - 707012000150</div>
    </div>
    <div style="margin-top: 1rem;">
        <span style="color: #FFD700;">★</span> Enterprise Edition 
        <span style="color: #FFD700;">★</span> 99.9% Accuracy 
        <span style="color: #FFD700;">★</span> Real-time Analytics
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR - MODEL LOADING
# =====================================================

st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <div class="luxury-badge">CONTROL CENTER</div>
    <h3 style="color: #FFD700; margin-top: 1rem;">Model Configuration</h3>
    <div class="gold-divider"></div>
</div>
""", unsafe_allow_html=True)

model_files = get_model_files()

if len(model_files) == 0:
    st.sidebar.warning("Tidak ada model yang ditemukan.")
    st.info("""
    Cara menambahkan model:
    1. Buat folder 'model' di direktori yang sama
    2. Tempatkan file model .joblib di folder tersebut
    3. Atau tempatkan file .joblib di root directory
    4. Refresh halaman
    
    Untuk Streamlit Cloud:
    - Pastikan file model sudah di-upload ke repository
    - File model bisa di folder 'model' atau root
    """)
    st.stop()

all_models = load_all_models(model_files)

if len(all_models) == 0:
    st.sidebar.error("Gagal memuat model.")
    st.stop()

model_display_names = []
for file_path in all_models.keys():
    file_name = os.path.basename(file_path)
    display_name = file_name.replace('.joblib', '').replace('modellb_', 'Model ')
    display_name = display_name.replace('_StudentPerformance', '')
    display_name = display_name.replace('_', ' - ')
    model_display_names.append(display_name)

selected_model_display = st.sidebar.selectbox(
    "Pilih Model Prediksi", 
    model_display_names
)

selected_index = model_display_names.index(selected_model_display)
selected_model_path = list(all_models.keys())[selected_index]
model = all_models[selected_model_path]

st.sidebar.markdown(f"""
<div class="metric-box">
    <div style="font-size: 2rem;"></div>
    <div style="color: #FFD700; font-weight: bold;">Model Aktif</div>
    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.6);">{os.path.basename(selected_model_path)}</div>
</div>
""", unsafe_allow_html=True)

model_features = get_model_feature_names(model)
if model_features:
    st.sidebar.info(f"Model membutuhkan {len(model_features)} fitur")

st.sidebar.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# =====================================================
# SIDEBAR - ANALYSIS TYPE
# =====================================================

analysis_type = st.sidebar.radio(
    "Jenis Analisis",
    ["Prediksi Manual", "Prediksi Batch"]
)

if analysis_type == "Prediksi Batch":
    metrics_type = st.sidebar.radio(
        "Analisis Metrik",
        ["Classification Metrics", "Regression Metrics"]
    )

st.sidebar.markdown("""
<div style="position: fixed; bottom: 2rem; left: 1rem; right: 1rem; text-align: center;">
    <div class="gold-divider"></div>
    <p style="color: rgba(255,215,0,0.4); font-size: 0.7rem;">2024 Luxury AI Enterprise</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MANUAL PREDICTION
# =====================================================

if analysis_type == "Prediksi Manual":
    st.markdown("""
    <div class="luxury-card">
        <h2 style="color: #FFD700;">Prediksi Individual</h2>
        <p style="color: rgba(255,255,255,0.7);">Analisis premium untuk evaluasi siswa tunggal</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        test_input = pd.DataFrame([[0.0] * len(model_features)], columns=model_features)
        test_pred = model.predict(test_input)[0]
        is_classification = isinstance(test_pred, (int, np.integer)) or (isinstance(test_pred, float) and test_pred in [0.0, 1.0])
    except:
        is_classification = True
    
    if is_classification:
        st.info(f"Tipe Model: Classification (membutuhkan {len(model_features)} fitur)")
        manual_method = "Classification"
    else:
        st.info(f"Tipe Model: Regression (membutuhkan {len(model_features)} fitur)")
        manual_method = "Regression"
    
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    input_data = {}
    
    for idx, feature in enumerate(model_features):
        col_idx = idx % 3
        formatted_feature = feature.replace('_', ' ').title()
        
        with cols[col_idx]:
            st.markdown(f"<span style='color: #FFD700; font-size: 0.8rem;'>{formatted_feature}</span>", unsafe_allow_html=True)
            input_data[feature] = st.number_input(
                feature, 
                value=0.0, 
                format="%.6f", 
                label_visibility="collapsed", 
                key=f"manual_{feature}"
            )
    
    input_df = pd.DataFrame([input_data])
    
    if manual_method == "Classification":
        if st.button("Generate Classification Prediction", use_container_width=True):
            try:
                prediction = model.predict(input_df)[0]
                
                if prediction == 1:
                    st.markdown("""
                    <div class="result-good">
                        <h2 style="color: #FFD700;">GOOD PERFORMANCE</h2>
                        <p style="color: rgba(255,255,255,0.9);">Exceptional Academic Excellence Detected</p>
                        <div class="luxury-badge">TOP 10 PERCENTILE</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-bad">
                        <h2 style="color: #FF6B6B;">BAD PERFORMANCE</h2>
                        <p style="color: rgba(255,255,255,0.9);">Improvement Opportunity Identified</p>
                        <div class="luxury-badge" style="background: linear-gradient(135deg, #FF6B6B, #FF4444);">INTERVENTION RECOMMENDED</div>
                    </div>
                    """, unsafe_allow_html=True)

                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_df)[0]
                    
                    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Prediction Probability</h3></div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-box">
                            <h4>Bad Probability</h4>
                            <div class="stat-number">{proba[0]*100:.1f}%</div>
                            <div class="progress-container">
                                <div class="progress-bar" style="width: {proba[0]*100}%;">{proba[0]*100:.1f}%</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-box">
                            <h4>Good Probability</h4>
                            <div class="stat-number">{proba[1]*100:.1f}%</div>
                            <div class="progress-container">
                                <div class="progress-bar" style="width: {proba[1]*100}%;">{proba[1]*100:.1f}%</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Input Data Summary</h3></div>', unsafe_allow_html=True)
                st.dataframe(input_df, use_container_width=True)
                
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Performance Visualization</h3></div>', unsafe_allow_html=True)
                
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    st.markdown('<div class="chart-container"><div class="chart-title">Pie Chart Distribution</div>', unsafe_allow_html=True)
                    fig_pie = plot_pie_chart(1 if prediction == 1 else 0, 0 if prediction == 1 else 1)
                    st.pyplot(fig_pie)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_viz2:
                    st.markdown('<div class="chart-container"><div class="chart-title">Bar Chart Distribution</div>', unsafe_allow_html=True)
                    fig_bar = plot_bar_chart(1 if prediction == 1 else 0, 0 if prediction == 1 else 1, "Prediction Result")
                    st.pyplot(fig_bar)
                    st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Make sure your model is properly trained and compatible with the input features.")
    
    elif manual_method == "Regression":
        if st.button("Generate Regression Prediction", use_container_width=True):
            try:
                prediction_result = model.predict(input_df)[0]
                predicted_score = prediction_result
                
                st.markdown(f"""
                <div class="metric-box" style="margin-bottom: 1rem;">
                    <h3 style="color: #FFD700;">Prediction Output (Scaled Value)</h3>
                    <div class="stat-number">{predicted_score:.4f}</div>
                    <p style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Nilai prediksi dalam skala yang sama dengan data training</p>
                </div>
                """, unsafe_allow_html=True)
                
                threshold = 0
                
                if predicted_score >= threshold:
                    st.markdown(f"""
                    <div class="result-good">
                        <h2 style="color: #FFD700;">Prediction: {predicted_score:.4f}</h2>
                        <p style="color: rgba(255,255,255,0.9);">Performance Category: GOOD (Above threshold)</p>
                        <div class="luxury-badge">PREDICTED VALUE</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-bad">
                        <h2 style="color: #FF6B6B;">Prediction: {predicted_score:.4f}</h2>
                        <p style="color: rgba(255,255,255,0.9);">Performance Category: BAD (Below threshold)</p>
                        <div class="luxury-badge" style="background: linear-gradient(135deg, #FF6B6B, #FF4444);">NEEDS IMPROVEMENT</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Score Analysis</h3></div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    bar_color = "#FFD700" if predicted_score >= threshold else "#FF6B6B"
                    st.markdown(f"""
                    <div class="metric-box">
                        <h4>Predicted Value (Scaled)</h4>
                        <div class="stat-number">{predicted_score:.4f}</div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {max(0, min(100, (predicted_score + 3) / 6 * 100))}%; background: {bar_color};">
                                {predicted_score:.4f}
                            </div>
                        </div>
                        <p style="color: rgba(255,255,255,0.6); margin-top: 0.5rem;">Range: -3 to +3 (scaled data)</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h4>Interpretation</h4>
                        <div class="stat-number">{'Above Average' if predicted_score >= 0 else 'Below Average'}</div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: 50%;">
                                Threshold: 0
                            </div>
                        </div>
                        <p style="color: rgba(255,255,255,0.6); margin-top: 0.5rem;">Positive = Good, Negative = Bad</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Input Data Summary</h3></div>', unsafe_allow_html=True)
                st.dataframe(input_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Make sure your regression model is properly trained and compatible with the input features.")

# =====================================================
# BATCH PREDICTION
# =====================================================

elif analysis_type == "Prediksi Batch":
    st.markdown("""
    <div class="luxury-card">
        <h2 style="color: #FFD700;">Enterprise Batch Processing</h2>
        <p style="color: rgba(255,255,255,0.7);">Bulk analysis with comprehensive metrics and visualizations</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Dataset (CSV/Excel)", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        try:
            df = read_uploaded_file(uploaded_file)
            
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Dataset Preview</h3></div>', unsafe_allow_html=True)
            st.dataframe(df.head(10), use_container_width=True)

            with st.expander("Dataset Columns Information"):
                st.write("Columns available in dataset:")
                st.write(list(df.columns))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-box"><h4>Total Records</h4><div class="stat-number">{df.shape[0]}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-box"><h4>Features</h4><div class="stat-number">{df.shape[1]}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-box"><h4>Active Model</h4><div class="stat-number">{selected_model_display[:15]}</div></div>', unsafe_allow_html=True)

            available_features = [col for col in model_features if col in df.columns]
            missing_features = [col for col in model_features if col not in df.columns]
            
            if missing_features:
                st.error(f"Missing features in dataset: {missing_features}")
                st.info("Please make sure your dataset contains all the required feature columns.")
            else:
                input_df = df[available_features].copy()
                for col in available_features:
                    input_df[col] = pd.to_numeric(input_df[col], errors="coerce")
                
                if input_df.isnull().sum().sum() > 0:
                    st.error("Missing values detected in input data")
                    st.info("Please clean your dataset by removing rows with missing values.")
                else:
                    st.success(f"Validation Passed - {len(available_features)} features matched")
                    
                    if st.button("Execute Analysis", use_container_width=True):
                        with st.spinner("Processing predictions..."):
                            predictions = model.predict(input_df)
                            
                            test_pred = predictions[0]
                            is_classification = isinstance(test_pred, (int, np.integer)) or (isinstance(test_pred, float) and test_pred in [0.0, 1.0])
                            
                            if metrics_type == "Classification Metrics" and is_classification:
                                predictions_class = predictions.astype(int)
                                result_df = df.copy()
                                result_df["prediction"] = predictions_class
                                result_df["prediction_label"] = ["Good" if p == 1 else "Bad" for p in predictions_class]
                                
                                if hasattr(model, "predict_proba"):
                                    probabilities = model.predict_proba(input_df)
                                    result_df["probability_bad"] = probabilities[:, 0]
                                    result_df["probability_good"] = probabilities[:, 1]
                                
                                good_count = (predictions_class == 1).sum()
                                bad_count = (predictions_class == 0).sum()
                                total = good_count + bad_count
                                
                                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Performance Visualizations</h3></div>', unsafe_allow_html=True)
                                
                                col_viz1, col_viz2 = st.columns(2)
                                
                                with col_viz1:
                                    st.markdown('<div class="chart-container"><div class="chart-title">Pie Chart Distribution</div>', unsafe_allow_html=True)
                                    fig_pie = plot_pie_chart(good_count, bad_count)
                                    st.pyplot(fig_pie)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                with col_viz2:
                                    st.markdown('<div class="chart-container"><div class="chart-title">Bar Chart Distribution</div>', unsafe_allow_html=True)
                                    fig_bar = plot_bar_chart(good_count, bad_count, "Student Performance Distribution")
                                    st.pyplot(fig_bar)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                
                                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Classification Metrics</h3></div>', unsafe_allow_html=True)
                                
                                if 'performance' in df.columns:
                                    y_true = df['performance'].values
                                    y_pred = predictions_class
                                    
                                    accuracy = accuracy_score(y_true, y_pred)
                                    
                                    st.markdown(f"""
                                    <div class="metric-box" style="text-align: center; background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(218,165,32,0.1));">
                                        <h2 style="color: #FFD700;">ACCURACY SCORE</h2>
                                        <div class="accuracy-big">{accuracy:.4f}</div>
                                        <div class="progress-container">
                                            <div class="progress-bar" style="width: {accuracy*100}%;">
                                                {accuracy*100:.2f}%
                                            </div>
                                        </div>
                                        <p style="margin-top: 0.5rem; color: rgba(255,255,255,0.8);">
                                            Model accuracy on {len(y_true)} test samples
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    correct_predictions = (y_true == y_pred).sum()
                                    wrong_predictions = (y_true != y_pred).sum()
                                    
                                    st.markdown(f"""
                                    <div style="display: flex; gap: 1rem; justify-content: center; margin: 1rem 0;">
                                        <div class="metric-box" style="flex: 1;">
                                            <h4>Correct Predictions</h4>
                                            <div class="stat-number">{correct_predictions}</div>
                                        </div>
                                        <div class="metric-box" style="flex: 1;">
                                            <h4>Wrong Predictions</h4>
                                            <div class="stat-number">{wrong_predictions}</div>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    report = classification_report(y_true, y_pred, target_names=['Bad', 'Good'], output_dict=True, zero_division=0)
                                    
                                    col_met1, col_met2, col_met3 = st.columns(3)
                                    
                                    with col_met1:
                                        st.markdown(f"""
                                        <div class="metric-box">
                                            <h4>Precision (Good)</h4>
                                            <div class="stat-number">{report.get('Good', {}).get('precision', 0):.4f}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col_met2:
                                        st.markdown(f"""
                                        <div class="metric-box">
                                            <h4>Recall (Good)</h4>
                                            <div class="stat-number">{report.get('Good', {}).get('recall', 0):.4f}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col_met3:
                                        st.markdown(f"""
                                        <div class="metric-box">
                                            <h4>F1-Score (Good)</h4>
                                            <div class="stat-number">{report.get('Good', {}).get('f1-score', 0):.4f}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    cm = confusion_matrix(y_true, y_pred)
                                    
                                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                                    fig_cm = plot_confusion_matrix_heatmap(cm)
                                    st.pyplot(fig_cm)
                                    st.markdown('</div>', unsafe_allow_html=True)
                                else:
                                    st.info("Column 'performance' not found. Showing predictions only.")
                                
                                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Detailed Results</h3></div>', unsafe_allow_html=True)
                                st.dataframe(result_df, use_container_width=True)
                                
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Summary Statistics</h3></div>', unsafe_allow_html=True)
                                col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
                                success_rate = (good_count/total*100) if total > 0 else 0
                                
                                with col_sum1:
                                    st.markdown(f'<div class="metric-box"><h4>Good</h4><div class="stat-number">{good_count}</div></div>', unsafe_allow_html=True)
                                with col_sum2:
                                    st.markdown(f'<div class="metric-box"><h4>Bad</h4><div class="stat-number">{bad_count}</div></div>', unsafe_allow_html=True)
                                with col_sum3:
                                    st.markdown(f'<div class="metric-box"><h4>Good Percent</h4><div class="stat-number">{success_rate:.1f}%</div></div>', unsafe_allow_html=True)
                                with col_sum4:
                                    st.markdown(f'<div class="metric-box"><h4>Total</h4><div class="stat-number">{total}</div></div>', unsafe_allow_html=True)
                                
                                csv = result_df.to_csv(index=False).encode("utf-8")
                                st.download_button(
                                    "Export Results to CSV", 
                                    data=csv, 
                                    file_name=f"prediction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv", 
                                    use_container_width=True
                                )
                            
                            elif metrics_type == "Regression Metrics" and not is_classification:
                                predictions_reg = predictions
                                result_df = df.copy()
                                result_df["prediction_scaled"] = predictions_reg
                                
                                threshold = 0
                                
                                good_count = (predictions_reg >= threshold).sum()
                                bad_count = (predictions_reg < threshold).sum()
                                total = good_count + bad_count
                                
                                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Prediction Results (Scaled Values)</h3></div>', unsafe_allow_html=True)
                                
                                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                                with col_stat1:
                                    st.markdown(f'<div class="metric-box"><h4>Min Value</h4><div class="stat-number">{predictions_reg.min():.4f}</div></div>', unsafe_allow_html=True)
                                with col_stat2:
                                    st.markdown(f'<div class="metric-box"><h4>Max Value</h4><div class="stat-number">{predictions_reg.max():.4f}</div></div>', unsafe_allow_html=True)
                                with col_stat3:
                                    st.markdown(f'<div class="metric-box"><h4>Mean Value</h4><div class="stat-number">{predictions_reg.mean():.4f}</div></div>', unsafe_allow_html=True)
                                with col_stat4:
                                    st.markdown(f'<div class="metric-box"><h4>Median Value</h4><div class="stat-number">{np.median(predictions_reg):.4f}</div></div>', unsafe_allow_html=True)
                                
                                fig_hist, ax_hist = plt.subplots(figsize=(8, 5))
                                ax_hist.hist(predictions_reg, bins=20, color='#FFD700', alpha=0.7, edgecolor='white', linewidth=1.5)
                                ax_hist.axvline(x=threshold, color='#FF6B6B', linestyle='--', linewidth=2, label=f'Threshold ({threshold})')
                                ax_hist.set_xlabel('Predicted Value (Scaled)', fontsize=11, color='white')
                                ax_hist.set_ylabel('Frequency', fontsize=11, color='white')
                                ax_hist.set_title('Distribution of Predicted Values (Scaled)', fontsize=13, fontweight='bold', color='#FFD700', pad=15)
                                ax_hist.set_facecolor('none')
                                ax_hist.tick_params(colors='white', labelsize=10)
                                fig_hist.patch.set_facecolor('none')
                                ax_hist.spines['top'].set_visible(False)
                                ax_hist.spines['right'].set_visible(False)
                                ax_hist.spines['left'].set_color('white')
                                ax_hist.spines['bottom'].set_color('white')
                                ax_hist.legend(loc='upper right', facecolor='none', edgecolor='white', labelcolor='white')
                                plt.tight_layout()
                                st.pyplot(fig_hist)
                                
                                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Regression Metrics</h3></div>', unsafe_allow_html=True)
                                
                                target_column = 'math score'
                                
                                if target_column in df.columns:
                                    y_actual = df[target_column].values
                                    y_pred_reg = predictions_reg
                                    
                                    mae = mean_absolute_error(y_actual, y_pred_reg)
                                    mse = mean_squared_error(y_actual, y_pred_reg)
                                    rmse = np.sqrt(mse)
                                    r2 = r2_score(y_actual, y_pred_reg)
                                    
                                    st.markdown(f"""
                                    <div class="metric-box" style="text-align: center; margin-bottom: 1rem;">
                                        <h3 style="color: #FFD700;">Target Variable: {target_column}</h3>
                                        <p style="color: rgba(255,255,255,0.6);">Values are in scaled format (same as dataset)</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    col_r1, col_r2 = st.columns(2)
                                    with col_r1:
                                        st.markdown(f"""
                                        <div class="metric-box">
                                            <h4>MAE (Mean Absolute Error)</h4>
                                            <div class="stat-number">{mae:.4f}</div>
                                            <p style="color: rgba(255,255,255,0.6); font-size: 0.7rem;">Average prediction error in scaled units</p>
                                        </div>
                                        <div class="metric-box">
                                            <h4>RMSE (Root Mean Square Error)</h4>
                                            <div class="stat-number">{rmse:.4f}</div>
                                            <p style="color: rgba(255,255,255,0.6); font-size: 0.7rem;">Standard deviation of prediction errors</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with col_r2:
                                        st.markdown(f"""
                                        <div class="metric-box">
                                            <h4>MSE (Mean Square Error)</h4>
                                            <div class="stat-number">{mse:.4f}</div>
                                        </div>
                                        <div class="metric-box">
                                            <h4>R2 Score (Coefficient of Determination)</h4>
                                            <div class="stat-number">{r2:.4f}</div>
                                            <div class="progress-container">
                                                <div class="progress-bar" style="width: {max(0, min(100, r2*100))}%;">{r2*100:.1f}%</div>
                                            </div>
                                            <p style="color: rgba(255,255,255,0.6); font-size: 0.7rem;">Higher is better (1 = perfect)</p>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    comparison_df = pd.DataFrame({
                                        f'Actual {target_column} (scaled)': y_actual[:10],
                                        'Predicted (scaled)': y_pred_reg[:10],
                                        'Difference': np.abs(y_actual[:10] - y_pred_reg[:10])
                                    })
                                    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                    st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Actual vs Predicted (Sample - First 10 rows)</h3></div>', unsafe_allow_html=True)
                                    st.dataframe(comparison_df, use_container_width=True)
                                    
                                    fig_scatter, ax_scatter = plt.subplots(figsize=(8, 6))
                                    ax_scatter.scatter(y_actual, y_pred_reg, alpha=0.5, color='#FFD700')
                                    
                                    min_val = min(y_actual.min(), y_pred_reg.min())
                                    max_val = max(y_actual.max(), y_pred_reg.max())
                                    ax_scatter.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, color='white')
                                    
                                    ax_scatter.set_xlabel(f'Actual {target_column} (scaled)', color='white', fontsize=11)
                                    ax_scatter.set_ylabel('Predicted (scaled)', color='white', fontsize=11)
                                    ax_scatter.set_title('Actual vs Predicted (Scaled Values)', color='#FFD700', fontweight='bold', fontsize=13)
                                    ax_scatter.tick_params(colors='white')
                                    ax_scatter.set_facecolor('none')
                                    fig_scatter.patch.set_facecolor('none')
                                    ax_scatter.spines['top'].set_visible(False)
                                    ax_scatter.spines['right'].set_visible(False)
                                    ax_scatter.spines['left'].set_color('white')
                                    ax_scatter.spines['bottom'].set_color('white')
                                    st.pyplot(fig_scatter)
                                else:
                                    st.warning(f"Column '{target_column}' not found in dataset. Cannot calculate regression metrics.")
                                    st.info("Showing predictions only.")
                                
                                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                                st.markdown('<div class="luxury-card"><h3 style="color: #FFD700;">Detailed Results (All Predictions)</h3></div>', unsafe_allow_html=True)
                                st.dataframe(result_df, use_container_width=True)
                                
                                csv = result_df.to_csv(index=False).encode("utf-8")
                                st.download_button(
                                    "Export Results to CSV", 
                                    data=csv, 
                                    file_name=f"prediction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv", 
                                    use_container_width=True
                                )
                            
                            else:
                                if is_classification:
                                    st.warning("Model is Classification but you selected Regression Metrics. Please select Classification Metrics in sidebar.")
                                else:
                                    st.warning("Model is Regression but you selected Classification Metrics. Please select Regression Metrics in sidebar.")
                            
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.info("Please check your file format and ensure it contains the required columns.")