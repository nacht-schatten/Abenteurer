import streamlit as st
import numpy as np
import random



st.set_page_config(
    page_title="Finde alle Fallen!",
    page_icon="🔦",
    layout="centered",
    initial_sidebar_state="expanded"
)



st.title("Finde alle Fallen!")



st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Courier+Prime&display=swap" rel="stylesheet">
    <style>
    .schreibmaschine {
        font-family: 'Courier Prime', monospace;
        font-size: 17px;
        line-height: 1.2;
    }
    </style>
""", unsafe_allow_html=True)



if "level_fixiert" not in st.session_state or not st.session_state.level_fixiert:
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Caveat&display=swap" rel="stylesheet">
    <style>
    .handfont {
        font-family: 'Caveat', cursive;
        font-size: 20px;
        line-height: 1.4;
    }
    </style>
    <div class="handfont">
Sei gegrüßt, Abenteurer!

Du bist sicherlich wegen meiner Reichtümer hier. - Nun, sie gehören dir! ...wenn du an meinen Fallen vorbeikommst.
Je größer das Rikiso, desto größer der Schatz!

Hier, nimm ein paar Kieselsteine zum Werfen, sie werden dir helfen, die Fallen zu finden, bevor du selbst hineingerätst.
Aber bedenke, du musst immer zwei Steine gleichzeitig werfen! Lausche und höre, wieviele Fallen zuschnappen!
</div>
""", unsafe_allow_html=True)
    level = st.selectbox("🧭 Wie mutig bist du heute?", ["Angsthase (6x6)", "Vorsichtig (7x7)", "Furchtlos (8x8)", "Abenteurer (9x9)", "Draufgänger (10x10)"])
    if st.button("🗝️ Schatzkammer betreten"):
        st.session_state.level = level
        st.session_state.level_fixiert = True
        st.rerun()
else:
    st.markdown(f"🧭 Gewählter Modus: **{st.session_state.level}**")


if "level" in st.session_state:
    level = st.session_state.level
    
else:
    st.warning("⚠️ Wähle einen Modus und betrete die Schatzkammer bevor du werfen kanns!")
    st.stop()  # verhindert weitere Ausführung bis Level gewählt wurde




###########################


# Größer und/oder mehr! ;)
if level == "Angsthase (6x6)":
    f = 6
    schiffe = [5, 4, 3, 1]
    MAX_ZUEGE = 17
elif level == "Vorsichtig (7x7)":
    f = 7
    schiffe = [5, 4, 3, 2, 2]
    MAX_ZUEGE = 25
elif level == "Furchtlos (8x8)":
    f = 8
    schiffe = [6, 5, 4, 3, 2, 2, 1]
    MAX_ZUEGE = 30
elif level == "Abenteurer (9x9)":
    f = 9
    schiffe = [7, 6, 5, 4, 3, 2, 1]
    MAX_ZUEGE = 40
else:
    f = 10
    schiffe = [7, 6, 5, 4, 3, 2, 2, 1, 1]
    MAX_ZUEGE = 50






# --- Spielfeldfunktionen ---
def erstelle_spielfeld(size=f):
    return np.zeros((size, size), dtype=int)

def ist_umgebung_frei(spielfeld, r, c):
    size = len(spielfeld)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                if spielfeld[nr][nc] == 1:
                    return False
    return True




def generiere_freie_schiffsform(spielfeld, laenge):
    size = len(spielfeld)

    while True:
        r0, c0 = random.randint(0, size-1), random.randint(0, size-1)
        if spielfeld[r0][c0] != 0 or not ist_umgebung_frei(spielfeld, r0, c0):
            continue

        schiff = [(r0, c0)]

        while len(schiff) < laenge:
            letzte = schiff[-1]
            mögliche = []

            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = letzte[0]+dr, letzte[1]+dc
                if (0 <= nr < size and 0 <= nc < size and
                    (nr, nc) not in schiff and spielfeld[nr][nc] == 0 and ist_umgebung_frei(spielfeld, nr, nc)):
                    mögliche.append((nr, nc))

            if not mögliche:
                break  # ungültiger Pfad → abbrechen

            schiff.append(random.choice(mögliche))

        if len(schiff) == laenge:
            return schiff







