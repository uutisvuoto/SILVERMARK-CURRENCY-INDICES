import streamlit as st
import urllib.request
import json
from datetime import datetime

# Asetetaan sivun nimi ja muotoilu
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSIINDEKSI", layout="wide")

# Haetaan kellonaika sekunnilleen
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
    # Haetaan kurssit luotettavasta rajapinnasta
    url = "https://open.er-api.com/v6/latest/USD"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus = urllib.request.urlopen(req)
    data = json.loads(vastaus.read())
    
    rates = data["rates"]
    
    # 1. Lasketaan kaikkien valuuttojen reaaliaikainen arvo dollareina (USD per 1 yksikkö)
    usd_arvo = 1.0000
    eur_arvo = 1.0 / float(rates["EUR"])
    gbp_arvo = 1.0 / float(rates["GBP"])
    cny_arvo = 1.0 / float(rates["CNY"])
    rub_arvo = 1.0 / float(rates["RUB"])
    jpy_arvo = 1.0 / float(rates["JPY"])
    
    # Hopeakannan laskenta (1 SMK = 0.5 grammaa hopeaa)
    hopea_unssi_usd = 30.50
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_arvo = hopea_gramma_usd * 0.5
    
    # Luodaan puhdas datalista järjestämistä varten
    valuutat = [
        {"nimi": "Suomen Markka (SMK)", "arvo": smk_arvo, "bold": True},
        {"nimi": "Iso-Britannian Punta (GBP)", "arvo": gbp_arvo, "bold": False},
        {"nimi": "Euro (EUR)", "arvo": eur_arvo, "bold": False},
        {"nimi": "US-Dollari (USD)", "arvo": usd_arvo, "bold": False},
        {"nimi": "Kiinan Yuan (CNY)", "arvo": cny_arvo, "bold": False},
        {"nimi": "Venäjän Rupla (RUB)", "arvo": rub_arvo, "bold": False},
        {"nimi": "Japanin Jeni (JPY)", "arvo": jpy_arvo, "bold": False}
    ]
    
    # Järjestetään kalleimmasta halvimpaan (reverse=True)
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # --- REAALIAIKAINEN RANKING-TAULUKKO ---
    st.markdown("### **VIRALLISET KURSSINOTEERAUKSET (USD-RANKING)**")
    st.write("Valuutat järjestetty reaaliaikaisen markkina-arvon mukaan (kallein ylimpänä). Viitestandardi: 1 SMK = 0,5g hopeaa.")
    
    # Tehdään 90-luvun tyylikäs HTML-taulukko kauniilla reunuksella
    html = """
    <table border="3" cellpadding="6" cellspacing="0" style="font-family: monospace; width: 100%; max-width: 600px; border-color: #808080;">
        <tr bgcolor="#d3d3d3">
            <th align="left" style="width: 60px;">SIJA</th>
            <th align="left">VALUUTTAYKSIKKÖ (1 kpl)</th>
            <th align="right">ARVO (USD)</th>
        </tr>
    """
    
    for i, v in enumerate(valuutat, start=1):
        if v["bold"]:
            nimi_str = f"<b>{v['nimi']}</b>"
            arvo_str = f"<b>{v['arvo']:.4f} USD</b>"
            rivi_bg = 'bgcolor="#f5f5f5"'  # Kevyt korostustausta SMK:lle
        else:
            nimi_str = v["nimi"]
            arvo_str = f"{v['arvo']:.4f} USD"
            rivi_bg = ""
            
        html += f"""
        <tr {rivi_bg}>
            <td>{i}.</td>
            <td>{nimi_str}</td>
            <td align="right">{arvo_str}</td>
        </tr>
        """
        
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    st.write("---")

    # --- VALUUTTAMUUNNIN OSION ---
    st.markdown("### **VALUUTTAMUUNNIN (SMK -> EUR)**")
    st.write("Laske haluamasi Uusien markkojen määrä euroina voimassa olevan kurssin mukaan:")
    
    markat = st.number_input("Syötä SMK-määrä:", min_value=1, value=100, step=1)
    smk_eur_suhde = smk_arvo / eur_arvo
    euroina = markat * smk_eur_suhde
    
    st.text(f" HUOMIO: {markat} SMK on tällä hetkellä arvoltaan {euroina:.2f} EUR.")

    st.write("---")
    st.write("[Ohjeita sivulla liikkujille] [Sisällysluettelo] [Tekstiversio]")
    st.caption("Powered by Silicon Graphics Computer Systems & Streamlit Engine. All rights reserved 2026.")

except Exception as e:
    st.error(f"JÄRJESTELMÄVIRHE: Valuuttatietokoneeseen ei saatu yhteyttä. Syy: {e}")
