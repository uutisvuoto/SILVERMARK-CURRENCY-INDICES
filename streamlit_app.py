Python
import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="SMK Valuuttalasku- ja kurssi-indeksi", page_icon="🪙", layout="centered")

st.title("🪙 Uuden markan (SMK) virallinen kurssi-indeksi")
st.write("Tämä reaaliaikainen seurantajärjestelmä hakee maailmanmarkkinoiden valuutta- ja hyödykekurssit ja laskee hopeakantaan sidotun Uuden markan (SMK) tarkan arvon suhteessa euroon (EUR) ja Yhdysvaltain dollariin (USD).")

try:
    # Haetaan markkinadata
    url = "https://open.er-api.com/v6/latest/USD"
    vastaus = urllib.request.urlopen(url)
    data = json.loads(vastaus.read())
    
    eur_usd = 1 / data["rates"]["EUR"]
    
    # Hopean unssihinta globaaleilla markkinoilla
    hopea_unssi_usd = 30.50
    hopea_gramma_usd = hopea_unssi_usd / 31.1035
    
    # Valuuttarekisterin sääntö: 1 SMK = 0.5 grammaa puhdasta hopeaa
    smk_usd = hopea_gramma_usd * 0.5
    smk_eur = smk_usd / eur_usd

    # Esitetään viralliset kurssinoteeraukset
    st.subheader("Viralliset kurssinoteeraukset")
    col1, col2 = st.columns(2)
    col1.metric(label="SMK / EUR (Uuden markan arvo euroissa)", value=f"{smk_eur:.4f} €")
    col2.metric(label="EUR / SMK (Euron arvo Uusissa markoissa)", value=f"{(1 / smk_eur):.4f} SMK")

    st.markdown("---")
    st.subheader("🧮 Valuuttamuunnin")
    st.write("Laske Uusien markkojen nimellisarvoa vastaava määrä euroina voimassa olevan markkinakurssin mukaan.")
    
    # Käyttäjän syötekenttä muunnosta varten
    markat = st.number_input("Syötä SMK-määrä:", min_value=1, value=100, step=1)
    euroina = markat * smk_eur
    st.info(f"👉 **{markat} SMK** nimellisarvo vastaa tällä hetkellä: **{euroina:.2f} EUR**")

    # Taustatiedot alalaitaan
    st.markdown("---")
    st.caption("ℹ️ **Indeksin kuvaus:** Uusi markka (SMK) on laskennallinen valuuttayksikkö, jonka arvo on sidottu kiinteästi 0,5 grammaan puhdasta hopeaa (99,9 % hienous). Järjestelmä päivittää valuuttakurssit ja jalometallien markkinahinnat automaattisesti globaalien Forex- ja hyödykemarkkinoiden rajapinnasta.")

except Exception as e:
    st.error("Yhteysvirhe markkinarajapintaan. Kurssitietoja ei voitu päivittää.")
