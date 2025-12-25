import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI (EN ÜSTTE OLMALI) ---
st.set_page_config(
    page_title="YTU Glass Calculator",
    page_icon="⚗️",
    layout="wide"
)

# --- STİL AYARLARI (SİYAH YAZI İÇİN) ---
st.markdown("""
    <style>
    /* Uygulama arka planı beyaz, yazılar siyah */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Tüm başlık ve metinleri zorla siyah yap */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stMetricValue, .stMetricLabel {
        color: #000000 !important;
    }
    
    /* Input alanlarının içi */
    .stNumberInput input {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Üst Başlık Kutusu (Burası Okunsun Diye Beyaz Yazı) */
    .header-box {
        background: linear-gradient(90deg, #1d3557 0%, #457b9d 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .header-box h2, .header-box div {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK KISMI ---
st.markdown("""
    <div class="header-box">
        <h2 style="margin:0;">YTU GLASS RESEARCH GROUP</h2>
        <div style="font-size: 1rem; opacity: 0.9;">Precision Glass Batch Recipe Calculator</div>
    </div>
    """, unsafe_allow_html=True)

# --- VERİ TABANI ---
materials_db = {
    "SiO2":    {"raw": "SiO2",      "mw": 60.0800,  "factor": 1.0, "oxide_mw": 60.08},
    "Na2O":    {"raw": "Na2CO3",    "mw": 105.9800, "factor": 1.0, "oxide_mw": 61.98},
    "Al2O3":   {"raw": "Al2O3",     "mw": 101.9600, "factor": 1.0, "oxide_mw": 101.96},
    "ZnO":     {"raw": "ZnO",       "mw": 81.3700,  "factor": 1.0, "oxide_mw": 81.37},
    "CaO":     {"raw": "CaCO3",     "mw": 100.0869, "factor": 1.0, "oxide_mw": 56.08},
    "B2O3":    {"raw": "H3BO3",     "mw": 61.8300,  "factor": 2.0, "oxide_mw": 69.62},
    "PbO":     {"raw": "PbO",       "mw": 223.1900, "factor": 1.0, "oxide_mw": 223.19},
    "NaBr":    {"raw": "NaBr",      "mw": 102.8900, "factor": 1.0, "oxide_mw": 102.89},
    "Cs2O":    {"raw": "Cs2CO3",    "mw": 325.8200, "factor": 1.0, "oxide_mw": 281.81}, 
    "NaI":     {"raw": "NaI",       "mw": 149.8900, "factor": 1.0, "oxide_mw": 149.89},
    "TeO2":    {"raw": "TeO2",      "mw": 159.6000, "factor": 1.0, "oxide_mw": 159.60},
    "GeO2":    {"raw": "GeO2",      "mw": 104.6300, "factor": 1.0, "oxide_mw": 104.63},
    "WO3":     {"raw": "WO3",       "mw": 231.8500, "factor": 1.0, "oxide_mw": 231.85},
    "Li2O":    {"raw": "Li2CO3",    "mw": 73.8900,  "factor": 1.0, "oxide_mw": 29.88},
    "Bi2O3":   {"raw": "Bi2O3",     "mw": 465.9600, "factor": 1.0, "oxide_mw": 465.96},
    "BaO":     {"raw": "BaCO3",     "mw": 197.3400, "factor": 1.0, "oxide_mw": 153.33},
    "TiO2":    {"raw": "TiO2",      "mw": 79.8660,  "factor": 1.0, "oxide_mw": 79.866},
    "MgO":     {"raw": "MgO",       "mw": 40.3040,  "factor": 1.0, "oxide_mw": 40.304},
    "K2O":     {"raw": "K2CO3",     "mw": 138.2050, "factor": 1.0, "oxide_mw": 94.20},
    "Sb2O3":   {"raw": "Sb2O3",     "mw": 291.5000, "factor": 1.0, "oxide_mw": 291.50},
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    target_weight = st.number_input(
        "Amount (grams)", 
        min_value=0.1, 
        value=100.0, 
        step=1.0,
        format="%.2f"
    )
    st.markdown("---")
    st.markdown("© 2025 **YTU Glass Research Group**")

# --- MAIN INPUT SECTION ---
st.subheader("1. Composition (Mol %)")

cols = st.columns(4)
inputs = {}
i = 0
for oxide, props in materials_db.items():
    with cols[i % 4]:
        val = st.number_input(
            f"{oxide}", 
            min_value=0.0, 
            max_value=100.0, 
            step=0.1, 
            format="%.2f",
            key=oxide
        )
        inputs[oxide] = val
    i += 1

# Progress Bar
total_mol_percent = sum(inputs.values())
st.write("") 

if 99.9 <= total_mol_percent <= 100.1:
    st.success(f"**Total: {total_mol_percent:.2f}%**")
else:
    st.error(f"**Total: {total_mol_percent:.2f}%** (Must be 100%)")

# --- CALCULATION LOGIC ---
if total_mol_percent > 0:
    results = []
    total_theoretical_glass_weight = 0
    total_raw_batch_weight = 0
    
    for oxide, val in inputs.items():
        if val > 0:
            props = materials_db[oxide]
            moles_oxide = val 
            moles_raw = moles_oxide * props['factor']
            weight_raw = moles_raw * props['mw']
            weight_oxide = moles_oxide * props['oxide_mw']
            
            total_theoretical_glass_weight += weight_oxide
            total_raw_batch_weight += weight_raw
            
            results.append({
                "Oxide": oxide,
                "Raw Material": props['raw'],
                "Mol Mass": props['mw'],
                "Mol %": val,
                "Raw Weight (Basis)": weight_raw
            })

    if total_theoretical_glass_weight > 0:
        scaling_factor = target_weight / total_theoretical_glass_weight
    else:
        scaling_factor = 0

    final_batch_data = []
    for row in results:
        batch_amount = row["Raw Weight (Basis)"] * scaling_factor
        final_batch_data.append({
            "Oxide": row["Oxide"],
            "Raw Material": row["Raw Material"],
            "Mol Mass (g/mol)": f"{row['Mol Mass']:.4f}",
            "Target Mol %": f"{row['Mol %']:.2f}",
            "To Weigh (g)": batch_amount 
        })

    # --- RESULTS DISPLAY ---
    st.divider()
    st.subheader("2. Batch Recipe 🧪")

    df = pd.DataFrame(final_batch_data)
    
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        total_batch = df["To Weigh (g)"].sum()
        
        m1.metric("Target Glass", f"{target_weight} g")
        m2.metric("Total Batch Mix", f"{total_batch:.4f} g")
        
        loi = 0
        if total_batch > 0:
            loi = ((total_batch - target_weight) / total_batch) * 100
        m3.metric("Est. Gas Loss (LOI)", f"{loi:.2f} %")

        # Tabloyu Göster
        st.dataframe(
            df.style.format({"To Weigh (g)": "{:.4f}"}),
            use_container_width=True,
            hide_index=True
        )

        # İndirme Butonu
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Recipe as CSV",
            data=csv,
            file_name='ytu_glass_batch_recipe.csv',
            mime='text/csv'
        )
            
    else:
        st.info("Start by entering Mol % values above.")

else:
    st.info("👋 Welcome! Please enter the composition in the table above.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: black;'>YTU Glass Research Group | v6.2 Black Text Edition</div>", unsafe_allow_html=True)
