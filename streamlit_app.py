import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime, timedelta

# Sivun asetukset: wide-näkymä
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI", layout="wide")

# CSS-tyylittely
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        h1, h2, h3, p, span, label { color: #FFFFFF !important; font-family: 'Courier New', monospace !important; }
        hr { border-color: #333333 !important; }
        .stCheckbox label { color: #FF0000 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Aika ja Logo
nykyinen_aika = datetime.now().strftime("%H:%M:%S")
st.code("""
███████╗███╗   ███╗██╗  ██╗
██╔════╝████╗ ████║██║ ██╔╝
███████╗██╔████╔██║█████╔╝ 
╚════██║██║╚██╔╝██║██╔═██╗ 
███████║██║ ╚═╝ ██║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
  * SUOMEN VALUUTTAREKISTERI PÖRSSIPÄÄTE v4.3 *
""", language="text")

st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI**")
st.write(f"Päivitetty {nykyinen_aika}")

# Kriisikytkin
sotatila = st.checkbox("AKTIVOI SOTATILA-SIMULAATIO (DEFCON 1)")
st.write("---")

try:
    # Datahaku
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    hopea_usd = (1.0 / float(rates["XAG"]) * 6.0) if sotatila else (1.0 / float(rates["XAG"]))
    smk_arvo = (hopea_usd / 31.1035) * 0.5
    
    # Valuuttalista
    valuutat = [
        {"lyhenne": "SMK", "arvo": smk_arvo},
        {"lyhenne": "GBP", "arvo": (1.0/rates["GBP"])*(0.7 if sotatila else 1)},
        {"lyhenne": "EUR", "arvo": (1.0/rates["EUR"])*(0.2 if sotatila else 1)},
        {"lyhenne": "USD", "arvo": 1.0000},
        {"lyhenne": "RUB", "arvo": (1.0/rates["RUB"])*(0.05 if sotatila else 1)}
    ]
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # Sarakkeet
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### **P331 KURSSIT**")
        html_rows = "".join([f'<tr><td style="color:#FFF;">{i:02d}</td><td style="color:{"#FFFF00" if v["lyhenne"]=="SMK" else "#00FF00"}">{v["lyhenne"]}</td><td align="right" style="color:#00FFFF;">{v["arvo"]:.4f}</td></tr>' for i, v in enumerate(valuutat, start=1)])
        components.html(f'<div style="background:#000; border:2px solid #0000FF; padding:10px;"><table style="width:100%; font-family:monospace;">{html_rows}</table></div>', height=300)

    with col2:
        st.markdown("### **P332 HISTORIA**")
        graph = '<span style="color:#00FF00;">*</span>' * 5
        components.html(f'<div style="background:#000; border:2px solid #0000FF; padding:10px; font-family:monospace; color:#FFF;">Käyrä:<br>{graph}</div>', height=150)

    with col3:
        st.markdown("### **P333 ENNUSTE**")
        vari = "#FF0000" if sotatila else "#00FF00"
        ennuste_html = f'<div style="background:#000; border:2px solid #00FFFF; padding:15px; font-family:monospace; color:#FFF;">TRENDI: <span style="color:{vari};">{"KARHUKÄS" if sotatila else "HÄRÄKÄS"}</span><br>ENNUSTE: <span style="color:#00FFFF;">{(smk_arvo*1.05):.4f} USD</span></div>'
        components.html(ennuste_html, height=150)

    # Laskuri
    st.write("---")
    markat = st.number_input("SMK-MÄÄRÄ:", value=100)
    st.code(f">>> {markat} SMK = {(markat * smk_arvo):.2f} USD", language="text")

except Exception as e:
    st.error(f"JÄRJESTELMÄVIRHE: {e}")