def platziere_schiffe(spielfeld, schiffe):

    schiffe_info = []  # ✨ Liste aller Schiffe

    for länge in schiffe:
        platziert = False
        while not platziert:
            pfad = generiere_freie_schiffsform(spielfeld, länge)
            if pfad:
                for r, c in pfad:
                    spielfeld[r][c] = 1
                schiffe_info.append(pfad)
                platziert = True

    return spielfeld, schiffe_info


# --- Grid-Anzeige als HTML-Tabelle ---
def zeige_spielfeld(versuche, wasser_marker, treffer_marker):
    buchstaben = "ABCDEFGHIJ"
    grid_html = "<table style='border-collapse: collapse;'>"
    grid_html += "<tr><th></th>" + "".join([f"<th style='padding: 4px'>{i+1}</th>" for i in range(f)]) + "</tr>"
    for zeile in range(f):
        grid_html += f"<tr><th style='padding: 4px'>{buchstaben[zeile]}</th>"
        for spalte in range(f):
            pos = (zeile, spalte)
            if pos in treffer_marker:
                farbe = "#FFD700"
                symbol = "‼️"
            elif pos in wasser_marker:
                farbe = "#DCDCDC"
                symbol = "🧱"
            elif pos in versuche:
                farbe = "#FF7F7F"
                symbol = "💥"
            else:
                farbe = "#C9B09A"
                symbol = "🟫"
            grid_html += f"<td style='width:24px;height:24px;text-align:center;background-color:{farbe};border:1px solid #ccc'>{symbol}</td>"
        grid_html += "</tr>"
    grid_html += "</table>"
    st.markdown(grid_html, unsafe_allow_html=True)
    
    
    
    
def parse_koordinaten(eingabe, zeilen_map, erlaubte_anzahl=None, label="Eingabe"):
    koordinaten = []
    fehler = None
    gesehen = set()
    
    punkte = [p.strip() for p in eingabe.split(";") if p.strip()]

    for punkt in punkte:
        if len(punkt) < 2:
            fehler = f"⚠️ Ungültige Koordinate '{punkt}' in {label} – zu kurz."
            break
        zeile = punkt[0].upper()
        spalte_str = punkt[1:]
        if zeile not in zeilen_map:
            fehler = f"⚠️ Ungültiger Zeilenbuchstabe '{zeile}' in '{punkt}' ({label})."
            break
        if not spalte_str.isdigit() or not (1 <= int(spalte_str) <= f):
            fehler = f"⚠️ Ungültige Spaltenzahl '{spalte_str}' in '{punkt}' ({label})."
            break
        koord = (zeilen_map[zeile], int(spalte_str) - 1)
        if erlaubte_anzahl == 2 and koord in gesehen:
            fehler = f"⚠️ Koordinate '{punkt}' wurde doppelt eingegeben ({label})."
            break
        gesehen.add(koord)
        koordinaten.append(koord)

    if not fehler and erlaubte_anzahl and len(koordinaten) != erlaubte_anzahl:
        fehler = f"⚠️ Du musst genau {erlaubte_anzahl} unterschiedliche Koordinaten eingeben ({label}) – aktuell: {len(koordinaten)}."

    return koordinaten, fehler    


#------------------------------------------


with st.sidebar:
    st.title("📌 Spielregeln")

    st.markdown(f"""
    **Ziel des Spiels:**  
    Finde alle Fallen und gelange zum Schatz!

    **So funktioniert's:**  
    - Du hast **{MAX_ZUEGE} Züge**, um alle Fallen zu finden.  
    - Bewerfe immer **zwei Felder**.
    - Du erfährst die **Anzahl der Treffer**, aber **nicht, wo** diese erfolgt sind.  
    - Die Züge und deren Ergebnis werden im **Notizbuch** vermerkt:
        - 🟢: 2 Treffer
        - 🟡: 1 Treffer
        - 🔴: 0 Treffer
    - Beworfene Felder werden mit 💥 gekennzeichent.
    - Du kannst **eigene Markierungen** auf die Felder setzten, die du für
        - Sicher 🧱 oder
        - Fallen ‼️ hältst.
    - Hast du alle Steine geworfen, kannst du dich zum Schatz vorwagen!
    """)

    st.markdown("---")
    st.subheader("☠️ Das sind die Fallen:")

    spielschiffe = {
    "Pechregen": 7,     
    "Rotierende Schwerter ": 6,    
    "Fallendes Gitter": 5,
    "Netzfalle": 4,
    "Steinschlag": 3,
    "Giftpfeile": 2,
    "Falltür": 1
    }

