import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime

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
        
        html_rows = ""
        for i, v in enumerate(valuutat, start=1):
            if v["arvo"] >= 1.0000:
                vari_koodi = "#00FF00" # Vihreä
            else:
                vari_koodi = "#FF0000" # Punainen

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
                <td style="color: #FFFFFF; font-family: monospace;">{i:02d}</td>
                <td {väri_tyyli}>{nimi_str}</td>
                <td align="right" style="color: #00FFFF; font-family: monospace;">{arvo_str}</td>
            </tr>
            """
            
        teksti_tv_laatikko = f"""
        <div style="background-color: #000000; padding: 15px; border: 4px solid #0000FF; font-family: 'Courier New', monospace; min-height: 400px;">
            <div style="color: #FFFF00; font-weight: bold; font-size: 18px; margin-bottom: 10px; border-bottom: 2px dashed #FFFF00; padding-bottom: 5px;">
                P331  VALUUTTAKURSSIT (USD)
            </div>
            <table cellpadding="4" cellspacing="0" style="width: 100%; font-size: 16px; font-family: monospace;">
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
        # Komponentti upottaa HTML:n eristetysti, jolloin se toimii varmasti
        components.html(teksti_tv_laatikko, height=450)

    with col_kaavio:
        st.markdown("### **PÖRSSIPÄÄTE / TEKSTI-TV SIVU 332**")
        
        kallein_arvo = max([v["arvo"] for v in valuutat]) if valuutat else 1.0
        
        chart_rows = ""
        for v in valuutat:
            palkin_pituus = int((v["arvo"] / kallein_arvo) * 16)
            palkin_pituus = max(1, palkin_pituus)
            palikat = "█" * palkin_pituus
            
            if v["lyhenne"] == "SMK":
                palkki_vari = "#FFFF00"
                tunnus_str = f"<b>*{v['lyhenne']}*</b>"
            elif v["arvo"] >= 1.0000:
                palkki_vari = "#00FF00"
                tunnus_str = v["lyhenne"]
            else:
                palkki_vari = "#00FFFF"
                tunnus_str = v["lyhenne"]
                
            chart_rows += f"""
            <tr>
                <td style="color: #FFFFFF; width: 60px; font-family: monospace;">{tunnus_str}</td>
                <td style="color: {palkki_vari}; font-size: 16px; letter-spacing: 1px; font-family: monospace;">{palikat}</td>
                <td align="right" style="color: #FFFF00; width: 70px; font-family: monospace;">{v['arvo']:.2f}</td>
            </tr>
            """
            
        teksti_tv_kaavio = f"""
        <div style="background-color: #000000; padding: 15px; border: 4px solid #0000FF; font-family: 'Courier New', monospace; min-height: 400px;">
            <div style="color: #FFFF00; font-weight: bold; font-size: 18px; margin-bottom: 10px; border-bottom: 2px dashed #FFFF00; padding-bottom: 5px;">
                P332  DIAGRAMMI-VERTAILU
            </div>
            <table cellpadding="4" cellspacing="0" style="width: 100%; font-size: 15px; font-family: monospace;">
                <tr style="color: #FFFF00; font-weight: bold;">
                    <td align="left">TUNNUS</td>
                    <td align="left">GRAAFI (USD-SUHDE)</td>
                    <td align="right">USD</td>
                </tr>
                {chart_rows}
            </table>
            <div style="color: #FFFFFF; font-size: 11px; margin-top: 13px; text-align: left; border-top: 1px dashed #333333; padding-top: 5px;">
                Selite: <span style="color:#00FF00;">██</span> &gt; 1 USD | <span style="color:#00FFFF;">██</span> &lt; 1 USD | <span style="color:#FFFF00;">██</span> = SMK
            </div>
        </div>
        """
        components.html(teksti_tv_kaavio, height=450)

    st.write("---")

    # --- VALUUTTAMUUNNIN JA ESITTELYOSIO ---
    st.markdown("### **VALUUTTAMUUNNIN JA VALUUTTAESITTELY**")
    
    st.info("""
    **TIEDOTE: MIKÄ ON SUOMEN MARKKA (SMK)?**
    
    Uusi Suomen Markka (SMK) on nykyaikaiseen puhtaaseen hopeakantaan sidottu vakaa viitevaluutta. 
    Toisin kuin valtiolliset fiat-valuutat (kuten EUR tai USD), joiden arvo perustuu luottamukseen ja keskuspankkien sääntelyyn, SMK:n arvo on sidottu suoraan fyysiseen reaalivarallisuuteen.
    
    **MÄÄRITYS JA LASKENTAPERUSTE:**
    * **1 SMK = tasan 0,5 grammaa puhdasta hopeaa.**
    * Järjestelmä laskee SMK:n dynaamisen arvon sekunnilleen maailmanmarkkinoiden virallisen hopean unssihinnan (XAG/USD) perusteella.
    * Koska yksi troy-unssi on 31,1035 grammaa, saadaan SMK:n dollarivastus kaavalla: 
      `((Hopean unssihinta USD / 31.1035) * 0.5)`.
    
    Tämän ansiosta SMK toimii matemaattisen tarkkana inflaatiosuojana, joka peilaa reaaliaikaisesti jalometallin globaalia pörssiarvoa suhteessa muihin maailmanvaluuttoihin.
    """)
    
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
