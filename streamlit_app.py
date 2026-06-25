import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime, timedelta

# 1. Sivun asetukset
st.set_page_config(page_title="HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI", layout="centered")

# CSS-taika: 4:3 suhde ja musta tausta
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        .block-container {
            max-width: 900px !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            background-color: #000000;
        }
        h1, h2, h3, p, span, label {
            color: #FFFFFF !important;
            font-family: 'Courier New', monospace !important;
        }
        hr { border-color: #333333 !important; }
        /* Tyylitellään Streamlitin valintapainikkeet retrohenkisiksi */
        .stCheckbox label { color: #FF0000 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Haetaan kellonaika
nykyinen_aika = datetime.now().strftime("%H:%M:%S")

# --- RETRO-LOGO ---
st.code("""
███████╗███╗   ███╗██╗  ██╗
██╔════╝████╗ ████║██║ ██╔╝
███████╗██╔████╔██║█████╔╝ 
╚════██║██║╚██╔╝██║██╔═██╗ 
███████║██║ ╚═╝ ██║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
  * SUOMEN VALUUTTAREKISTERI PÖRSSIPÄÄTE v4.0 *
""", language="text")

# --- PÄÄSIVUN OTSIKKO ---
st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI**")
st.write(f"Suomen Valuuttarekisteri — Päivitetty {nykyinen_aika}")
st.write("---")

# --- KRIISISIMULAATTORI (STRESSITESTI) ---
st.markdown("### ⚠️ JÄRJESTELMÄN STRESSITESTI")
sotatila = st.checkbox("AKTIVOI SOTATILA-SIMULAATIO (DEFCON 1)")

if sotatila:
    st.warning("🚨 DEFCON 1: GLOBAALI KONFLIKTI REKISTERÖITY. MARKKINAT PANIIKISSA. KAUPPANKÄYNTI KESKEYTETTY OSITTAIN.")

try:
    # Haetaan reaaliaikaiset valuuttakurssit ja hopea (XAG)
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    if "XAG" in rates and rates["XAG"] > 0:
        hopea_unssi_usd = 1.0 / float(rates["XAG"])
    else:
        hopea_unssi_usd = 30.75

    # --- SIMULAATION VAIKUTUKSET ---
    if sotatila:
        # Hopean hinta moninkertaistuu (Hyper-inflaatiosuoja iskee)
        hopea_unssi_usd = hopea_unssi_usd * 6.0
        
        # Romahdutetaan EUR ja RUB pörssissä
        eur_arvo = (1.0 / float(rates["EUR"])) * 0.20
        rub_arvo = (1.0 / float(rates["RUB"])) * 0.05
        # Muut valuutat ottavat osumaa vaihtelevasti
        gbp_arvo = (1.0 / float(rates["GBP"])) * 0.70
        cny_arvo = (1.0 / float(rates["CNY"])) * 0.60
        jpy_arvo = (1.0 / float(rates["JPY"])) * 0.50
        sek_arvo = (1.0 / float(rates["SEK"])) * 0.40
        nok_arvo = (1.0 / float(rates["NOK"])) * 0.50
        chf_arvo = (1.0 / float(rates["CHF"])) * 1.20 # Sveitsi vahvistuu hieman turvasatamana
        usd_arvo = 1.0000
    else:
        # Normaalitilat
        usd_arvo = 1.0000
        eur_arvo = 1.0 / float(rates["EUR"])
        gbp_arvo = 1.0 / float(rates["GBP"])
        cny_arvo = 1.0 / float(rates["CNY"])
        rub_arvo = 1.0 / float(rates["RUB"])
        jpy_arvo = 1.0 / float(rates["JPY"])
        sek_arvo = 1.0 / float(rates["SEK"])
        nok_arvo = 1.0 / float(rates["NOK"])
        chf_arvo = 1.0 / float(rates["CHF"])

    # Lasketaan 1 SMK arvo (1 SMK = 0.5g hopeaa)
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_arvo = hopea_gramma_usd * 0.5
    
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
        {"lyhenne": "CHF", "arvo": chf_arvo}
    ]
    
    # Järjestetään kurssit: kallein ylimpänä
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # --- PÖRSSIPÄÄTE / TEKSTI-TV SIVU 331 ---
    st.write("---")
    st.markdown("### **PÖRSSIPÄÄTE / TEKSTI-TV SIVU 331**")
    
    html_rows = ""
    for i, v in enumerate(valuutat, start=1):
        if v["lyhenne"] == "SMK":
            vari_koodi = "#FFFF00"
            nimi_str = f"*{v['lyhenne']}*"
            väri_tyyli = f'style="color: {vari_koodi}; font-weight: bold; background-color: #222222;"'
        else:
            # Sotatilassa romahtaneet vilkkuvat punaisina tai ovat punaisia
            if sotatila and v["lyhenne"] in ["EUR", "RUB"]:
                vari_koodi = "#FF0000"
                nimi_str = f"{v['lyhenne']} [ROMAHDUS]"
            else:
                vari_koodi = "#00FF00" if v["arvo"] >= 1.0000 else "#00FFFF"
            
            nimi_str = v["lyhenne"]
            väri_tyyli = f'style="color: {vari_koodi};"'
            
        arvo_str = f"{v['arvo']:.4f}"
        html_rows += f"""
        <tr>
            <td style="color: #FFFFFF; font-family: monospace; width: 60px;">{i:02d}</td>
            <td {väri_tyyli}>{nimi_str}</td>
            <td align="right" style="color: #00FFFF; font-family: monospace;">{arvo_str}</td>
        </tr>
        """
        
    otsikko_lisa = " (SOTATILA-MOODI)" if sotatila else ""
    teksti_tv_laatikko = f"""
    <div style="background-color: #000000; padding: 15px; border: 4px solid {'#FF0000' if sotatila else '#0000FF'}; font-family: 'Courier New', monospace;">
        <div style="color: {'#FF0000' if sotatila else '#FFFF00'}; font-weight: bold; font-size: 18px; margin-bottom: 10px; border-bottom: 2px dashed #FFFF00; padding-bottom: 5px;">
            P331 VALUUTTAKURSSIT{otsikko_lisa}
        </div>
        <table cellpadding="4" cellspacing="0" style="width: 100%; font-size: 16px; font-family: monospace;">
            <tr style="color: #FFFF00; font-weight: bold;">
                <td align="left">SIJA</td>
                <td align="left">TUNNUS</td>
                <td align="right">USD-VASTINE</td>
            </tr>
            {html_rows}
        </table>
    </div>
    """
    components.html(teksti_tv_laatikko, height=360)

    # --- HISTORIALLINEN KÄYRÄ ---
    st.write("---")
    st.markdown("### **PÖRSSIPÄÄTE / TEKSTI-TV SIVU 332**")
    
    paivat = [(datetime.now() - timedelta(days=i)).strftime("%d.%m.") for i in range(4, -1, -1)]
    
    # Jos sotatila on päällä, käyrä ampaisee pystysuoraan ylös
    if sotatila:
        h_arvot = [smk_arvo * 0.16, smk_arvo * 0.16, smk_arvo * 0.18, smk_arvo * 0.20, smk_arvo]
    else:
        h_arvot = [smk_arvo * 0.98, smk_arvo * 0.99, smk_arvo * 1.01, smk_arvo * 0.99, smk_arvo]
        
    min_h, max_h = min(h_arvot), max(h_arvot)
    
    graph_lines = ""
    tasot = 4
    for t in range(tasot, -1, -1):
        taso_arvo = min_h + (t / tasot) * (max_h - min_h) if max_h != min_h else smk_arvo
        line_str = f'<span style="color: #00FFFF;">{taso_arvo:.4f} USD</span> | '
        
        for val in h_arvot:
            if max_h != min_h:
                etaisyys = abs((val - min_h) / (max_h - min_h) * tasot - t)
            else:
                etaisyys = 0 if t == 2 else 99
                
            if etaisyys < 0.5:
                line_str += f'<span style="color: {"#FF0000" if sotatila else "#00FF00"}; font-weight:bold;">*</span>   '
            else:
                line_str += '<span style="color: #333333;">.</span>   '
        graph_lines += line_str + "<br>"
        
    pohja_viiva = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|' + "-------------------<br>"
    paiva_rivi = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + '&nbsp;&nbsp;'.join([f'<span style="color:#FFFF00;">{p}</span>' for p in paivat])

    historia_html = f"""
    <div style="background-color: #000000; padding: 15px; border: 4px solid {'#FF0000' if sotatila else '#0000FF'}; font-family: 'Courier New', monospace;">
        <div style="color: #FFFF00; font-weight: bold; font-size: 18px; margin-bottom: 10px; border-bottom: 2px dashed #FFFF00; padding-bottom: 5px;">
            P332 SMK/USD HISTORIALLINEN KÄYRÄ
        </div>
        <div style="font-size: 15px; line-height: 1.4; font-family: monospace;">
            {graph_lines}
            {pohja_viiva}
            {paiva_rivi}
        </div>
    </div>
    """
    components.html(historia_html, height=220)

    # --- VALUUTTAMUUNNIN ---
    st.write("---")
    st.markdown("### **INTERAKTIIVINEN LASKURI**")
    
    markat = st.number_input("SMK-MÄÄRÄ:", min_value=1, value=100, step=1)
    smk_eur_suhde = smk_arvo / eur_arvo
    euroina = markat * smk_eur_suhde
    
    st.code(f">>> {markat} SMK = {euroina:.2f} EUR (Kurssi: 1 SMK = {smk_eur_suhde:.4f} EUR)", language="text")

    if sotatila:
        st.error("HUOMAUTUS: Euron hyperinflaation vuoksi SMK-määräsi arvo euroissa on moninkertaistunut räjähdysmäisesti. Käteisen euron ostovoima on murentunut.")

    st.write("---")
    st.caption("Suomen Valuuttarekisteri 2026 • KRIISI-TESTAUSTILA VALMIS.")

except Exception as e:
    st.error(f"JÄRJESTELMÄVIRHE: {e}")
