import streamlit as st
import urllib.request
import json
import pandas as pd
from datetime import datetime

# Sivun asetukset
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI", layout="wide")

# Haetaan kellonaika
nykyinen_aika = datetime.now().strftime("%H:%M:%S")

# --- VASEMMAN REUNAN NAVIGAATIOPALKKI ---
with st.sidebar:
    st.markdown("### **VALIKKO**")
    st.markdown("[INDEKSI-ETUSIVU](#hopeaan-sidotun-suomen-markan-kurssiindeksi)")
    st.markdown("---")
    st.markdown("**RAHOITUSLINKIT:**")
    st.markdown("[Reuters Financial Systems](https://www.reuters.com)")
    st.markdown("[Bloomberg Markets](https://www.bloomberg.com)")
    st.markdown("---")
    st.write("Webmaster: admin@smk.index")

# --- PÄÄSIVUN OTSIKKO ---
st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI**")
st.write(f"Suomen Valuuttarekisteri — Sivu perustettu 2026 — Päivitetty {nykyinen_aika}")
st.write("---")

try:
    # 1. Haetaan reaaliaikaiset valuuttakurssit
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    # 2. Hopean hinnan haku (kiinteä fallback jos demo-raja täynnä)
    hopea_unssi_usd = 30.75

    # Lasketaan 1 SMK arvo (1 SMK = 0.5g hopeaa)
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_arvo = hopea_gramma_usd * 0.5
    
    # Valuuttojen arvot dollareina (Vain lyhenteet käytössä)
    usd_arvo = 1.0000
    eur_arvo = 1.0 / float(rates["EUR"])
    gbp_arvo = 1.0 / float(rates["GBP"])
    cny_arvo = 1.0 / float(rates["CNY"])
    rub_arvo = 1.0 / float(rates["RUB"])
    jpy_arvo = 1.0 / float(rates["JPY"])
    
    # Luodaan lista rankingia varten
    valuutat = [
        {"lyhenne": "SMK", "arvo": smk_arvo, "bold": True},
        {"lyhenne": "GBP", "arvo": gbp_arvo, "bold": False},
        {"lyhenne": "EUR", "arvo": eur_arvo, "bold": False},
        {"lyhenne": "USD", "arvo": usd_arvo, "bold": False},
        {"lyhenne": "CNY", "arvo": cny_arvo, "bold": False},
        {"lyhenne": "RUB", "arvo": rub_arvo, "bold": False},
        {"lyhenne": "JPY", "arvo": jpy_arvo, "bold": False}
    ]
    
    # Järjestetään kurssit: kallein ylimpänä
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # --- JAETAAN SIVU KAHTEEN PALKKIIN (TAULUKKO JA DIAGRAMMI VIEREKKÄIN) ---
    col_taulukko, col_kaavio = st.columns([1, 1])

    with col_taulukko:
        st.markdown("### **VIRALLISET NOTEERAUKSET (USD)**")
        
        # Aloitetaan puhtaan HTML-taulukon rakentaminen
        html_rows = ""
        for i, v in enumerate(valuutat, start=1):
            # Valitaan tekstin väri arvon mukaan (Yli 1 USD = Vihreä, alle 1 USD = Punainen)
            # SMK on aina vihreä ja lihavoitu, koska se edustaa hopeakantaa
            if v["lyhenne"] == "SMK":
                väri_tyyli = 'style="color: #008000; font-weight: bold;"' # Vihreä
                nimi_str = f"<b>{v['lyhenne']}</b>"
                arvo_str = f"<b>{v['arvo']:.4f} USD</b>"
                rivi_bg = 'style="background-color: #f5f5f5;"'
            else:
                if v["arvo"] >= 1.0:
                    väri_tyyli = 'style="color: #008000;"' # Vihreä (Vahva valuutta)
                else:
                    väri_tyyli = 'style="color: #FF0000;"' # Punainen (Heikko valuutta)
                
                nimi_str = v["lyhenne"]
                arvo_str = f"{v['arvo']:.4f} USD"
                rivi_bg = ""
                
            html_rows += f"""
            <tr {rivi_bg}>
                <td>{i}.</td>
                <td {väri_tyyli}>{nimi_str}</td>
                <td align="right" {väri_tyyli}>{arvo_str}</td>
            </tr>
            """
            
        koko_taulukko = f"""
        <table border="3" cellpadding="8" cellspacing="0" style="font-family: monospace; width: 100%; max-width: 400px; border-color: #808080;">
            <tr bgcolor="#d3d3d3">
                <th align="left" style="width: 50px;">SIJA</th>
                <th align="left">TUNNUS</th>
                <th align="right">ARVO (USD)</th>
            </tr>
            {html_rows}
        </table>
        """
        st.html(koko_taulukko)

    with col_kaavio:
        st.markdown("### **VALUUTTOJEN ARVOVERTAILU (USD)**")
        
        # Valmistellaan data Streamlitin pylvääseen (Pandas DataFrame)
        chart_data = pd.DataFrame(
            [v["arvo"] for v in valuutat],
            index=[v["lyhenne"] for v in valuutat],
            columns=["USD-Arvo"]
        )
        # Piirretään pylväsdiagrammi
        st.bar_chart(chart_data)

    st.write("---")

    # --- VALUUTTAMUUNNIN OSION ---
    st.markdown("### **VALUUTTAMUUNNIN (SMK -> EUR)**")
    st.write("Laske haluamasi Uusien markkojen määrä euroina voimassa olevan kurssin mukaan:")
    
    markat = st.number_input("Syötä SMK-määrä:", min_value=1, value=100, step=1)
    smk_eur_suhde = smk_arvo / eur_arvo
    euroina = markat * smk_eur_suhde
    
    st.code(f">>> {markat} SMK on tällä hetkellä arvoltaan {euroina:.2f} EUR", language="text")

    st.write("---")
    st.write("[Ohjeita sivulla liikkujille] [Sisällysluettelo] [Tekstiversio]")
    st.caption("Powered by Silicon Graphics Computer Systems & Streamlit Engine. All rights reserved 2026.")

except Exception as e:
    st.error(f"JÄRJESTELMÄVIRHE: Tietokoneeseen ei saaju yhteyttä. Syy: {e}")
