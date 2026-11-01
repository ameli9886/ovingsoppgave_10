# DAT120 - Øving 10, oppgave a – Månedlige værdata

# Legg Python-filen i samme mappe som de utpakkede CSV-filene.
from pathlib import Path

# Finn mappen der Python-filen ligger

MAPPE = Path(__file__).resolve().parent
# Bibliotek for å lese CSV-filer
import csv
# Gjør datoer fra tekst om til dato-objekter
from datetime import datetime
# Brukes til å tegne grafer
import matplotlib.pyplot as plt

# Skriv filnavnene akkurat slik de heter i mappen din.
FILER = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025_med_makstemperatur.csv",
}

# HJELPEFUNKSJON: Gjør en måling fra tekst om til tall.
def til_tall(tekst):
    # En strek eller tom celle betyr at målingen mangler.
    # Fjern mellomrom, og bytt norsk desimalkomma til punktum.
    tekst = tekst.strip().replace(",", ".")
    if tekst in ("", "-"):
        return None
    # Prøv å gjøre teksten om til et desimaltall.
    try:
        return float(tekst)
    except ValueError:
        return None


# HJELPEFUNKSJON: Leser én CSV-fil og lager en liste med daglige målinger.
def les_rader(fil):
    # Leser en CSV-fil og lagrer dato og værmålinger.
    resultat = []
    # Semikolon skiller kolonnene i værfilene.
    leser = csv.reader(fil, delimiter=";")
    next(leser, None)  # Hopp over overskriften.
    # Se på én linje i CSV-filen om gangen.
    for rad in leser:
        # Vi trenger minst åtte kolonner.
        if len(rad) < 8:
            continue
        # Datoen står i kolonne 2, for eksempel 31.01.2024.
        try:
            dato = datetime.strptime(rad[2], "%d.%m.%Y")
        except ValueError:
            continue
        # Lagre datoen og de fem målingene som en ordbok.
        # None betyr at en måling mangler.
        resultat.append({
            "dato": dato,
            "maks_temp": til_tall(rad[3]),
            "middeltemp": til_tall(rad[4]),
            "nedbor": til_tall(rad[5]),
            "vind": til_tall(rad[6]),
            "sno": til_tall(rad[7]),
        })
    # Send alle gyldige datolinjer tilbake til programmet.
    return resultat


# Leser direkte fra hver CSV-fil, uten ZIP.
def les_alle_stasjoner():
    stasjoner = {}

    for navn, filnavn in FILER.items():
        try:
            # Åpne CSV-filen. Den bruker semikolon og norske desimaltall.
            with open(MAPPE / filnavn, encoding="utf-8-sig") as fil:
                stasjoner[navn] = les_rader(fil)
            print(f"Lest {navn}: {len(stasjoner[navn])} dager")
        except FileNotFoundError:
            print(f"Finner ikke {filnavn}. Sjekk filnavn og mappe.")

    return stasjoner

# OPPGAVE A: Lag månedlige verdier av daglige målinger.
def oppgave_a(data, navn):
    # Samle daglige målinger etter år og måned.
    # Her er nøkkelen (år, måned), for eksempel (2024, 1).
    maneder = {}
    for rad in data:
        # Hent dato og finn hvilket år og hvilken måned den hører til.
        dato = rad["dato"]
        nokkel = (dato.year, dato.month)
        if nokkel not in maneder:
            maneder[nokkel] = []
        # Legg hele dagsmålingen i listen for denne måneden.
        maneder[nokkel].append(rad)

    # Én liste for x-aksen og én for hver verdi vi skal plotte.
    datoer = []
    maks_sno = []
    total_nedbor = []
    maks_temp = []
    min_temp = []
    maks_vind = []

    # Gå gjennom månedene i kronologisk rekkefølge.
    for aar, maaned in sorted(maneder):
        # Hent alle daglige målinger i denne måneden.
        rader = maneder[(aar, maaned)]
        # Lag lister med gyldige tall (hopp over None).
        sno = [r["sno"] for r in rader if r["sno"] is not None]
        nedbor = [r["nedbor"] for r in rader if r["nedbor"] is not None]
        temp = [r["middeltemp"] for r in rader if r["middeltemp"] is not None]
        vind = [r["vind"] for r in rader if r["vind"] is not None]

     # Bruk månedens første dag som punkt på x-aksen.
        datoer.append(datetime(aar, maaned, 1))
        # Finn høyeste snødybde, eller None dersom data mangler.
        maks_sno.append(max(sno) if sno else None)
        # Nedbør krever MER enn 20 gyldige målinger.
        total_nedbor.append(sum(nedbor) if len(nedbor) > 20 else None)
        # Bruk dagsmiddeltemperatur: høyeste og laveste i måneden.
        maks_temp.append(max(temp) if temp else None)
        min_temp.append(min(temp) if temp else None)
        # Finn høyeste målte middelvind i måneden.
        maks_vind.append(max(vind) if vind else None)

    # Lag fire grafer, en under den andre.
    figur, akser = plt.subplots(4, 1, figsize=(11, 10), sharex=True)
    # Graf 1: snødybde.
    akser[0].plot(datoer, maks_sno)
    akser[0].set_ylabel("Snødybde (cm)")
    akser[0].set_title("Maks snødybde per måned")

      # Graf 2: total nedbør per måned.
    akser[1].plot(datoer, total_nedbor)
    akser[1].set_ylabel("Nedbør (mm)")
    akser[1].set_title("Total nedbør per måned")

    # Graf 3: høyeste og laveste dagsmiddeltemperatur.
    akser[2].plot(datoer, maks_temp, label="Maks")
    akser[2].plot(datoer, min_temp, label="Min")
    akser[2].set_ylabel("Temperatur (°C)")
    akser[2].set_title("Høyeste og laveste middeltemperatur")
    akser[2].legend()

    # Graf 4: maksimal middelvind.
    akser[3].plot(datoer, maks_vind)
    akser[3].set_ylabel("Vind (m/s)")
    akser[3].set_title("Maks middelvind per måned")
    akser[3].set_xlabel("År")

  # Legg rutenett på alle grafene så de blir enklere å lese.
    for akse in akser:
        akse.grid(True)
    figur.suptitle(f"Oppgave a – {navn}")
    plt.tight_layout()
    # Vis figuren på skjermen.
    plt.show()



# Start denne oppgaven når filen kjøres.
if __name__ == "__main__":
    stasjoner = les_alle_stasjoner()
    for navn, data in stasjoner.items():
        print("Lager månedsgrafer for", navn)
        oppgave_a(data, navn)

