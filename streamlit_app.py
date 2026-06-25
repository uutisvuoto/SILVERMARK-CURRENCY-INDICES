import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime

# Sivun asetukset
st.set_page_config(page_title="PÖRSSIPÄÄTE", layout="wide")

# CSS-tyylit
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        h1, h2, h3, p, span { color: #FFFFFF !important; font-family: 'Courier New', monospace !important; }
    </style>
""", unsafe_allow_html=True)

# Logo ja otsikko
st.code("""
███████╗███╗   ███╗██╗  ██╗
██╔════╝████╗ ████║██║ ██╔╝
███████╗██╔████╔██║█████╔╝ 
╚════██║██║╚██╔╝██║██╔═██╗ 
███████║██║ ╚═╝ ██║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
""", language="text")

st.markdown("# **SUOMEN VALUUTTAREKISTERI**")
st.write(f"Päivitetty: {datetime.now().strftime('%H:%M:%S')}")

try:
    # Datan haku
    url = "https://open.er-api.com/v6/latest/USD"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        rates = data["rates"]

    # Laskenta
    hopea_usd = 1.0 / float(rates["XAG"])
    smk_arvo = (hopea_usd / 31.1035) * 0.5
    
    valuutat = [
        {"n": "SMK", "v": smk_arvo},
        {"n": "GBP", "v": 1.0/rates["GBP"]},
        {"n": "EUR", "v": 1.0/rates["EUR"]},
        {"n": "USD", "v": 1.0},
        {"n": "CHF", "v": 1.0/rates["CHF"]}
    ]
    valuutat.sort(key=lambda x: x["v"], reverse=True)

    # Sarakkeet
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("P331 KURSSIT")
        html_rows = "".join([f'<tr><td style="color:#FFF;">{i+1:02d}</td><td style="color:#00FF00;">{v["n"]}</td><td align="right" style="color:#00FFFF;">{v["v"]:.4f}</td></tr>' for i, v in enumerate(valuutat)])
        components.html(f'<table style="width:100%; font-family:monospace; color:#FFF;">{html_rows}</table>', height=200)

    with c2:
        st.subheader("P332 HISTORIA")
        st.write("SMK/USD trendi vakaa.")
        st.progress(0.7)

    with c3:
        st.subheader("P333 ENNUSTE")
        ennuste = smk_arvo * 1.002
        st.write(f"24H ENNUSTE: {ennuste:.4f} USD")
        st.write("SUOSITUS: HOLD")

    # Laskuri
    st.write("---")
    maara = st.number_input("SMK-MÄÄRÄ:", value=100)
    st.code(f">>> {maara} SMK = {(maara * smk_arvo):.2f} USD", language="text")

except Exception as e:
    st.error(f"YHTEYSVIRHE: Päivitä sivu. ({e})")
