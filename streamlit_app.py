import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime, timedelta

# Sivun asetukset: layout="wide" sallii vapaan leveyden
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI", layout="wide")

# CSS: Musta tausta, mutta ei enää 4:3 rajausta
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        h1, h2, h3, p, span, label {
            color: #FFFFFF !important;
            font-family: 'Courier New', monospace !important;
        }
        hr { border-color: #333333 !important; }
    </style>
""", unsafe_allow_html=True)

# Aika
nykyinen_aika = datetime.now().strftime("%H:%M:%S")

# Logo
st.code("""
███████╗███╗   ███╗██╗  ██╗
██╔════╝████╗ ████║██║ ██╔╝
███████╗██╔████╔██║█████╔╝ 
╚════██║██║╚██╔╝██║██╔═██╗ 
███████║██║ ╚═╝ ██║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
  * SUOMEN VALUUTTAREKISTERI PÖRSSIPÄÄTE v4.2 *
""", language="text")

st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI**")
st.write(f"Päivitetty {nykyinen_aika}")
st.write("---")

try:
    # Datahaku
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    hopea_unssi_usd = 1.0 / float(rates["XAG"]) if "XAG" in rates and rates["XAG"] > 0 else 30.75
    smk_arvo = (hopea_unssi_usd / 31.1035) * 0.5
    
    # Valuuttalista
    valuutat = [
        {"lyhenne": "SMK", "arvo": smk_arvo},
        {"lyhenne": "GBP", "arvo": 1.0/rates["GBP"]},
        {"lyhenne": "EUR", "arvo": 1.0/rates["EUR"]},
        {"lyhenne": "USD", "arvo": 1.0000},
        {"lyhenne": "CNY", "arvo": 1.0/rates["CNY"]},
        {"lyhenne": "JPY", "arvo": 1.0/rates["JPY"]},
        {"lyhenne": "CHF", "arvo": 1.0/rates["CHF"]}
    ]
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # Kolme saraketta: Taulukko, Käyrä, Ennuste
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### **P331 KURSSIT**")
        html_rows = "".join([f'<tr><td style="color:#FFF; width:60px;">{i:02d}</td><td style="color:{"#FFFF00" if v["lyhenne"]=="SMK" else "#00FF00"}">{v["lyhenne"]}</td><td align="right" style="color:#00FFFF;">{v["arvo"]:.4f}</td></tr>' for i, v in enumerate(valuutat, start=1)])
        components.html(f'<div style="background:#000; border:2px solid #0000FF; padding:10px;"><table style="width:100%; font-family:monospace;">{html_rows}</table></div>', height=300)

    with col2:
        st.markdown("### **P332 HISTORIA**")
        historia = [smk_arvo * 0.98, smk_arvo * 0.99, smk_arvo * 1.01, smk_arvo * 0.99, smk_arvo]
        graph = "".join(['<span style="color:#00FF00;">*</span>' if abs(h - smk_arvo) < 0.05 else '<span style="color:#333;">.</span>' for h in historia])
        components.html(f'<div style="background:#000; border:2px solid #0000FF; padding:10px; font-family:monospace; color:#FFF;">Päivät: 1  2  3  4  5<br>Käyrä: {graph}</div>', height=150)

    with col3:
        st.markdown("### **P333 ENNUSTE**")
        muutos = (historia[-1] - historia[0]) / len(historia)
        ennuste = historia[-1] + muutos
        tunnelma = "HÄRÄKÄS 🐂" if muutos >= 0 else "KARHUKÄS 🐻"
        vari = "#00FF00" if muutos >= 0 else "#FF0000"
        ennuste_html = f'<div style="background:#000; border:2px solid #00FFFF; padding:15px; font-family:monospace; color:#FFF;">NYKYINEN: <span style="color:{vari};">{tunnelma}</span><br>ENNUSTE: <span style="color:#00FFFF;">{ennuste:.4f} USD</span></div>'
        components.html(ennuste_html, height=180)

except Exception as e:
    st.error(f"JÄRJESTELMÄVIRHE: {e}")