# Beispielhafte Schiffsliste
    schiffe_liste = schiffe

# Umkehr-Dictionary: Länge → Name
    laengen_map = {v: k for k, v in spielschiffe.items()}

# Zählen, wie oft jede Länge vorkommt
    from collections import Counter
    anzahl_pro_typ = Counter(schiffe_liste)

# Ausgabe
    for laenge, anzahl in anzahl_pro_typ.items():
        name = laengen_map.get(laenge, f"{laenge}-Felder-Schiff")
        st.markdown(f"- **{anzahl}×** {name}: ({laenge} Feld{'er' if laenge > 1 else ''})")
        
    st.markdown("""
    **Anordnung der Fallen:**
    - Die Felder einer Falle berühren einander an mindestens einer **Seitenfläche**, **nicht an den Ecken**.
    - Die Fallen **berühren** sich **nicht**, auch **nicht diagonal**.
    """)

    st.markdown("---")
    from collections import Counter
    laengen_map = {v: k for k, v in spielschiffe.items()}
    anzahl_pro_typ = Counter(schiffe_liste)

    st.header("🧭 Vermutlich Enttarnt:")

    for laenge, anzahl in anzahl_pro_typ.items():
        name = laengen_map.get(laenge, f"{laenge}-Felder-Schiff")
        for i in range(anzahl):
            key = f"{name}_{i}"
            st.checkbox(f"{name}", key=key)







# --- Session-Setup ---

if "spielfeld" not in st.session_state:
    feld, info = platziere_schiffe(erstelle_spielfeld(f), schiffe)
    st.session_state.spielfeld = feld
    st.session_state.schiffe_info = info

    st.session_state.versuche = []
    st.session_state.zug_nr = 1
    st.session_state.phase = "spiel"
if "rate_abgeschlossen" not in st.session_state:
    st.session_state.rate_abgeschlossen = False
if "schussprotokoll" not in st.session_state:
    st.session_state.schussprotokoll = []
    
    

# --- Eingabe der Koordinaten ---

buchstaben = "ABCDEFGHIJ"
zeilen_map = {buch: idx for idx, buch in enumerate(buchstaben)}

if st.session_state.phase == "spiel":
    st.subheader("🎯 Los geht's! – Wohin willst du zielen?")
    eingabe = st.text_input(f"Du kannst {MAX_ZUEGE} mal werfen. Gibt hier immer zwei Koordinaten so ein: A1;C3", value="A1;C3")
    koordinaten, fehler = parse_koordinaten(eingabe, zeilen_map, erlaubte_anzahl=2, label="Abschuss")
    if fehler:
        st.error(fehler)


    

    if st.button("🏹 Abwerfen!") and len(koordinaten) == 2:
        spielfeld = st.session_state.spielfeld
        treffer = sum(1 for r, c in koordinaten if spielfeld[r, c] == 1)
        st.toast(f"💡 {treffer} Treffer!")
        st.session_state.versuche.extend(koordinaten)
        st.session_state.zug_nr += 1
        st.session_state.schussprotokoll.append((koordinaten, treffer))
        
        

        # Phase-Wechsel prüfen
        if st.session_state.zug_nr > MAX_ZUEGE:
            st.session_state.phase = "raten"
else:
    st.warning("🔒 Keine Steine mehr übrig – du kannst jetzt nicht mehr werfen.")

    
    
    
    
def zeige_auswertung(korrekt, verpasst, daneben):
       buchstaben = "ABCDEFGHIJ"
       html = "<table style='border-collapse: collapse;'>"
       html += "<tr><th></th>" + "".join([f"<th>{i+1}</th>" for i in range(f)]) + "</tr>"

       for r in range(f):
           html += f"<tr><th>{buchstaben[r]}</th>"
           for c in range(f):
               pos = (r, c)
               if pos in korrekt:
                   farbe = "#90EE90"  # grün
                   symbol = "✅"
               elif pos in daneben:
                   farbe = "#FF6961"  # rot
                   symbol = "❌"
               elif pos in verpasst:
                   farbe = "#D3D3D3"  # grau
                   symbol = "❓"
               else:
                    farbe = "#C9B09A"
                    symbol = "🟫"
               html += f"<td style='width:24px;height:24px;text-align:center;background-color:{farbe};border:1px solid #aaa'>{symbol}</td>"
           html += "</tr>"
       html += "</table>"
       st.markdown(html, unsafe_allow_html=True)




