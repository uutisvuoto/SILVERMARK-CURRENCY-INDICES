import streamlit as st
import urllib.request
import json
from datetime import datetime

# Sivun nimi ja asetukset
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI", layout="wide")

# Haetaan tämän hetkinen kellonaika automaattisesti
nykyinen_aika = datetime.now().strftime("%H:%M:%S")

# --- VASEMMAN REUNAN NAVIGAATIOPALKKI ---
with st.sidebar:
    st.markdown("### **VALIKKO**")
    st.markdown("[INDEKSI-ETUSIVU](#hopeaan-sidotun-suomen-markan-kurssiindeksi)")
    st.markdown("[VALUUTTAKURSSIT](#viralliset-kurssinoteeraukset-usd-ranking)")
    st.markdown("[VALUUTTAMUUNNIN](#valuuttamuunnin)")
    st.markdown("---")
    st.markdown("**RAHOITUSLINKIT:**")
    st.markdown("[Reuters Financial Systems](https://www.reuters.com)")
    st.markdown("[Bloomberg Markets](https://www.bloomberg.com)")
    st.markdown("---")
    st.write("Yhteydenotot: webmaster@smk.index")

# --- PÄÄSIVUN SISÄLTÖ ---
st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI**")
st.write(f"Suomen Valuuttarekisteri — Sivu perustettu 2026 — Päivitetty {nykyinen_aika}")
st.write("---")

try:
    # Haetaan markkinadata (pohjana USD)
    url = "https://open.er-api.com/v6/latest/USD"
    vastaus = urllib.request.urlopen(url)
    data = json.loads(vastaus.read())
    
    kurssit_usd_suhteessa = data["rates"]
    
    # Hopean hinta ja SMK arvo dollareissa (1 SMK = 0.5g hopeaa)
    hopea_unssi_usd = 30.50
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_in_usd = hopea_gramma_usd * 0.5
    
    # Lasketaan kaikkien valuuttojen arvot suhteessa Yhdysvaltain dollariin (USD)
    eur_in_usd = 1 / kurssit_usd_suhteessa["EUR"]
    gbp_in_usd = 1 / kurssit_usd_suhteessa["GBP"]
    cny_in_usd = 1 / kurssit_usd_suhteessa["CNY"]
    rub_in_usd = 1 / kurssit_usd_suhteessa["RUB"]
    jpy_in_usd = 1 / kurssit_usd_suhteessa["JPY"]
    usd_in_usd = 1.0000
    
    # Luodaan sanakirja dynaamista järjestämistä varten
    valuuttalista = [
        {"nimi": "Suomen Markka (SMK)", "arvo": smk_in_usd, "korostus": True},
        {"nimi": "Iso-Britannian Punta (GBP)", "arvo": gbp_in_usd, "korostus": False},
        {"nimi": "Euro (EUR)", "arvo": eur_in_usd, "korostus": False},
        {"nimi": "US-Dollari (USD)", "arvo": usd_in_usd, "korostus": False},
        {"nimi": "Kiinan Yuan (CNY)", "arvo": cny_in_usd, "korostus": False},
        {"nimi": "Venäjän Rupla (RUB)", "arvo": rub_in_usd, "korostus": False},
        {"nimi": "Japanin Jeni (JPY)", "arvo": jpy_in_usd, "korostus": False}
    ]
    
    # JÄRJESTETÄÄN VALUUTAT: Kallein USD-arvo ensin (päällimmäiseksi)
    valuuttalista = sorted(valuuttalista, key=lambda x: x["arvo"], reverse=True)

    # --- RAKENNETAAN REAALIAIKAINEN RANKING-TAULUKKO ---
    st.markdown("### **VIRALLISET KURSSINOTEERAUKSET (USD-RANKING)**")
    st.write("Valuutat järjestetty reaaliaikaisen markkina-arvon mukaan (kallein ylimpänä). Viitestandardi: 1 SMK = 0,5g hopeaa.")
    
    # Aloitetaan HTML-taulukon rakennus
    html_taulukko = """
    <table border="3" cellpadding="5" cellspacing="0" style="font-family: monospace; width: 100%; max-width: 650px; border-color: #808080;">
        <tr bgcolor="#d3d3d3">
            <th align="left" style="width: 50px;">SIJA</th>
