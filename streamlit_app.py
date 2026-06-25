import streamlit as st
import urllib.request
import json
import pandas as pd
from datetime import datetime

# Sivun asetukset - SIVUN NIMI MUUTETTU CAPS LOCKILLA
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

# --- PÄÄSIVUN OTSIKKO CAPS LOCKILLA ---
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
    
    # Valuuttojen arvot dollareina (Paljonko 1 yksikkö on USD)
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
        {"lyhenne": "CNY", "arvo": cny_arvo},
        {"lyhenne": "RUB", "arvo": rub_arvo},
        {"lyhenne": "JPY", "arvo": jpy_arvo},
        {"lyhenne": "SEK", "arvo": sek_arvo},
        {"lyhenne": "NOK", "arvo": nok_arvo},
        {"lyhenne": "CHF", "arvo": chf_arvo},
        {"lyhenne": "CAD", "arvo": cad_arvo},
        {"lyhenne": "AUD", "arvo": aud_arvo},
        {"lyhenne": "INR", "arvo": inr_arvo}
    ]
    
    # Järjestetään kurssit: kallein ylimpänä
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # --- JAETAAN SIVU KAHTEEN PALKKIIN ---
    col_taulukko, col_kaavio = st.columns([1, 1])

    with col_taulukko:
        st.markdown("### **PÖRSSIPÄÄTE / TEKSTI-TV SIVU 331**")
        
        # Rakennetaan aito Teksti-TV-ruutu HTML-muotoilulla
        html_rows = ""
        for i, v in enumerate(valuutat, start=1):
            # Teksti-TV värit: Vihreä tai Punainen neonväri suhteessa dollariin
            if v["arvo"] >= 1.0000:
                vari_koodi = "#00FF00" # Kirkas Teksti-TV-vihreä
            else:
                vari_koodi = "#FF0000" # Kirkas Teksti-TV-punainen

            # Jos kyseessä on SMK, pidetään se korostettuna (bold) ja ympäröidään asteriskeilla
            if v["lyhenne"] == "SMK":
                väri_tyyli = f'style="color: {vari_koodi}; font-weight: bold; background-color: #222222;"'
                nimi_str = f"*{v['lyhenne']}*"
                arvo_str = f"{v['arvo']:.4f}"
            else:
                väri_tyyli = f'style="color: {vari_koodi};"'
                nimi_str = v["lyhenne"]
                arvo_str = f"{v['arvo']:.4f}"
                
            html_rows += f"""
            <tr>
                <td style="color: #FFFFFF;">{i:02d}</td>
                <td {väri_tyyli}>{nimi_str}</td>
                <td align="right" style="color: #00FFFF;">{arvo_str}</td>
            </tr>
            """
            
        teksti_tv_laatikko = f"""
        <div style="background-color: #000000; padding: 15px; border: 4px solid #0000FF; font-family: 'Courier New', monospace; max-width: 420px; box-shadow: 5px 5px 0px #888888;">
            <div style="color: #FFFF00; font-weight: bold; font-size: 18px; margin-bottom: 10px; border-bottom: 2px dashed #FFFF00; padding-bottom: 5px;">
                P331  VALUUTTAKURSSIT (USD)
            </div>
            <table cellpadding="4" cellspacing="0" style="width: 100%; font-size: 16px;">
                <tr style="color: #FFFF00; font-weight: bold;">
                    <td align="left" style="width: 50px;">SIJA</td>
                    <td align="left">TUNNUS</td>
                    <td align="right">USD-ARVO</td>
                </tr>
                {html_rows}
            </table>
            <div style="color: #00FFFF; font-size: 12px; margin-top: 15px; text-align: center; border-top: 1px solid #333333; padding-top: 5px;">
                SUOMEN VALUUTTAREKISTERI LASKURI
            </div>
        </div>
        """
        st.html(teksti_tv_laatikko)

    with col_kaavio:
        st.markdown("### **GRAPH-VERTAILU (INDEKSI %)**")
        
        # Luodaan kevyt ja varma data kaaviolle ilman ulkoisia kirjastoja (prosentteina)
        chart_data = pd.DataFrame(
            [v["arvo"] * 100 for v in valuutat],
            index=[v["lyhenne"] for v in valuutat],
            columns=["Suhde dollariin (%)"]
        )
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
    st.error(f"JÄRJESTELMÄVIRHE: Tietokoneeseen ei saatu yhteyttä. Syy: {e}")
