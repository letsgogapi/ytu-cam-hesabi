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
    
    /* Tablo Düzeni */
    .dataframe { font-size: 14px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLIK ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image("logo.png", width=130)
    except:
        st.write("Logo") # Logo dosyası yoksa yazı yazar
with col_title:
    st.markdown("""
    <div class="header-box">
        <h2>YTU GLASS RESEARCH GROUP</h2>
        <div style="font-size: 1rem;">Precision Batch Calculator v9.0 (PhD Edition)</div>
    </div>
    """, unsafe_allow_html=True)

# --- VERİ TABANI (HASSAS KÜTLELER GÜNCELLENDİ) ---
# Not: P2O5 hatasını gidermek için atom ağırlıkları hassaslaştırıldı.
# MnO için hammadde olarak MnCO3 (Mangan Karbonat) varsayıldı.

materials_db = {
    # --- TEMEL OKSİTLER ---
    "SiO2":    {"raw": "SiO2",      "mw": 60.0843,  "factor": 1.0, "oxide_mw": 60.0843},
    "B2O3":    {"raw": "H3BO3",     "mw": 61.8330,  "factor": 2.0, "oxide_mw": 69.6202},
    "P2O5":    {"raw": "P2O5",      "mw": 141.9445, "factor": 1.0, "oxide_mw": 141.9445}, # HASSAS AYAR
    "GeO2":    {"raw": "GeO2",      "mw": 104.6388, "factor": 1.0, "oxide_mw": 104.6388},
    "TeO2":    {"raw": "TeO2",      "mw": 159.5988, "factor": 1.0, "oxide_mw": 159.5988},
    "Bi2O3":   {"raw": "Bi2O3",     "mw": 465.9590, "factor": 1.0, "oxide_mw": 465.9590},
    "Sb2O3":   {"raw": "Sb2O3",     "mw": 291.5180, "factor": 1.0, "oxide_mw": 291.5180},
    "Al2O3":   {"raw": "Al2O3",     "mw": 101.9613, "factor": 1.0, "oxide_mw": 101.9613},
    
    # --- ALKALİ & TOPRAK ALKALİ (KARBONATLI) ---
    "Na2O":    {"raw": "Na2CO3",    "mw": 105.9888, "factor": 1.0, "oxide_mw": 61.9789},
    "K2O":     {"raw": "K2CO3",     "mw": 138.2055, "factor": 1.0, "oxide_mw": 94.1960},
    "Li2O":    {"raw": "Li2CO3",    "mw": 73.8910,  "factor": 1.0, "oxide_mw": 29.8814},
    "CaO":     {"raw": "CaCO3",     "mw": 100.0869, "factor": 1.0, "oxide_mw": 56.0774},
    "MgO":     {"raw": "MgO",       "mw": 40.3044,  "factor": 1.0, "oxide_mw": 40.3044}, # Genelde MgO olarak eklenir
    "BaO":     {"raw": "BaCO3",     "mw": 197.3359, "factor": 1.0, "oxide_mw": 153.3264},
    "SrO":     {"raw": "SrCO3",     "mw": 147.6300, "factor": 1.0, "oxide_mw": 103.6200},
    "Cs2O":    {"raw": "Cs2CO3",    "mw": 325.8200, "factor": 1.0, "oxide_mw": 281.8100},
    
    # --- GEÇİŞ METALLERİ & RENKLENDİRİCİLER (YENİ EKLENENLER) ---
    "ZnO":     {"raw": "ZnO",       "mw": 81.4080,  "factor": 1.0, "oxide_mw": 81.4080},
    "PbO":     {"raw": "PbO",       "mw": 223.1994, "factor": 1.0, "oxide_mw": 223.1994},
    "TiO2":    {"raw": "TiO2",      "mw": 79.8660,  "factor": 1.0, "oxide_mw": 79.8660},
    "Fe2O3":   {"raw": "Fe2O3",     "mw": 159.6882, "factor": 1.0, "oxide_mw": 159.6882}, # Hematit
    "MnO":     {"raw": "MnCO3",     "mw": 114.9470, "factor": 1.0, "oxide_mw": 70.9374},  # MnO kaynağı MnCO3
    "CuO":     {"raw": "CuO",       "mw": 79.5450,  "factor": 1.0, "oxide_mw": 79.5450},
    "MoO3":    {"raw": "MoO3",      "mw": 143.9400, "factor": 1.0, "oxide_mw": 143.9400},
    "WO3":     {"raw": "WO3",       "mw": 231.8400, "factor": 1.0, "oxide_mw": 231.8400},
    "SnO2":    {"raw": "SnO2",      "mw": 150.7080, "factor": 1.0, "oxide_mw": 150.7080},
    "Nb2O5":   {"raw": "Nb2O5",     "mw": 265.8100, "factor": 1.0, "oxide_mw": 265.8100},
    "Ag2O":    {"raw": "Ag2O",      "mw": 231.7350, "factor": 1.0, "oxide_mw": 231.7350},
    "CdO":     {"raw": "CdO",       "mw": 128.4110, "factor": 1.0, "oxide_mw": 128.4110},

    # --- HALOJENLER & DİĞERLERİ ---
    "NaF":     {"raw": "NaF",       "mw": 41.9882,  "factor": 1.0, "oxide_mw": 41.9882},
    "CaF2":    {"raw": "CaF2",      "mw": 78.0700,  "factor": 1.0, "oxide_mw": 78.0700},
    "NaCl":    {"raw": "NaCl",      "mw": 58.4400,  "factor": 1.0, "oxide_mw": 58.4400},
    "NaBr":    {"raw": "NaBr",      "mw": 102.8940, "factor": 1.0, "oxide_mw": 102.8940},
    "NaI":     {"raw": "NaI",       "mw": 149.8900, "factor": 1.0, "oxide_mw": 149.8900},
    "KBr":     {"raw": "KBr",       "mw": 119.0020, "factor": 1.0, "oxide_mw": 119.0020},
    "CsBr":    {"raw": "CsBr",      "mw": 212.8100, "factor": 1.0, "oxide_mw": 212.8100},
    
    # --- NADİR TOPRAK ELEMENTLERİ (REE) ---
    "Er2O3":   {"raw": "Er2O3",     "mw": 382.5600, "factor": 1.0, "oxide_mw": 382.5600},
    "Nd2O3":   {"raw": "Nd2O3",     "mw": 336.4800, "factor": 1.0, "oxide_mw": 336.4800},
    "Yb2O3":   {"raw": "Yb2O3",     "mw": 394.0800, "factor": 1.0, "oxide_mw": 394.0800},
    "Eu2O3":   {"raw": "Eu2O3",     "mw": 351.9260, "factor": 1.0, "oxide_mw": 351.9260},
    "Sm2O3":   {"raw": "Sm2O3",     "mw": 348.7200, "factor": 1.0, "oxide_mw": 348.7200},
    "CeO2":    {"raw": "CeO2",      "mw": 172.1150, "factor": 1.0, "oxide_mw": 172.1150},
    "Tm2O3":   {"raw": "Tm2O3",     "mw": 385.8700, "factor": 1.0, "oxide_mw": 385.8700},
    "Ho2O3":   {"raw": "Ho2O3",     "mw": 377.8600, "factor": 1.0, "oxide_mw": 377.8600},
    "Dy2O3":   {"raw": "Dy2O3",     "mw": 373.0000, "factor": 1.0, "oxide_mw": 373.0000},
    "YbF3":    {"raw": "YbF3",      "mw": 230.0400, "factor": 1.0, "oxide_mw": 230.0400},
}

# --- SESSION STATE (Tarif Yönetimi İçin) ---
if 'inputs' not in st.session_state:
    st.session_state['inputs'] = {k: 0.0 for k in materials_db.keys()}
    # Varsayılan (Senin test örneğin)
    st.session_state['inputs']['SiO2'] = 5.0
    st.session_state['inputs']['Na2O'] = 15.0
    st.session_state['inputs']['CaO'] = 15.0
    st.session_state['inputs']['P2O5'] = 45.0
    st.session_state['inputs']['K2O'] = 15.0
    st.session_state['inputs']['MgO'] = 5.0

if 'saved_recipes' not in st.session_state:
    st.session_state['saved_recipes'] = {}

# --- SIDEBAR: RECIPE MANAGER ---
with st.sidebar:
    st.header("⚙️ Settings")
    target_weight = st.number_input(
        "Target Glass Weight (g)", 
        min_value=0.1, 
        value=30.0, 
        step=1.0,
        format="%.2f"
    )
    
    st.markdown("---")
    st.subheader("💾 Recipe Manager")
    
    # Kaydetme
    new_recipe_name = st.text_input("Recipe Name", placeholder="e.g. Test Phosphate Glass")
    if st.button("Save Current Recipe"):
        if new_recipe_name:
            st.session_state['saved_recipes'][new_recipe_name] = st.session_state['inputs'].copy()
            st.success(f"Saved: {new_recipe_name}")
        else:
            st.warning("Enter a name first!")

    st.markdown("---")

    # Yükleme
    if len(st.session_state['saved_recipes']) > 0:
        selected_recipe = st.selectbox("Select Saved Recipe", list(st.session_state['saved_recipes'].keys()))
        if st.button("📂 Load Recipe"):
            st.session_state['inputs'] = st.session_state['saved_recipes'][selected_recipe].copy()
            st.rerun() 
    else:
        st.info("No saved recipes yet.")

    st.markdown("---")
    st.caption("© 2025 **YTU Glass Research**")

# --- GİRİŞ KISMI (INPUTS) ---
st.subheader("1. Composition Input (Parts / Mol %)")
st.caption("You can enter values totaling more than 100. The app will normalize automatically.")

# Sütunları dinamik oluştur
cols = st.columns(4)
i = 0
active_inputs = []

for oxide in materials_db.keys():
    # Sadece içinde bir şey yazılı olanları veya kullanıcı bir şey yazarsa onu takip etmek için
    current_val = st.session_state['inputs'].get(oxide, 0.0)
    
    with cols[i % 4]:
        val = st.number_input(
            f"{oxide}", 
            min_value=0.0, 
            step=0.1, 
            format="%.2f",
            key=f"widget_{oxide}", 
            value=float(current_val)
        )
        st.session_state['inputs'][oxide] = val
        if val > 0:
            active_inputs.append(oxide)
    i += 1

# Toplam Kontrol
total_parts = sum(st.session_state['inputs'].values())

if total_parts > 0:
    st.success(f"**Total Moles/Parts:** {total_parts:.2f} | **Target:** {target_weight} g")
else:
    st.info("Please enter composition values above.")

# --- HESAPLAMA MOTORU ---
if total_parts > 0:
    # 1. Teorik Cam Ağırlığını ve Hammadde İhtiyacını Hesapla
    total_theoretical_glass_weight = 0
    calculation_data = []

    for oxide, val in st.session_state['inputs'].items():
        if val > 0:
            props = materials_db[oxide]
            moles_input = val
            
            # Bu oksidin cam içindeki ağırlığı (Mol * Oxide_MW)
            weight_oxide_in_glass = moles_input * props['oxide_mw']
            total_theoretical_glass_weight += weight_oxide_in_glass
            
            # Bu oksit için gereken hammadde ağırlığı (Mol * Factor * Raw_MW)
            # Factor: Örneğin B2O3 için 2 mol H3BO3 gerekir (Factor=2)
            moles_raw_needed = moles_input * props['factor']
            weight_raw_needed = moles_raw_needed * props['mw']
            
            calculation_data.append({
                "Oxide": oxide,
                "Raw Material": props['raw'],
                "Raw MW": props['mw'],
                "Oxide MW": props['oxide_mw'],
                "Moles Input": moles_input,
                "Raw Weight (Basis)": weight_raw_needed,
                "Oxide Weight (Basis)": weight_oxide_in_glass
            })

    # 2. Ölçekleme Faktörü (Target Weight / Theoretical Weight)
    # Bu faktör, 'Parts' toplamı 100 olmasa bile (örneğin 105 olsa bile) 
    # sonucu tam olarak hedef gramaja (30g) sıkıştırır.
    if total_theoretical_glass_weight > 0:
        scaling_factor = target_weight / total_theoretical_glass_weight
    else:
        scaling_factor = 0

    final_batch = []
    final_glass_content = []

    for item in calculation_data:
        # Gerçek tartım miktarı
        real_batch_weight = item["Raw Weight (Basis)"] * scaling_factor
        
        # Camın içindeki gerçek miktar
        real_oxide_weight = item["Oxide Weight (Basis)"] * scaling_factor
        
        # Gerçek Mol Yüzdesi (Normalizasyon sonrası)
        real_mol_percent = (item["Moles Input"] / total_parts) * 100

        final_batch.append({
            "Oxide": item["Oxide"],
            "Raw Material": item["Raw Material"],
            "Input (Mol)": f"{item['Moles Input']:.2f}",
            "Mol Mass": f"{item['Raw MW']:.4f}",
            "To Weigh (g)": real_batch_weight
        })
        
        final_glass_content.append({
            "Oxide": item["Oxide"],
            "Mol %": f"{real_mol_percent:.2f}",
            "Weight in Glass (g)": f"{real_oxide_weight:.4f}"
        })

    df_batch = pd.DataFrame(final_batch)
    df_content = pd.DataFrame(final_glass_content)

    # --- SONUÇ GÖSTERİMİ ---
    st.divider()
    
    col_left, col_right = st.columns(2)
    
    # SOL: TARTIM LİSTESİ
    with col_left:
        st.subheader("🧪 Batch Recipe (To Weigh)")
        if not df_batch.empty:
            total_powder = df_batch["To Weigh (g)"].sum()
            st.metric("Total Powder Mix", f"{total_powder:.4f} g")
            
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

    # SAĞ: HEDEF CAM İÇERİĞİ
    with col_right:
        st.subheader("🔍 Target Glass Composition")
        if not df_content.empty:
            st.metric("Final Glass Weight", f"{target_weight:.2f} g")
            
            st.dataframe(
                df_content,
                use_container_width=True,
                hide_index=True
            )
            
            # LOI (Loss on Ignition) Hesabı
            loi = ((total_powder - target_weight) / total_powder) * 100
            st.caption(f"Estimated Gas Loss (LOI): {loi:.2f}% (CO2, H2O, etc.)")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: black; opacity: 0.7;'>YTU Glass Research Group | v9.0 Final PhD Edition</div>", unsafe_allow_html=True)
