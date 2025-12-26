import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="YTU Glass Calculator",
    page_icon="⚗️",
    layout="wide"
)

# --- CSS: SİYAH YAZI VE TEMİZ GÖRÜNÜM ---
st.markdown("""
    <style>
    /* Genel Ayarlar */
    .stApp { background-color: #ffffff; color: #000000; }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div, span, th, td { color: #000000 !important; }
    
    /* Inputlar */
    .stNumberInput input { color: #000000 !important; background-color: #f0f2f6 !important; font-weight: bold; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #ddd; }
    
    /* Butonlar */
    .stButton button { width: 100%; border-radius: 5px; font-weight: bold; }

    /* Başlık Kutusu */
    .header-box {
        background: linear-gradient(90deg, #1d3557 0%, #457b9d 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        color: white !important;
    }
    .header-box h2, .header-box div { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK ---
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.markdown("""
    <div class="header-box">
        <h2>YTU GLASS RESEARCH GROUP</h2>
        <div style="font-size: 1rem;">Batch Calculator v8.1 (Final)</div>
    </div>
    """, unsafe_allow_html=True)

# --- VERİ TABANI ---
materials_db = {
    "SiO2":    {"raw": "SiO2",      "mw": 60.0900,  "factor": 1.0, "oxide_mw": 60.0900},
    "Na2O":    {"raw": "Na2CO3",    "mw": 105.9800, "factor": 1.0, "oxide_mw": 61.9700},
    "Al2O3":   {"raw": "Al2O3",     "mw": 101.9600, "factor": 1.0, "oxide_mw": 101.9600},
    "ZnO":     {"raw": "ZnO",       "mw": 81.3700,  "factor": 1.0, "oxide_mw": 81.3700},
    "CaO":     {"raw": "CaCO3",     "mw": 100.0869, "factor": 1.0, "oxide_mw": 56.0774},
    "TeO2":    {"raw": "TeO2",      "mw": 159.6000, "factor": 1.0, "oxide_mw": 159.6000},
    "B2O3":    {"raw": "H3BO3",     "mw": 61.8300,  "factor": 2.0, "oxide_mw": 69.6100},
    "NaF":     {"raw": "NaF",       "mw": 41.9900,  "factor": 1.0, "oxide_mw": 41.9900},
    "KBr":     {"raw": "KBr",       "mw": 119.0100, "factor": 1.0, "oxide_mw": 119.0100},
    "SnO2":    {"raw": "SnO2",      "mw": 150.6900, "factor": 1.0, "oxide_mw": 150.6900},
    "PbO":     {"raw": "PbO",       "mw": 223.1900, "factor": 1.0, "oxide_mw": 223.1900},
    "NaBr":    {"raw": "NaBr",      "mw": 102.3900, "factor": 1.0, "oxide_mw": 102.3900},
    "NaCl":    {"raw": "NaCl",      "mw": 58.4400,  "factor": 1.0, "oxide_mw": 58.4400},
    "GeO2":    {"raw": "GeO2",      "mw": 104.6100, "factor": 1.0, "oxide_mw": 104.6100},
    "WO3":     {"raw": "WO3",       "mw": 231.8500, "factor": 1.0, "oxide_mw": 231.8500},
    "Li2O":    {"raw": "Li2CO3",    "mw": 73.8900,  "factor": 1.0, "oxide_mw": 29.8800},
    "Bi2O3":   {"raw": "Bi2O3",     "mw": 465.9600, "factor": 1.0, "oxide_mw": 465.9600},
    "BaO":     {"raw": "BaCO3",     "mw": 197.3400, "factor": 1.0, "oxide_mw": 153.3300},
    "TiO2":    {"raw": "TiO2",      "mw": 79.8660,  "factor": 1.0, "oxide_mw": 79.8660},
    "P2O5":    {"raw": "P2O5",      "mw": 141.9400, "factor": 1.0, "oxide_mw": 141.9400},
    "Ho2O3":   {"raw": "Ho2O3",     "mw": 377.8600, "factor": 1.0, "oxide_mw": 377.8600},
    "Tm2O3":   {"raw": "Tm2O3",     "mw": 385.8700, "factor": 1.0, "oxide_mw": 385.8700},
    "Sm2O3":   {"raw": "Sm2O3",     "mw": 348.7200, "factor": 1.0, "oxide_mw": 348.7200},
    "Er2O3":   {"raw": "Er2O3",     "mw": 382.5200, "factor": 1.0, "oxide_mw": 382.5200},
    "Nd2O3":   {"raw": "Nd2O3",     "mw": 336.4800, "factor": 1.0, "oxide_mw": 336.4800},
    "Yb2O3":   {"raw": "Yb2O3",     "mw": 394.0800, "factor": 1.0, "oxide_mw": 394.0800},
    "Eu2O3":   {"raw": "Eu2O3",     "mw": 351.9260, "factor": 1.0, "oxide_mw": 351.9260},
    "CeO2":    {"raw": "CeO2",      "mw": 172.1200, "factor": 1.0, "oxide_mw": 172.1200},
    "Ag2O":    {"raw": "Ag2O",      "mw": 231.7400, "factor": 1.0, "oxide_mw": 231.7400},
    "Dy2O3":   {"raw": "Dy2O3",     "mw": 373.0000, "factor": 1.0, "oxide_mw": 373.0000},
    "YbF3":    {"raw": "YbF3",      "mw": 230.0400, "factor": 1.0, "oxide_mw": 230.0400},
    "PbBr2":   {"raw": "PbBr2",     "mw": 367.0100, "factor": 1.0, "oxide_mw": 367.0100},
    "PbCl2":   {"raw": "PbCl2",     "mw": 278.1100, "factor": 1.0, "oxide_mw": 278.1100},
    "CsBr":    {"raw": "CsBr",      "mw": 212.8100, "factor": 1.0, "oxide_mw": 212.8100},
    "Cs2O":    {"raw": "Cs2CO3",    "mw": 325.8198, "factor": 1.0, "oxide_mw": 281.8100},
    "CdO":     {"raw": "CdO",       "mw": 128.4130, "factor": 1.0, "oxide_mw": 128.4130},
    "CdSe":    {"raw": "CdSe",      "mw": 191.3700, "factor": 1.0, "oxide_mw": 191.3700},
    "ZnTe":    {"raw": "ZnTe",      "mw": 193.0100, "factor": 1.0, "oxide_mw": 193.0100},
    "K2O":     {"raw": "K2CO3",     "mw": 138.2050, "factor": 1.0, "oxide_mw": 94.1960},
    "CdTe":    {"raw": "CdTe",      "mw": 240.0140, "factor": 1.0, "oxide_mw": 240.0140},
    "NaI":     {"raw": "NaI",       "mw": 149.8900, "factor": 1.0, "oxide_mw": 149.8900},
    "Nb2O5":   {"raw": "Nb2O5",     "mw": 265.8100, "factor": 1.0, "oxide_mw": 265.8100},
    "CaF2":    {"raw": "CaF2",      "mw": 78.0700,  "factor": 1.0, "oxide_mw": 78.0700},
    "ZnSe":    {"raw": "ZnSe",      "mw": 144.3510, "factor": 1.0, "oxide_mw": 144.3510},
    "MgO":     {"raw": "MgO",       "mw": 40.3040,  "factor": 1.0, "oxide_mw": 40.3040},
    "Sb2O3":   {"raw": "Sb2O3",     "mw": 291.5000, "factor": 1.0, "oxide_mw": 291.5000},
}

# --- SESSION STATE (Girdileri ve Kayıtlı Tarifleri Tutmak İçin) ---
if 'inputs' not in st.session_state:
    st.session_state['inputs'] = {k: 0.0 for k in materials_db.keys()}

if 'saved_recipes' not in st.session_state:
    st.session_state['saved_recipes'] = {}

# --- SIDEBAR: RECIPE MANAGER ---
with st.sidebar:
    st.header("⚙️ Settings")
    target_weight = st.number_input(
        "Target Glass Weight (g)", 
        min_value=0.1, 
        value=100.0, 
        step=1.0,
        format="%.2f"
    )
    
    st.markdown("---")
    st.subheader("💾 Recipe Manager")
    
    # 1. Kaydetme Bölümü
    new_recipe_name = st.text_input("Recipe Name", placeholder="e.g. Base Glass 1")
    if st.button("Save Current Recipe"):
        if new_recipe_name:
            # Şu anki inputları kaydet
            st.session_state['saved_recipes'][new_recipe_name] = st.session_state['inputs'].copy()
            st.success(f"Saved: {new_recipe_name}")
        else:
            st.warning("Enter a name first!")

    st.markdown("---")

    # 2. Yükleme Bölümü
    if len(st.session_state['saved_recipes']) > 0:
        selected_recipe = st.selectbox("Select Saved Recipe", list(st.session_state['saved_recipes'].keys()))
        if st.button("📂 Load Recipe"):
            # Seçili tarifi inputlara geri yükle
            st.session_state['inputs'] = st.session_state['saved_recipes'][selected_recipe].copy()
            st.rerun() # Sayfayı yenile ki değerler kutulara gelsin
    else:
        st.info("No saved recipes yet.")

    st.markdown("---")
    st.caption("© 2025 **YTU Glass Research**")

# --- GİRİŞ KISMI (INPUTS) ---
st.subheader("1. Composition Input (Parts / Mol %)")
st.caption("Enter values below. You can save/load compositions from the sidebar.")

cols = st.columns(4)
i = 0
for oxide in materials_db.keys():
    with cols[i % 4]:
        # Session state'den değeri alarak kutuyu oluşturuyoruz
        val = st.number_input(
            f"{oxide}", 
            min_value=0.0, 
            step=0.1, 
            format="%.2f",
            key=f"widget_{oxide}", # Widget key'i farklı olsun
            value=st.session_state['inputs'].get(oxide, 0.0)
        )
        # Kutudaki değeri ana session değişkenine eşle
        st.session_state['inputs'][oxide] = val
    i += 1

# Toplam Kontrolü
total_parts = sum(st.session_state['inputs'].values())
if total_parts > 0:
    st.info(f"**Total Input:** {total_parts:.2f} | **Scaling Target:** {target_weight} g")

# --- HESAPLAMA MOTORU ---
if total_parts > 0:
    results = []
    
    # 1. Hesaplamalar
    total_oxide_weight_in_mix = 0
    temp_data = []
    
    # Session state'deki inputları kullan
    for oxide, val in st.session_state['inputs'].items():
        if val > 0:
            props = materials_db[oxide]
            moles_input = val 
            
            weight_oxide = moles_input * props['oxide_mw']
            moles_raw = moles_input * props['factor']
            weight_raw = moles_raw * props['mw']
            
            total_oxide_weight_in_mix += weight_oxide
            
            temp_data.append({
                "Oxide": oxide,
                "Raw Material": props['raw'],
                "Raw MW": props['mw'],
                "Input Value": moles_input, # Bunu tabloda göstereceğiz
                "Raw Weight (Unscaled)": weight_raw
            })
            
    # 2. Ölçekleme
    if total_oxide_weight_in_mix > 0:
        scaling_factor = target_weight / total_oxide_weight_in_mix
    else:
        scaling_factor = 0
        
    final_batch_list = []
    
    for item in temp_data:
        final_raw_weight = item["Raw Weight (Unscaled)"] * scaling_factor
        
        final_batch_list.append({
            "Oxide": item["Oxide"],
            "Raw Material": item["Raw Material"],
            "Input (Mol/Parts)": f"{item['Input Value']:.2f}", # Kontrol Sütunu
            "Mol Mass": f"{item['Raw MW']:.4f}",
            "To Weigh (g)": final_raw_weight
        })

    df_batch = pd.DataFrame(final_batch_list)

    # --- SONUÇ EKRANI ---
    st.divider()
    
    st.subheader("🧪 Final Batch Recipe")
    
    if not df_batch.empty:
        # Önce Toplamı Göster
        total_batch_weight = df_batch["To Weigh (g)"].sum()
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Total Powder to Weigh", f"{total_batch_weight:.4f} g")
        
        # Tabloyu Göster (Yeni Sütunlarla)
        st.dataframe(
            df_batch[["Oxide", "Raw Material", "Input (Mol/Parts)", "To Weigh (g)"]].style.format({
                "To Weigh (g)": "{:.4f}"
            }), 
            use_container_width=True, 
            hide_index=True
        )
        
        # CSV İndirme Butonu KALDIRILDI.
        
else:
    st.info("Enter values above to start calculation.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: black; opacity: 0.7;'>YTU Glass Research Group | v8.1 Final</div>", unsafe_allow_html=True)
