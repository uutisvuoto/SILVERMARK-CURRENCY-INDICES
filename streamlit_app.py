import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime, timedelta

# Sivun asetukset CAPS LOCKILLA
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI", layout="wide")

# Haetaan kellonaika
nykyinen_aika = datetime.now().strftime("%H:%M:%S")

# --- VASEMMAN REUNAN NAVIGAATIOPALKKI ---
with st.sidebar:
    st.markdown("### **VALIKKO**")
    st.markdown("[INDEKSI-ETUSIVU](#hopeaan-sidotun-suomen-markan-kurssi-indeksi)")
    st.markdown("---")
    st.markdown("**RAHOITUSLINKIT:**")
    st.markdown("[Reuters Financial Systems](https://www.reuters.com)")
    st.markdown("[Bloomberg Markets](https://www.bloomberg.com)")
    st.markdown("---")
    st.write("Webmaster: admin@smk.index")

# --- RETROHENKINEN SIVUSTON LOGO (HTML/ASCII-TYYLI) ---
logo_html = """
<div style="background-color: #000000; padding: 15px; border: 3px double #00FF00; font-family: 'Courier New', monospace; text-align: center; margin-bottom: 20px; box-shadow: 4px 4px 0px #333333;">
    <pre style="color: #FFFF00; font-weight: bold; font-size: 14px; margin: 0; line-height: 1.2; background: transparent; border: none;">
 ██████╗ ███╗   ███╗ ██╗  ██╗   
██╔════╝ ████╗ ████║ ██║ ██╔╝    
╚█████╗  ██╔████╔██║ █████╔╝    
 ╚═══██╗ ██║╚██╔╝██║ ██╔═██╗     
██████╔╝ ██║ ╚═╝ ██║ ██║  ██╗    
╚═════╝  ╚═╝     ╚═╝ ╚═╝  ╚═╝    
    </pre>
    <div style="color: #00FFFF; font-size: 12px; margin-top: 8px; letter-spacing: 2px; font-weight: bold;">
        * SUOMEN VALUUTTAREKISTERI PÖRSSIPÄÄTE SYSTEM v3.3 *
    </div>
</div>
"""
st.components.v1.html(logo_html, height=140)

# --- PÄÄSIVUN OTSIKKO ---
st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI**")
st.write(f"Suomen Valuuttarekisteri — Sivu perustettu 2026 — Päivitetty {nykyinen_aika}")
st.write("---")

try:
    # 1. Haetaan reaaliaikaiset valuuttakurssit ja hopea (XAG) samasta rajapinnasta
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    if "XAG" in rates and rates["XAG"] > 0:
        hopea_unssi_usd = 1.0 / float(rates["XAG"])
    else:
        hopea_unssi_usd = 30.75

    # Lasketaan 1 SMK arvo (1 SMK = 0.5g hopeaa, unssi = 31.1035g)
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_arvo = hopea_gramma_usd * 0.5
    
    # Valuuttojen arvot dollareina
    usd_arvo = 1.0000
    eur_arvo = 1.0 / float(rates["EUR"])
    gbp_arvo = 1.0 / float(rates["GBP"])
    cny_arvo = 1.0 / float(rates["CNY"])
    rub_arvo = 1.0 / float(rates["RUB"])
    jpy_arvo = 1.0 / float(rates["JPY"])
    sek_arvo = 1.0 / float(rates["SEK"])
    nok_arvo = 1.0 / float(rates["NOK"])
    chf_arvo = 1.0 / float(rates["CHF"])
    cad_arvo = 1.0 / float(rates["CAD"])
    aud_arvo = 1.0 / float(rates["AUD"])
    inr_arvo = 1.0 / float(rates["INR"])
    
    # Luodaan lista rankingia varten
    valuutat = [
        {"lyhenne": "SMK", "arvo": smk_arvo},
        {"lyhenne": "GBP", "arvo": gbp_arvo},
        {"lyhenne": "EUR", "arvo": eur_arvo},
        {"lyhenne": "USD", "arvo": usd_arvo},
        {"lyhenne": "CNY", "arvo": cny_ar
