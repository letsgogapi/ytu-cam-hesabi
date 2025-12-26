import streamlit as st
import pandas as pd

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="YTU Glass Calculator",
    page_icon="⚗️",
    layout="wide"
)

# --- STİL VE GÖRÜNÜM (CSS) ---
st.markdown("""
    <style>
    /* Genel Arka Plan ve Yazı Rengi */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Tüm Yazıları Siyah Yap */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stMetricValue, .stMetricLabel, div {
        color: #000000 !important;
    }
    
    /* Input Alanları */
    .stNumberInput input {
        color: #000000 !important;
        background-color: #f0f2f6 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #ddd;
    }

    /* Başlık Kutusu */
    .header-box {
        background: linear-gradient(90deg, #1d3557 0%, #457b9d 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    .header-box h2 {
        color: #ffffff !important;
        margin: 0;
    }
    .header-box div {
        color: #f1f1f1 !important;
    }
    
    /* Tablo Yazıları */
    .dataframe {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=120)
    except:
        st.write("Logo")
with col_title:
    st.markdown("""
    <div class="header-box">
        <h2>YTU GLASS RESEARCH GROUP</h2>
        <div style="font-size: 1rem;">Ultimate Batch Calculator v7.0</div>
    </div>
    """, unsafe_allow_html=True)

# --- VERİ TABANI (EXCEL'DEN BİREBİR) ---
# Format: "Oxide": {"raw": "RawMaterialName", "mw": RawMW, "factor": Stoichiometry, "oxide_mw": OxideMW}
# Not: Excel'deki kırmızı sütunlar (Mol Kütlesi) OxideMW olarak, beyaz sütunlar RawMW olarak işlenmiştir.

materials_db = {
    "SiO2":    {"raw": "SiO2",      "mw": 60.0800,  "factor": 1.0, "oxide_mw": 60.0800},
    "Na2O":    {"raw": "Na2CO3",    "mw": 105.9800, "factor": 1.0, "oxide_mw": 61.9700}, # Excel: 61.97
    "Al2O3":   {"raw": "Al2O3",     "mw": 101.9600, "factor": 1.0, "oxide_mw": 101.9600},
    "ZnO":     {"raw": "ZnO",       "mw": 81.3700,  "factor": 1.0, "oxide_mw": 81.3700},
    "CaO":     {"raw": "CaCO3",     "mw": 100.0869, "factor": 1.0, "oxide_mw": 56.0774}, # Excel: 56.0774
    "TeO2":    {"raw": "TeO2",      "mw": 159.6000, "factor": 1.0, "oxide_mw": 159.6000},
    "B2O3":    {"raw": "H3BO3",     "mw": 61.8300,  "factor": 2.0, "oxide_mw": 69.6100}, # Excel: 69.61
    "NaF":     {"raw": "NaF",       "mw": 41.9900,  "factor": 1.0, "oxide_mw": 41.9900},
    "KBr":     {"raw": "KBr",       "mw": 119.0100, "factor": 1.0, "oxide_mw": 119.0100},
    "SnO2":    {"raw": "SnO2",      "mw": 150.6900, "factor": 1.0, "oxide_mw": 150.6900},
    "PbO":     {"raw": "PbO",       "mw": 223.1900, "factor": 1.0, "oxide_mw": 223.1900},
    "NaBr":    {"raw": "NaBr",      "mw": 102.8900, "factor": 1.0, "oxide_mw": 102.8900},
    "NaCl":    {"raw": "NaCl",      "mw": 58.4400,  "factor": 1.0, "oxide_mw": 58.4400},
    "GeO2":    {"raw": "GeO2",      "mw": 104.6300, "factor": 1.0, "oxide_mw": 104.6300},
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
    "Cs2O":    {"raw": "Cs2CO3",    "mw": 325.8200, "factor": 1.0, "oxide_mw": 281.8300}, # Excel'de Cs2O=281.83
    "CdO":     {"raw": "CdO",       "mw": 128.4100, "factor": 1.0, "oxide_mw": 128.4100},
    "CdSe":    {"raw": "CdSe",      "mw": 191.3700, "factor": 1.0, "oxide_mw": 191.3700},
    "ZnTe":    {"raw": "ZnTe",      "mw": 193.0100, "factor": 1.0, "oxide_mw": 193.0100},
    "K2O":     {"raw": "K2CO3",     "mw": 138.2050, "factor": 1.0, "oxide_mw": 94.1960}, # Excel: 94.196
    "CdTe":    {"raw": "CdTe",      "mw": 240.0300, "factor": 1.0, "oxide_mw": 240.0300},
    "NaI":     {"raw": "NaI",       "mw": 149.8900, "factor": 1.0, "oxide_mw": 149.8900},
    "Nb2O5":   {"raw": "Nb2O5",     "mw": 265.8100, "factor": 1.0, "oxide_mw": 265.8100},
    "CaF2":    {"raw": "CaF2",      "mw": 78.0700,  "factor": 1.0, "oxide_mw": 78.0700},
    "ZnSe":    {"raw": "ZnSe",      "mw": 144.3500, "factor": 1.0, "oxide_mw": 144.3500},
    "MgO":     {"raw": "MgO",       "mw": 40.3040,  "factor": 1.0, "oxide_mw": 40.3040},
    "Sb2O3":   {"raw": "Sb2O3",     "mw": 291.5000, "factor": 1.0, "oxide_mw": 291.5000},
}

# --- SIDEBAR & SESSION STATE (LAST CALC) ---
if 'last_recipe' not in st.session_state:
    st.session_state['last_recipe'] = None

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
    # Geçmiş Gösterimi
    if st.session_state['last_recipe'] is not None:
        st.info("💾 **Last Calculated:**")
        st.dataframe(st.session_state['last_recipe'][['Oxide', 'To Weigh (g)']], hide_index=True)
    
    st.markdown("---")
    st.markdown("© 2025 **YTU Glass Research**")

# --- GİRİŞ KISMI ---
st.subheader("1. Composition Input (Parts / Mol %)")
st.caption("You can enter values totaling more than 100. The app will normalize automatically.")

cols = st.columns(4)
inputs = {}
i = 0
for oxide, props in materials_db.items():
    with cols[i % 4]:
        val = st.number_input(
            f"{oxide}", 
            min_value=0.0, 
            step=0.1, 
            format="%.2f",
            key=oxide
        )
        inputs[oxide] = val
    i += 1

# Toplam Kontrolü (Sadece Bilgi Amaçlı, Hata Vermez)
total_parts = sum(inputs.values())
if total_parts > 0:
    st.info(f"**Total Input Sum:** {total_parts:.2f} (Calculations will be scaled to {target_weight}g glass)")

# --- HESAPLAMA MOTORU ---
if total_parts > 0:
    results = []
    
    # 1. Adım: Tüm girdilerin ağırlıklarını hesapla
    total_oxide_weight_in_mix = 0
    
    temp_data = []
    for oxide, val in inputs.items():
        if val > 0:
            props = materials_db[oxide]
            moles_input = val # Kullanıcının girdiği (örneğin 50)
            
            # Bu girdinin Oksit olarak ağırlığı (Camın içinde kalan)
            weight_oxide = moles_input * props['oxide_mw']
            
            # Bu girdi için gereken Hammadde ağırlığı
            moles_raw = moles_input * props['factor']
            weight_raw = moles_raw * props['mw']
            
            total_oxide_weight_in_mix += weight_oxide
            
            temp_data.append({
                "Oxide": oxide,
                "Raw Material": props['raw'],
                "Raw MW": props['mw'],
                "Input Moles": moles_input,
                "Raw Weight (Unscaled)": weight_raw,
                "Oxide Weight (Unscaled)": weight_oxide
            })
            
    # 2. Adım: Hedef Gramaja (Target Weight) Ölçekleme
    # Eğer 100g cam istiyorsak, teorik oksit toplamını 100'e eşitleyecek katsayıyı buluyoruz.
    if total_oxide_weight_in_mix > 0:
        scaling_factor = target_weight / total_oxide_weight_in_mix
    else:
        scaling_factor = 0
        
    final_batch_list = []
    final_target_list = []
    
    for item in temp_data:
        # Ölçeklenmiş Değerler
        final_raw_weight = item["Raw Weight (Unscaled)"] * scaling_factor
        final_oxide_weight = item["Oxide Weight (Unscaled)"] * scaling_factor
        
        # Yüzde Hesaplama (Molce)
        mol_percent = (item["Input Moles"] / total_parts) * 100
        
        # Tablo 1: Reçete (Tartılacak)
        final_batch_list.append({
            "Oxide": item["Oxide"],
            "Raw Material": item["Raw Material"],
            "Mol Mass (g/mol)": f"{item['Raw MW']:.4f}",
            "To Weigh (g)": final_raw_weight
        })
        
        # Tablo 2: Hedef Cam İçeriği
        final_target_list.append({
            "Oxide": item["Oxide"],
            "Mol %": f"{mol_percent:.2f}",
            "Weight in Glass (g)": f"{final_oxide_weight:.4f}"
        })

    df_batch = pd.DataFrame(final_batch_list)
    df_target = pd.DataFrame(final_target_list)
    
    # Sonucu Session State'e kaydet
    st.session_state['last_recipe'] = df_batch

    # --- SONUÇ EKRANI ---
    st.divider()
    
    col_res1, col_res2 = st.columns(2)
    
    # SOL TARAF: TARTIM REÇETESİ
    with col_res1:
        st.subheader("🧪 Batch Recipe (To Weigh)")
        if not df_batch.empty:
            total_batch_weight = df_batch["To Weigh (g)"].sum()
            st.metric("Total Batch Powder", f"{total_batch_weight:.4f} g")
            
            st.dataframe(
                df_batch.style.format({"To Weigh (g)": "{:.4f}"}), 
                use_container_width=True,
                hide_index=True
            )
            
            # CSV İndir
            csv = df_batch.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Recipe (CSV)",
                data=csv,
                file_name='ytu_glass_batch.csv',
                mime='text/csv'
            )

    # SAĞ TARAF: HEDEF CAM ÖZELLİKLERİ
    with col_res2:
        st.subheader("🔍 Target Glass Composition")
        if not df_target.empty:
            st.metric("Target Glass Weight", f"{target_weight:.2f} g")
            
            st.dataframe(
                df_target,
                use_container_width=True,
                hide_index=True
            )

else:
    st.info("Enter values above to start calculation.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: black; opacity: 0.7;'>YTU Glass Research Group | Developed for Laboratory Use</div>", unsafe_allow_html=True)
