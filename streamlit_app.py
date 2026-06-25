import streamlit as st
import urllib.request
import json
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
    # 1. Haetaan reaaliaikaiset valuuttakurssit (pohjana USD)
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    # 2. Haetaan reaaliaikainen hopean hinta hyödykerajapinnasta
    url_h = "https://api.metals.dev/v1/latest?api_key=DEMO_KEY&currency=USD&unit=toz"
    try:
        req_h = urllib.request.Request(url_h, headers={'User-Agent': 'Mozilla/5.0'})
        vastaus_h = urllib.request.urlopen(req_h)
        data_h = json.loads(vastaus_h.read())
        hopea_unssi_usd = float(data_h["metals"]["silver"])
    except Exception:
        # Varajärjestelmä (Fallback), jos metallirajapinnan demorajoitus täyttyy
        hopea_unssi_usd = 30.75

    # Lasketaan 1 SMK arvo (1 SMK = 0.5g hopeaa, unssi = 31.1035g)
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_arvo = hopea_gramma_usd * 0.5
    
    # Muunnetaan muut valuutat muotoon: paljonko 1 kpl valuuttaa on dollareina (USD)
    usd_arvo = 1.0000
    eur_arvo = 1.0 / float(rates["EUR"])
    gbp_arvo = 1.0 / float(rates["GBP"])
    cny_arvo = 1.0 / float(rates["CNY"])
    rub_arvo = 1.0 / float(rates["RUB"])
    jpy_arvo = 1.0 / float(rates["JPY"])
    
    # Luodaan lista rankingia varten
    valuutat = [
        {"nimi": "Suomen Markka (SMK)", "arvo": smk_arvo, "bold": True},
        {"nimi": "Iso-Britannian Punta (GBP)", "arvo": gbp_arvo, "bold": False},
        {"nimi": "Euro (EUR)", "arvo": eur_arvo, "bold": False},
        {"nimi": "US-Dollari (USD)", "arvo": usd_arvo, "bold": False},
        {"nimi": "Kiinan Yuan (CNY)", "arvo": cny_arvo, "bold": False},
        {"nimi": "Venäjän Rupla (RUB)", "arvo": rub_arvo, "bold": False},
        {"nimi": "Japanin Jeni (JPY)", "arvo": jpy_arvo, "bold": False}
    ]
    
    # Järjestetään kurssit: kallein ylimpänä
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # --- RAKENNETAAN REAALIAIKAINEN HTML-TAULUKKO ---
    st.markdown("### **VIRALLISET KURSSINOTEERAUKSET (USD-RANKING)**")
    st.write("Valuutat järjestetty reaaliaikaisen markkina-arvon mukaan (kallein ylimpänä). Viitestandardi: 1 SMK = 0,5g hopeaa.")
    
    # Aloitetaan puhtaan HTML-merkkijonon rakentaminen
    html_rows = ""
    for i, v in enumerate(valuutat, start=1):
        if v["bold"]:
            nimi_str = f"<b>{v['nimi']}</b>"
            arvo_str = f"<b>{v['arvo']:.4f} USD</b>"
            rivi_bg = 'style="background-color: #f5f5f5;"'
        else:
            nimi_str = v["nimi"]
            arvo_str = f"{v['arvo']:.4f} USD"
            rivi_bg = ""
            
        html_rows += f"""
        <tr {rivi_bg}>
            <td>{i}.</td>
            <td>{nimi_str}</td>
            <td align="right">{arvo_str}</td>
        </tr>
        """
        
    # Kootaan valmis taulukko yhteen muuttujaan ilman Streamlit-tekstikatkoja
    koko_taulukko = f"""
    <table border="3" cellpadding="6" cellspacing="0" style="font-family: monospace; width: 100%; max-width: 600px; border-color: #808080;">
        <tr bgcolor="#d3d3d3">
            <th align="left" style="width: 60px;">SIJA</th>
            <th align="left">VALUUTTAYKSIKKÖ (1 kpl)</th>
            <th align="right">ARVO (USD)</th>
        </tr>
        {html_rows}
    </table>
    """
    
    # Tulostetaan koko HTML-paketti kerralla
    st.html(koko_taulukko)

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
    st.error(f"JÄRJESTELMÄVIRHE: Tietokoneeseen ei saatu yhteyttä. Syy: {e}")
