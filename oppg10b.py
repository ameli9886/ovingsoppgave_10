
import csv
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt


# OPPGAVE 10B - SOMMERDAGER

# Finn mappen der Python-filen ligger
mappe = Path(__file__).resolve().parent

# CSV-filen til Oslo Blindern
filnavn = mappe / "oslo_blindern_1954_2025_med_makstemperatur.csv"


# DEL 1: Les inn værdata
def les_vaerdata():

    # Lag en tom liste for værmålingene
    data = []

    # Åpne CSV-filen
    with open(filnavn, encoding="utf-8-sig") as fil:

        # Del opp hver rad ved semikolon
        leser = csv.reader(fil, delimiter=";")

        # Hopp over overskriften
        next(leser)

        # Gå gjennom alle radene i filen
        for rad in leser:

            # Kontroller at raden har nok kolonner
            if len(rad) < 4:
                continue

            # Hent dato og maksimaltemperatur
            dato_tekst = rad[2].strip()
            temp_tekst = rad[3].strip()

            # Hopp over manglende målinger
            if temp_tekst == "-" or temp_tekst == "":
                continue

            try:
                # Gjør dato om til datetime
                dato = datetime.strptime(dato_tekst, "%d.%m.%Y")

                # Gjør temperatur om til desimaltall
                temperatur = float(temp_tekst.replace(",", "."))

            except ValueError:
                continue

            # Lagre dato og temperatur
            data.append([dato, temperatur])

    return data


# DEL 2: Tell sommerdager for hvert år
def oppgave_b(data):

    # Lag en tom ordbok for antall dager
    antall_dager = {}

    # Gå gjennom alle målingene
    for dato, temperatur in data:

        # Finn årstallet
        aar = dato.year

        # Lag tellere for hvert nytt år
        if aar not in antall_dager:
            antall_dager[aar] = [0, 0, 0]

        # Tell sommerdager (over 20 grader)
        if temperatur > 20:
            antall_dager[aar][0] += 1

        # Tell høysommerdager (over 25 grader)
        if temperatur > 25:
            antall_dager[aar][1] += 1

        # Tell tropedager (over 30 grader)
        if temperatur > 30:
            antall_dager[aar][2] += 1

    # DEL 3: Lag lister til grafen

    # Sorter årstallene
    aarstall = sorted(antall_dager)

    # Lag tomme lister
    sommerdager = []
    hoysommerdager = []
    tropedager = []

    # Hent antall dager for hvert år
    for aar in aarstall:

        sommerdager.append(antall_dager[aar][0])
        hoysommerdager.append(antall_dager[aar][1])
        tropedager.append(antall_dager[aar][2])

    # DEL 4: Lag grafen
    plt.figure(figsize=(12, 6))

    # Plott sommerdager
    plt.plot(aarstall, sommerdager,
             color="blue", label="Sommerdager")

    # Plott høysommerdager
    plt.plot(aarstall, hoysommerdager,
             color="orange", label="Høysommerdager")

    # Plott tropedager
    plt.plot(aarstall, tropedager,
             color="red", label="Tropedager")

    # Tittel og akser
    plt.title("Oppgave 10b - Oslo Blindern")
    plt.xlabel("År")
    plt.ylabel("Antall dager")

    # Vis forklaring og rutenett
    plt.legend()
    plt.grid(True)

    # Vis grafen
    plt.tight_layout()
    plt.show()


# DEL 5: Kjør programmet

# Les inn værdata fra CSV-filen
data = les_vaerdata()

# Skriv ut hvor mange dager som ble lest
print("Antall dager lest inn:", len(data))

# Kjør oppgave b
oppgave_b(data)
