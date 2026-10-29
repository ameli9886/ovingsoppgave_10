
import csv
import matplotlib.pyplot as plt
from statistics import median 

def les_data ():
    vind_per_maaned = [[] for i in range(12)]

    with open("Innlevering/oslo_blindern_1954_2025_med_makstemperatur.csv", "r", encoding="utf-8-sig") as fil:
        leser = csv.reader(fil,delimiter = ";")
        next(leser)                               # Hopper over overskriftene
    
        for rad in leser:
            dato = rad[2]
            vind = rad[6]
            if len(dato.split(".")) == 3:            # Ser om datoen har tre deler
                maaned = int(dato.split(".")[1])     #[1] henter mnd, int gjør det om til heltall

                if vind != "" and vind != "-":
                    vindstyrke = float(vind.replace(",","."))
                    vind_per_maaned[maaned - 1].append(vindstyrke)
    return vind_per_maaned

vind_per_maaned = les_data()

minimun = []           # lager tom liste
medianverdier = []
maksimum = []

for i in range(12):
    vind = vind_per_maaned[i]

    if len(vind) > 0:
        minimun.append(min(vind))            #Finner minste tall
        medianverdier.append(median(vind))
        maksimum.append(max(vind))           #Finner størte tall

        print("Måned:", i +1)
        print("Minimum:", min(vind))
        print("Median:", median(vind))
        print("Maksimum:", max(vind))

#Graf 
maander = list(range(1,13))

plt.plot(maander, minimun, label = "Minimum")              #Tegner linjene
plt.plot(maander, medianverdier, label = "Median")
plt.plot(maander, maksimum, label = "Maksimum") 

plt.xlabel("Måned")
plt.ylabel("Vindstyrke (m/s)")
plt.title("Vindstyrke per måned - Oslo Blindern")
plt.xticks(maander)
plt.legend()                                              # Viser hvilke linje som er min, median og max
plt.grid()                                                # Legger til rutenett
plt.show()

