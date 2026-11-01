# DAT120 - Øving 10, oppgave c
# Sammenlign gjennomsnittstemperaturen per år for seks værstasjoner.

import csv
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

# Finn mappen som denne Python-filen ligger i.
mappe = Path(__file__).resolve().parent

# Navn på CSV-filene. Filene skal ligge i samme mappe som Python-filen.
filer = {
    "Oslo Blindern": "oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Røros": "roeros_1954_2025_med_makstemperatur.csv",
    "Tromsø": "tromsoe_1954_2025_med_makstemperatur.csv",
    "Værnes": "vaernes_1954_2025_med_makstemperatur.csv",
    "Venabu": "venabu_1954_2025_med_makstemperatur.csv",
    "Sinnes": "sinnes_2014_2025_med_makstemperatur.csv",
}


# DEL 1: Les dato og middeltemperatur fra en CSV-fil.
def les_vaerdata(filnavn):
    data = {}  # Dato -> temperatur. Gir bare én verdi per dag.

    with open(mappe / filnavn, encoding="utf-8-sig", newline="") as fil:
        leser = csv.reader(fil, delimiter=";")
        next(leser)  # Hopp over første rad med kolonnenavn.

        for rad in leser:
            if len(rad) < 5:
                continue  # Hopp over ufullstendige rader.

            dato_tekst = rad[2].strip()  # Dato ligger i kolonne 3.
            temp_tekst = rad[4].strip()  # Middeltemperatur ligger i kolonne 5.

            if temp_tekst == "" or temp_tekst == "-":
                continue  # Manglende temperatur skal ikke bli 0.

            try:
                dato = datetime.strptime(dato_tekst, "%d.%m.%Y")
                temperatur = float(temp_tekst.replace(",", "."))
            except ValueError:
                continue  # Hopp over ugyldige datoer og tall.

            data[dato] = temperatur  # Lagre dagens temperatur.

    return data


# DEL 2: Beregn gjennomsnittstemperaturen for hvert år.
def beregn_aarssnitt(data):
    temperaturer_per_aar = {}  # År -> liste med temperaturer.

    for dato, temperatur in data.items():
        aar = dato.year
        if aar not in temperaturer_per_aar:
            temperaturer_per_aar[aar] = []
        temperaturer_per_aar[aar].append(temperatur)

    aarstall = []  # Årene som har nok data.
    gjennomsnitt = []  # Gjennomsnittstemperaturen for disse årene.

    # Gå gjennom årene i sortert rekkefølge
    for aar in sorted(temperaturer_per_aar):

        # Hent temperaturene for dette året
        temperaturer = temperaturer_per_aar[aar]

        # Sjekk om året har minst 300 temperaturmålinger
        if len(temperaturer) >= 300:

            # Beregn gjennomsnittstemperaturen
            snitt = sum(temperaturer) / len(temperaturer)

            # Legg til årstall og gjennomsnitt
            aarstall.append(aar)
            gjennomsnitt.append(snitt)

    # Returner listene etter at alle årene er behandlet
    return aarstall, gjennomsnitt

# DEL 3: Lag én graf med en kurve for hver værstasjon.
def oppgave_c():
    plt.figure(figsize=(12, 6))

    for stasjon, filnavn in filer.items():
        try:
            data = les_vaerdata(filnavn)
        except FileNotFoundError:
            print(f"Finner ikke {filnavn}. Sjekk filnavn og mappe.")
            continue

        aarstall, gjennomsnitt = beregn_aarssnitt(data)
        print(f"{stasjon}: {len(aarstall)} år med minst 300 gyldige dager")

        # Tegn bare en kurve dersom stasjonen har nok data.
        if aarstall:
            plt.plot(aarstall, gjennomsnitt, label=stasjon)

    plt.title("Oppgave 10c - Årlig gjennomsnittstemperatur")
    plt.xlabel("År")
    plt.ylabel("Gjennomsnittstemperatur (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# DEL 4: Start programmet.
oppgave_c()
