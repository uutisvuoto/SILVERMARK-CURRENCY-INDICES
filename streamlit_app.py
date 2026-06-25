import streamlit as st
import urllib.request
import json

# Asetetaan sivun perustiedot
st.set_page_config(page_title="SMK Valuuttalasku- ja kurssi-indeksi", layout="wide")

# --- VASEMMAN REUNAN NAVIGAATIOPALKKI (90-LUVUN TYYLIIN) ---
with st.sidebar:
    st.markdown("### **VALIKKO**")
    st.markdown("[SMK-ETUSIVU](#uuden-markan-smk-virallinen-kurssi-indeksi)")
    st.markdown("[VALUUTTAKURSSIT](#viralliset-kurssinoteeraukset)")
    st.markdown("[VALUUTTAMUUNNIN](#valuuttamuunnin)")
    st.markdown("---")
    st.markdown("**LINKKEJÄ MAAILMALLE:**")
    st.markdown("[Reuters Financial Systems](https://www.reuters.com)")
    st.markdown("[Yleisradio (Teksti-TV)](https://yle.fi/tekstitv)")
    st.markdown("---")
    st.write("Yhteydenotot: webmaster@smk.index")

# --- PÄÄSIVUN SISÄLTÖ ---

# Otsikko isolla fontilla ilman muotoiluja, kuten vanha <h1>-tunniste
st.markdown("# **UUDEN MARKAN (SMK) VIRALLINEN KURSSI-INDEKSI**")
st.write("Yleisradioverkko / Suomen Valuuttarekisteri — Sivu perustettu 1997 — Päivitetty reaaliajassa")
st.write("---")

try:
    # Haetaan markkinadata (pohjana USD)
    url = "https://open.er-api.com/v6/latest/USD"
    vastaus = urllib.request.urlopen(url)
    data = json.loads(vastaus.read())
    
    kurssit_usd_suhteessa = data["rates"]
    
    # Valuuttamuunnokset dollarista
    eur_in_usd = 1 / kurssit_usd_suhteessa["EUR"]
    gbp_in_usd = 1 / kurssit_usd_suhteessa["GBP"]
    cny_in_usd = 1 / kurssit_usd_suhteessa["CNY"]
    rub_in_usd = 1 / kurssit_usd_suhteessa["RUB"]
    jpy_in_usd = 1 / kurssit_usd_suhteessa["JPY"]
    
    # Hopean unssihinta globaaleilla markkinoilla (viite vuoden 2026 tasoon)
    hopea_unssi_usd = 30.50
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    smk_usd = hopea_gramma_usd * 0.5
    
    # SMK-arvot eri valuutoissa
    smk_eur = smk_usd / eur_in_usd
    smk_gbp = smk_usd / gbp_in_usd
    smk_cny = smk_usd / cny_in_usd
    smk_rub = smk_usd / rub_in_usd
    smk_jpy = smk_usd / jpy_in_usd

    # --- VIRALLISET KURSSINOTEERAUKSEN TAULUKKOMUODOSSA ---
    st.markdown("### **VIRALLISET KURSSINOTEERAUKSET**")
    st.write("Valuuttakurssit haettu suoraan keskustietokoneelta. 1 SMK = kiinteästi 0,5g hopeaa.")
    
    # Tehdään perinteinen HTML-henkinen tekstitaulukko
    st.text(f"""
------------------------------------------------------------
 VALUUTTAYKSIKKÖ          | NIMELLISARVO (1 SMK)
------------------------------------------------------------
 Euro (EUR)               | {smk_eur:.4f}
 US-Dollari (USD)         | {smk_usd:.4f}
 Iso-Britannian Punta     | {smk_gbp:.4f}
 Kiinan Yuan (CNY)        | {smk_cny:.4f}
 Venäjän Rupla (RUB)      | {smk_rub:.4f}
 Japanin Jeni (JPY)       | {smk_jpy:.4f}
------------------------------------------------------------
 Viitekurssi: 1 EUR       | {(1 / smk_eur):.4f} SMK
------------------------------------------------------------
    """)

    st.write("---")

    # --- VALUUTTAMUUNNIN OSION ---
    st.markdown("### **VALUUTTAMUUNNIN**")
    st.write("Syötä haluamasi Uusien markkojen (SMK) määrä laskemista varten:")
    
    # Käyttäjän syöte
    markat = st.number_input("SMK-MÄÄRÄ:", min_value=1, value=100, step=1)
    euroina = markat * smk_eur
    
    # Tulos esitettynä karuna päätetekstinä
    st.text(f" HUOMIO: {markat} SMK on tällä hetkellä arvoltaan {euroina:.2f} EUR.")

    st.write("---")
    
    # Alatunnisteen linkit kuten Ylen sivun alalaidassa
    st.write("[Ohjeita sivulla liikkujille] [Sisällysluettelo] [Tekstiversio]")
    st.caption("Powered by Silicon Graphics Computer Systems & Streamlit Engine. All rights reserved 1997-2026.")

except Exception as e:
    st.write("**VIRHE: Järjestelmä ei saanut yhteyttä valuuttatietokoneeseen.**")
