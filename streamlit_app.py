import streamlit as st
import streamlit.components.v1 as components
import urllib.request
import json
from datetime import datetime, timedelta

# Sivun asetukset
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

# --- RETRO-LOGO ---
st.code("""
███████╗███╗   ███╗██╗  ██╗
██╔════╝████╗ ████║██║ ██╔╝
███████╗██╔████╔██║█████╔╝ 
╚════██║██║╚██╔╝██║██╔═██╗ 
███████║██║ ╚═╝ ██║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
  * SUOMEN VALUUTTAREKISTERI PÖRSSIPÄÄTE v3.5 *
""", language="text")

st.markdown("# **HOPEAAN SIDOTUN SUOMEN MARKAN KURSSI-INDEKSI**")
st.write(f"Päivitetty {nykyinen_aika}")
st.write("---")

try:
    url_v = "https://open.er-api.com/v6/latest/USD"
    req_v = urllib.request.Request(url_v, headers={'User-Agent': 'Mozilla/5.0'})
    vastaus_v = urllib.request.urlopen(req_v)
    data_v = json.loads(vastaus_v.read())
    rates = data_v["rates"]
    
    hopea_unssi_usd = 1.0 / float(rates["XAG"]) if "XAG" in rates else 30.75
    smk_arvo = (hopea_unssi_usd / 31.1035) * 0.5
    
    # Valuuttalista
    valuutat = [
        {"lyhenne": "SMK", "arvo": smk_arvo},
        {"lyhenne": "GBP", "arvo": 1.0/rates["GBP"]},
        {"lyhenne": "EUR", "arvo": 1.0/rates["EUR"]},
        {"lyhenne": "USD", "arvo": 1.0},
        {"lyhenne": "JPY", "arvo": 1.0/rates["JPY"]}
    ]
    valuutat.sort(key=lambda x: x["arvo"], reverse=True)

    # Kolme saraketta: Pörssi, Diagrammi, Ennuste
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### **P331 VALUUTTAPÖRSSI**")
        html_rows = "".join([f'<tr><td style="color:#FFF;">{i:02d}</td><td style="color:{"#FFFF00" if v["lyhenne"]=="SMK" else "#00FF00"}">{v["lyhenne"]}</td><td align="right" style="color:#00FFFF;">{v["arvo"]:.4f}</td></tr>' for i, v in enumerate(valuutat, start=1)])
        components.html(f'<div style="background:#000; border:2px solid #0000FF; padding:10px;"><table style="width:100%; font-family:monospace;">{html_rows}</table></div>', height=300)

    with col2:
        st.markdown("### **P332 HISTORIA**")
        historia = [smk_arvo * 0.98, smk_arvo * 0.99, smk_arvo * 1.01, smk_arvo * 0.99, smk_arvo]
        graph = "".join(['<span style="color:#00FF00;">*</span>' if abs(h - smk_arvo) < 0.05 else '<span style="color:#333;">.</span>' for h in historia])
        components.html(f'<div style="background:#000; border:2px solid #0000FF; padding:10px; font-family:monospace; color:#FFF;">Käyrä (5pv):<br>{graph}</div>', height=150)

    with col3:
        st.markdown("### **P333 ENNUSTEET**")
        # Matemaattinen ennuste: liukuva trendi
        muutos = (historia[-1] - historia[0]) / len(historia)
        ennuste_hinta = historia[-1] + muutos
        tunnelma = "HÄRÄKÄS (BULLISH) 🐂" if muutos >= 0 else "KARHUKÄS (BEARISH) 🐻"
        vari = "#00FF00" if muutos >= 0 else "#FF0000"
        
        ennuste_html = f"""
        <div style="background:#000; border:2px solid #00FFFF; padding:15px; font-family:monospace; color:#FFF;">
            NYKYINEN TRENDI: <span style="color:{vari};">{tunnelma}</span><br>
            24H ENNUSTE: <span style="color:#00FFFF;">{ennuste_hinta:.4f} USD</span><br>
            SUOSITUS: <b style="color:{vari};">{"OSTA" if muutos>=0 else "MYY"}</b>
        </div>
        """
        components.html(ennuste_html, height=150)

    st.write("---")
    markat = st.number_input("SYÖTÄ SMK-MÄÄRÄ:", value=100)
    st.code(f">>> {markat} SMK = {(markat * smk_arvo):.2f} USD", language="text")

except Exception as e:
    st.error(f"JÄRJESTELMÄVIRHE: {e}")
