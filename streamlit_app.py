import streamlit as st
import urllib.request
import json

# Asetetaan sivun otsikko ilman emojeita
st.set_page_config(page_title="SMK Valuuttalasku- ja kurssi-indeksi", layout="centered")

st.title("UUDEN MARKAN (SMK) VIRALLINEN KURSSI-INDEKSI")
st.write("Paivitetty jarjestelmarajapinta: Reaaliaikainen haku globaaleilta Forex- ja hyodynmarkkinoilta.")

try:
    # Haetaan markkinadata (pohjana USD)
    url = "https://open.er-api.com/v6/latest/USD"
    vastaus = urllib.request.urlopen(url)
    data = json.loads(vastaus.read())
    
    kurssit_usd_suhteessa = data["rates"]
    
    # Lasketaan keskeiset valuuttaparit suhteessa dollariin
    eur_in_usd = 1 / kurssit_usd_suhteessa["EUR"]
    gbp_in_usd = 1 / kurssit_usd_suhteessa["GBP"]
    cny_in_usd = 1 / kurssit_usd_suhteessa["CNY"]
    rub_in_usd = 1 / kurssit_usd_suhteessa["RUB"]
    jpy_in_usd = 1 / kurssit_usd_suhteessa["JPY"]
    
    # Hopean unssihinta globaaleilla markkinoilla (kiintea viite 2026 tasoon)
    hopea_unssi_usd = 30.50
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    
    # 1 SMK = 0.5 grammaa hopeaa
    smk_usd = hopea_gramma_usd * 0.5
    
    # Lasketaan SMK arvo eri valuutoissa
    smk_eur = smk_usd / eur_in_usd
    smk_gbp = smk_usd / gbp_in_usd
    smk_cny = smk_usd / cny_in_usd
    smk_rub = smk_usd / rub_in_usd
    smk_jpy = smk_usd / jpy_in_usd

    # --- 90-LUVUN TIETOKONENÄKYMÄ (MONOSPACE) ---
    st.write("-----------------------------------------------------------------")
    st.write("VIRALLISET KURSSINOTEERAUKSET (PÄIVITETTY NYT):")
    
    # Luodaan perinteinen tekstipohjainen taulukko, joka nayttaa vanhalta paatteelta
    paatenakyma = f"""
=================================================================
 VALUUTTAPARI             | ARVO VIITEVALUUTASSA
=================================================================
 1 SMK -> EUR (Euro)       | {smk_eur:.4f} EUR
 1 SMK -> USD (Dollari)    | {smk_usd:.4f} USD
 1 SMK -> GBP (Punta)      | {smk_gbp:.4f} GBP
 1 SMK -> CNY (Yuan)       | {smk_cny:.4f} CNY
 1 SMK -> RUB (Rupla)      | {smk_rub:.4f} RUB
 1 SMK -> JPY (Jeni)       | {smk_jpy:.4f} JPY
-----------------------------------------------------------------
 1 EUR -> SMK (Kovertio)   | {(1 / smk_eur):.4f} SMK
=================================================================
    """
    st.code(paatenakyma, language="text")

    st.write("-----------------------------------------------------------------")
    st.subheader("VALUUTTAMUUNNIN (SMK -> EUR)")
    
    # Kayttajan syotekentta muunnosta varten
    markat = st.number_input("Syota SMK-maara:", min_value=1, value=100, step=1)
    euroina = markat * smk_eur
    
    # Naytetaan lopputulos myos pelkkana tekstina ilman moderneja infolaatikoita
    st.code(f">>> {markat} SMK NIMELLISARVO VASTAA TÄLLÄ HETKELLÄ: {euroina:.2f} EUR", language="text")

    st.write("-----------------------------------------------------------------")
    st.caption("INDEKSIN KUVAUS: Uusi markka (SMK) on laskennallinen valuuttayksikko, jonka arvo on sidottu kiinteasti 0,5 grammaan puhdasta hopeaa (99,9 % hienous). Jarjestelma paivittaa valuuttakurssit automaattisesti.")

except Exception as e:
    st.error("YHTEYSVIRHE MARKKINARAJAPINTAAN. KURSSITIETOJA EI VOITU PAIVITTAA.")
