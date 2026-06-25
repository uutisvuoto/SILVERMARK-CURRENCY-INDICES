import streamlit as st
import urllib.request
import json
from datetime import datetime

# 5. Sivun nimi muutettu halutuksi
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI", layout="wide")

# Haetaan tämän hetkinen kellonaika automaattisesti (4. kohta)
nykyinen_aika = datetime.now().strftime("%H:%M:%S")

# --- VASEMMAN REUNAN NAVIGAATIOPALKKI (90-LUVUN TYYLIIN ILMAN YLE-VIITTEITÄ) ---
with st.sidebar:
    st.markdown("### **VALIKKO**")
    st.markdown("[INDEKSI-ETUSIVU](#hopeaan-sidotun-suomen-markan-kurssiindeksi)")
    st.markdown("[VALUUTTAKURSSIT](#viralliset-kurssinoteeraukset-usd)")
    st.markdown("[VALUUTTAMUUNNIN](#valuuttamuunnin)")
    st.markdown("---")
    st.markdown("**RAHOITUSLINKIT:**")
    st.markdown("[Reuters Financial Systems](https://www.reuters.com)")
    st.markdown("[Bloomberg Markets](https://www.bloomberg.com)")
    st.markdown("---")
    st.write("Yhteydenotot: webmaster@smk.index")

# --- PÄÄSIVUN SISÄLTÖ ---

# 5. Sivun pääotsikko
st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI**")
# 3. & 4. Perustamisvuosi ja dynaaminen kellonaika
st.write(f"Suomen Valuuttarekisteri — Sivu perustettu 2026 — Päivitetty {nykyinen_aika}")
st.write("---")

try:
    # Haetaan markkinadata (pohjana USD)
    url = "https://open.er-api.com/v6/latest/USD"
    vastaus = urllib.request.urlopen(url)
    data = json.loads(vastaus.read())
    
    kurssit_usd_suhteessa = data["rates"]
    
    # 2. Lasketaan valuuttojen arvot YHDEN YKSIKÖN arvona Yhdysvaltain dollareissa (USD)
    usd_in_usd = 1.0000
    eur_in_usd = 1 / kurssit_usd_suhteessa["EUR"]
    gbp_in_usd = 1 / kurssit_usd_suhteessa["GBP"]
    cny_in_usd = 1 / kurssit_usd_suhteessa["CNY"]
    rub_in_usd = 1 / kurssit_usd_suhteessa["RUB"]
    jpy_in_usd = 1 / kurssit_usd_suhteessa["JPY"]
    
    # Hopean hinta ja SMK arvo dollareissa (1 SMK = 0.5g hopeaa)
    hopea_unssi_usd = 30.50
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_in_usd = hopea_gramma_usd * 0.5
    
    # Lasketaan muunninta varten SMK:n suhde euroon
    smk_eur = smk_in_usd / eur_in_usd

    # --- 6. HIENOMPI HTML-TAULUKKO 90-LUVUN TYYLIIN ---
    st.markdown("### **VIRALLISET KURSSINOTEERAUKSET (USD)**")
    st.write("Valuuttaindeksi mitattuna Yhdysvaltain dollareina (USD). Viitestandardi: 1 SMK = 0,5g hopeaa.")
    
    # Luodaan perinteinen, siisti HTML-taulukko paksulla reunuksella ja harmaalla otsikolla
    html_taulukko = f"""
    <table border="3" cellpadding="5" cellspacing="0" style="font-family: monospace; width: 100%; max-width: 600px; border-color: #808080;">
        <tr bgcolor="#d3d3d3">
            <th align="left">VALUUTTAYKSIKKÖ (1 kpl)</th>
            <th align="right">ARVO (USD)</th>
        </tr>
        <tr>
            <td><b>Suomen Markka (SMK)</b></td>
            <td align="right"><b>{smk_in_usd:.4f} USD</b></td>
        </tr>
        <tr>
            <td>Euro (EUR)</td>
            <td align="right">{eur_in_usd:.4f} USD</td>
        </tr>
        <tr>
            <td>US-Dollari (USD)</td>
            <td align="right">{usd_in_usd:.4f} USD</td>
        </tr>
        <tr>
            <td>Iso-Britannian Punta (GBP)</td>
            <td align="right">{gbp_in_usd:.4f} USD</td>
        </tr>
        <tr>
            <td>Kiinan Yuan (CNY)</td>
            <td align="right">{cny_in_usd:.4f} USD</td>
        </tr>
        <tr>
            <td>Venäjän Rupla (RUB)</td>
            <td align="right">{rub_in_usd:.4f} USD</td>
        </tr>
        <tr>
            <td>Japanin Jeni (JPY)</td>
            <td align="right">{jpy_in_usd:.4f} USD</td>
        </tr>
    </table>
    """
    # Ajetaan aito HTML-koodi Streamlitiin
    st.markdown(html_taulukko, unsafe_allow_html=True)

    st.write("---")

    # --- VALUUTTAMUUNNIN OSION ---
    st.markdown("### **VALUUTTAMUUNNIN (SMK -> EUR)**")
    st.write("Laske haluamasi Uusien markkojen määrä euroina voimassa olevan kurssin mukaan:")
    
    markat = st.number_input("Syota SMK-maara:", min_value=1, value=100, step=1)
    euroina = markat * smk_eur
    
    # Muunnintulos siistissä 90-luvun tekstilaatikossa
    st.text(f" HUOMIO: {markat} SMK on talla hetkella arvoltaan {euroina:.2f} EUR.")

    st.write("---")
    
    st.write("[Ohjeita sivulla liikkujille] [Sisällysluettelo] [Tekstiversio]")
    st.caption("Powered by Silicon Graphics Computer Systems & Streamlit Engine. All rights reserved 2026.")

except Exception as e:
    st.write("**VIRHE: Järjestelmä ei saanut yhteyttä valuuttatietokoneeseen.**")
