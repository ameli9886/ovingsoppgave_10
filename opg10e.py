
#Har definert skiføre som minst 20cm snø
#Definert skisesong som november til april.

import csv
import matplotlib.pyplot as plt

def les_data(filnavn):
    skidager = {}      #teller dager med minst 20cm snø for hver skisesong
    maalte_dager = {}  # teller dager med gyldig snømåling også når snødybden er under 20cm

    with open(filnavn,"r", encoding = "utf-8-sig") as fil:
        leser = csv.reader(fil,delimiter = ";")
        next(leser)

        for rad in leser: 
            dato = rad[2]
            deler = dato.split(".")          # deler teksten hver gang en finner "."
            if len(deler) == 3:
                maaned = int(deler[1])
                aar = int(deler[2])
            else: 
                continue

            sno = rad[7]

            if sno != "" and sno != "-":
                snodybde = float(sno.replace(",","."))
                if maaned >= 11:
                    sesong = aar
                elif maaned <= 4:
                    sesong = aar - 1
                else:
                    continue

                if sesong not in maalte_dager:
                    maalte_dager[sesong] = 0
                maalte_dager[sesong] += 1  #Om en finner måling med eks 5cm snø økes målte dager men ikke skidager.

                if snodybde >= 20:
                    if sesong not in skidager:    # Ser om sesongen ikke finnes i ordboken
                        skidager[sesong] = 0
                    skidager[sesong] += 1

    aarstall = []
    antall_skidager = []

    for sesong in maalte_dager:
        if maalte_dager[sesong] >= 91:
            aarstall.append(sesong)                        #append legger til element bakest i listen
            antall_skidager.append(skidager.get(sesong,0))  #Henter skridager for den sesongen, om ikke brukes 0
    return aarstall, antall_skidager

filer = [
    "Innlevering/oslo_blindern_1954_2025_med_makstemperatur.csv",
    "Innlevering/roeros_1954_2025_med_makstemperatur.csv",
    "Innlevering/tromsoe_1954_2025_med_makstemperatur.csv",
    "Innlevering/vaernes_1954_2025_med_makstemperatur.csv",
    "Innlevering/venabu_1954_2025_med_makstemperatur.csv"
]

plt.figure(figsize=(14, 7)) # 14=bredden, 7=høyde

for filnavn in filer:       # Går gjennom de fem filene en om gangen
    aarstall, antall_skidager = les_data(filnavn)
    alle_aar = list(range(min(aarstall), max(aarstall) + 1))  # lager liste med alle årstallene fra første til siste sesong
    verdier = dict(zip(aarstall, antall_skidager)) #dict(zip) kobler hvert årstall til antall skidager
    skidager_med_hull= [verdier.get(aar) for aar in alle_aar] #henter skidager for året, om året mangler-None
    plt.plot(alle_aar, skidager_med_hull) #tegner kurven, stopper linjen der verdien er None

plt.xlabel("Skisesong (startår)")
plt.ylabel("Antall skidager")
plt.title("Antall skidager per skisesong")
plt.legend(["Oslo Blindern", "Røros", "Tromsø", "Værnes", "Venabu"],
           loc= "upper left", bbox_to_anchor=(1,1)) #flytter navneforklaring til høyre for grafen
plt.tight_layout() #hjelper me å få på plass alt

plt.grid(True)
plt.show()
    
