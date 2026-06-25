import streamlit as st
import urllib.request
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sivun asetukset - PÄIVITETTY SIVUN NIMI CAPS LOCKILLA
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
    # 1. Haetaan reaaliaikaiset valuuttakurssit ja hopea (XAG)
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    if "XAG" in rates and rates["XAG"] > 0:
        hopea_unssi_usd = 1.0 / float(rates["XAG"])
    else:
        hopea_unssi_usd = 30.75

    # Lasketaan 1 SMK arvo (1 SMK = 0.5g hopeaa)
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
        {"lyhenne": "SMK", "arvo": smk_arvo, "bold": True},
        {"lyhenne": "GBP", "arvo": gbp_arvo, "bold": False},
        {"lyhenne": "EUR", "arvo": eur_arvo, "bold": False},
        {"lyhenne": "USD", "arvo": usd_arvo, "bold": False},
        {"lyhenne": "CNY", "arvo": cny_arvo, "bold": False},
        {"lyhenne": "RUB", "arvo": rub_arvo, "bold": False},
        {"lyhenne": "JPY", "arvo": jpy_arvo, "bold": False},
        {"lyhenne": "SEK", "arvo": sek_arvo, "bold": False},
        {"lyhenne": "NOK", "arvo": nok_arvo, "bold": False},
        {"lyhenne": "CHF", "arvo": chf_arvo, "bold": False},
        {"lyhenne": "CAD", "arvo": cad_arvo, "bold": False},
        {"lyhenne": "AUD", "arvo": aud_arvo, "bold": False},
        {"lyhenne": "INR", "arvo": inr_arvo, "bold": False}
    ]
    
    # Järjestetään kurssit: kallein ylimpänä
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # --- JAETAAN SIVU KAHTEEN PALKKIIN ---
    col_taulukko, col_kaavio = st.columns([1, 1])

    with col_taulukko:
        st.markdown("### **PÖRSSIPÄÄTE / TEKSTI-TV SIVU 331**")
        
        # Rakennetaan aito Teksti-TV ruutu
        html_rows = ""
        for i, v in enumerate(valuutat, start=1):
            if v["arvo"] >= 1.0000:
                vari_koodi = "#00FF00" # Kirkas vihreä
            else:
                vari_koodi = "#FF0000" # Kirkas punainen

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
        st.markdown("### **GRAPH-VERTAILU (3D-RETROTYYLI)**")
        
        # Luodaan uniikit värit kullekin valuuttapalkille (retro-pörssivärit)
        retrovärit = [
            '#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33F3', 
            '#33FFF0', '#FFA500', '#8A2BE2', '#00FF00', '#FF0000',
            '#00FFFF', '#FFFF00', '#FF00FF'
        ]
        
        X_tunnukset = [v["lyhenne"] for v in valuutat]
        Y_arvot = [v["arvo"] for v in valuutat]
        
        # Rakennetaan tyylikäs 3D-efektillä varustettu sylinteri/palkisto Plotlylla
        fig = go.Figure(data=[go.Bar(
            x=X_tunnukset,
            y=Y_arvot,
            marker_color=retrovärit[:len(X_tunnukset)], # Annetaan kaikille eri väri
            marker_line_color='#000000',
            marker_line_width=1.5,
            opacity=0.85
        )])
        
        # Tehdään muotoilusta retro: tumma tausta, paksut viivat ja varjostukset
        fig.update_layout(
            plot_bgcolor='#111111',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Courier New, monospace", size=12, color="#000000"),
            margin=dict(l=20, r=20, t=20, b=20),
            height=420,
            barmode='group',
            bargap=0.15
        )
        
        # Lisätään 3D-efektiä matkiva varjostus ("pattern") palkkeihin
        fig.update_traces(marker_pattern_shape="/") 
        
        st.plotly_chart(fig, use_container_width=True)

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