##### Columns! ;)  
    
    



wasser_input = st.text_input("🧱 Vermutlich sicher (z. B. A1;B3)")
ratio = 3 if f > 8 else 2
col1, col2 = st.columns([ratio, 1])


with col1:
    
    
    # --- Zusatz-Eingaben für Marker ---
    
    treffer_input = st.text_input("‼️ Vermutete Fallen (z. B. C5;D7)")

    wasser_marker, fehler_wasser = parse_koordinaten(wasser_input, zeilen_map, label="Wasser-Markierung")
    treffer_marker, fehler_treffer = parse_koordinaten(treffer_input, zeilen_map, label="Treffer-Markierung")

    if fehler_wasser:
        st.warning(fehler_wasser)
    if fehler_treffer:
        st.warning(fehler_treffer)
        
    zeige_spielfeld(st.session_state.versuche, wasser_marker, treffer_marker)

with col2:
    st.subheader("Notizbuch")

    if st.session_state.schussprotokoll:
        scroll_html = f"<div class='schreibmaschine' style='max-height:{150+f*35}px; overflow-y:auto; padding:0px;'>"

        for i, (koords, hits) in enumerate(st.session_state.schussprotokoll, 1):
            coords_str = ",".join(f"{chr(65 + r)}{c+1}" for r, c in koords)

            if hits == 2:
                symbol = "🟢"
            elif hits == 1:
                symbol = "🟡"
            else:
                symbol = "🔴"

            scroll_html += f"<div style='margin-bottom:4px; padding:2px; border-radius:4px'>{symbol}Zug {i}: <b>{coords_str} </b></div>"

        scroll_html += "</div>"
        st.markdown(scroll_html, unsafe_allow_html=True)
    else:
        st.info("Noch keine Steine geworfen.")




# Phase initialisieren
if "phase" not in st.session_state:
    st.session_state.phase = "spiel"

# Wenn maximale Züge überschritten → Ratephase
if st.session_state.zug_nr > MAX_ZUEGE:
    st.session_state.phase = "raten"

if st.session_state.phase == "raten":
    st.header("🔍 Wo sind die Fallen?")
    
    spielfeld = st.session_state.spielfeld

    if not st.session_state.rate_abgeschlossen:
        raten_input = st.text_area("📍 Deine Vermutung (z. B. A1;A2;C5):", height=100)
        ratefelder, fehler_raten = parse_koordinaten(raten_input, zeilen_map, label="Rateverdacht")
        if fehler_raten:
            st.warning(fehler_raten)


        if st.button("🙏 Raten abschließen") and not fehler_raten:
            # → Auswertung + Ergebnis speichern/anzeigen
        
            schiffsfelder = [(r, c) for r in range(f) for c in range(f) if spielfeld[r, c] == 1]
            korrekte = [f for f in ratefelder if f in schiffsfelder]
            daneben = [f for f in ratefelder if f not in schiffsfelder]
            verpasst = [f for f in schiffsfelder if f not in ratefelder]
            
          
            st.session_state.ratefelder = ratefelder 
            st.session_state.ratergebnis = (korrekte, daneben, verpasst)
            st.session_state.rate_abgeschlossen = True
            st.rerun()
    else:
    
        # Ergebnis zeigen
        korrekte, daneben, verpasst = st.session_state.ratergebnis
        ratefelder = st.session_state.ratefelder 
        versenkte = [schiff for schiff in st.session_state.schiffe_info if all(pos in ratefelder for pos in schiff)]

        anzahl_versenkt = len(versenkte)
        if anzahl_versenkt < 1:
            st.error("☠️ Keine einzige Falle entdeckt! Dein Skelett wird andere Abentuerer warnen!")
        elif anzahl_versenkt <   len(st.session_state.schiffe_info):
            st.warning(f"🚑 **{anzahl_versenkt}** von {len(st.session_state.schiffe_info)} Fallen entdeckt. Du kommst mit dem Schrecken davon - ohne Schatz.")
        else:
            st.success("🪙 Alle Fallen gefunden! Meine Reichtümer sind dein!")
            st.balloons()
    
        zeige_auswertung(korrekte, verpasst, daneben)

        # Anzeige-Gitter mit Bewertung
     




