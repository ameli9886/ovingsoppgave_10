import csv
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime

def les_data():
    with open("Innlevering/sinnes_2014_2025_med_makstemperatur.csv", "r", encoding="utf-8-sig") as fil:
            leser = csv.reader(fil,delimiter = ";") #csv.reader leser filen rad for rad, delimeter = ";" skiller kolonnene fra hverandre
            next(leser) # hopp over første rad, er ikke værdata så trenger den ikke.
        
            data = list(leser)
            return data 


# OPPGAVE D
def plotting(data, aar):
    weather_dict = {}
    
    for parts in data:
        if len(parts) < 8 or not parts[2].strip():
          continue

        date_str = parts[2].strip()
        try:
          date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
          continue  

    # Remove '-' or null values, and format decimal numbers:
        def parse_float(val):
           val = val.strip()
           if val == "-" or val == "":
              return None
           return float(val.replace(",", "."))

        max_temp = parse_float(parts[3])
        mean_temp = parse_float(parts[4])
        precip = parse_float(parts[5])
        wind = parse_float(parts[6])
        snow = parse_float(parts[7])

    # Use a dictionary for storage, key: date_obj
        weather_dict[date_obj] = {
            "max_temp": max_temp,
            "mean_temp": mean_temp,
            "precip": precip,
            "wind": wind,
            "snow": snow,
        }

# sort the dates
    sorted_dates = sorted(weather_dict.keys())  

# creat new list
    dates = []
    max_temps = []
    mean_temps = []
    precips = []
    winds = []
    snows = []

    for d in sorted_dates:
       dates.append(d)

       max_temps.append(weather_dict[d]["max_temp"])
       mean_temps.append(weather_dict[d]["mean_temp"])
       precips.append(weather_dict[d]["precip"])
       winds.append(weather_dict[d]["wind"])
       snows.append(weather_dict[d]["snow"])
    if not dates:
       print("No valid weather data found")
       return
    
    print(f"Data reading and time-based sorting completed. There are {len(dates)} days of valid data（time range from："
    f'{dates[0].strftime("%Y-%m-%d")} to {dates[-1].strftime("%Y-%m-%d")}）。\n')

# Drawing functions:
    def plot_weather_by_year(target_year):
       year_dates = []
       year_snow = []
       year_precip = []
       year_mean_temp = []
       year_wind = []
       
       for d, s, p, mt, w in zip(dates, snows, precips, mean_temps, winds):
            if d.year == target_year:
                year_dates.append(d)
                year_snow.append(s if s is not None else 0)
                year_precip.append(p if p is not None else 0)
                year_mean_temp.append(mt if mt is not None else 0)
                year_wind.append(w if w is not None else 0)

       if not year_dates:
            print(f"The data of year {target_year} not exist.")
            return

  # plotting
       fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

  # 1 snødybde
       axes[0].plot(year_dates, year_snow, color="blue", label="Snødybde (cm)")
       axes[0].set_ylabel("Snødybde (cm)")
       axes[0].legend(loc="upper right")
       axes[0].grid(True)

  # 2 nedbør
       axes[1].bar(year_dates, year_precip, color="cyan", width=1, label="Nedbør (mm)")
       axes[1].set_ylabel("Nedbør (mm)")
       axes[1].legend(loc="upper right")
       axes[1].grid(True)

  # 3 middeltemperatur
       axes[2].plot(year_dates, year_mean_temp, color="red", label="Middeltemperatur (°C)")
       axes[2].set_ylabel("Temperatur (°C)")
       axes[2].legend(loc="upper right")
       axes[2].grid(True)

  # 4 høyeste middelvind hver dag
       axes[3].plot(year_dates, year_wind, color="green", label="Middelvind (m/s)")
       axes[3].set_ylabel("Vind (m/s)")
       axes[3].legend(loc="upper right")
       axes[3].grid(True)

  # Set the major ticks to the first day of each month.
       axes[3].xaxis.set_major_locator(mdates.MonthLocator())
  # Format the tick labels to display English month abbreviations (e.g., Jan, Feb...).
       axes[3].xaxis.set_major_formatter(mdates.DateFormatter("%b"))

       axes[3].set_xlabel(f"{target_year} ", fontsize=12)
       plt.suptitle(f"Sinnes Værstasjon - {target_year} Væroversikt", fontsize=14, fontweight="bold",)
       plt.tight_layout()
       plt.show()
    plot_weather_by_year(int(aar))



# OPPGAVE E
def skifore(data, aar):
    aar = int(aar)
    skifore_dager = 0

    for rad in data:
        if not rad[2] or rad[2].strip() == "":      #sjekk dato ikke er tomt
            continue

        datoer = datetime.strptime(rad[2], "%d.%m.%Y")    #kolonne 2=dat0
        
        if rad[7] == "-" or rad[7] == "":       #er registrert - eller ingenting på de dagene uten snø
            snodybde_verdier = 0.0
        else:
            snodybde_verdier = float(rad[7])                  #kolonne 7=snødybde

        #fra oppg. sesong er fra 1. nov til 31. mai
        start_sesong = datetime(aar -1, 11, 1)        #-1 pga forrige år
        slutt_sesong = datetime(aar, 5, 31)

        if start_sesong <= datoer <= slutt_sesong:
            if snodybde_verdier >= 20:             #er skiføre når minst 20cm
                skifore_dager += 1                  #legger til antall når over 20

    print(f"Antall dager med skiføre i sensongen {aar -1}/{aar}: {skifore_dager} dager") 


# OPPGAVE F
def plantevekst(data, aar):
    aar = int(aar)
    total_vekst = 0.0
 
    for rad in data:
        if not rad[2] or rad[2].strip() == "":
            continue

        try:
            datoer = datetime.strptime(rad[2], "%d.%m.%y")
        except ValueError:
            continue

        if rad[4] == "-" or rad[4] == "":   #hvis disse i kolonne, temp=0
            temperatur = 0.0
        else:
            temperatur = float(rad[4].replace(",","."))

        if datoer == aar and temperatur > 5:
            total_vekst += (temperatur - 5)

    print(f"Total plantevekst i {aar}: {total_vekst:.1f} enheter")
  


# OPPPGAVE G
def lengste_periode_uten_nedbor(data):
    antall = 0             # Antall uten nedbør
    lengste = 0            # Lengste periode uten nedbør
    lengste_start = ""     # Vet ikke startdato enda
    start = ""             # Vet ikke starten på perioden enda
    lengste_slutt = ""     # Vet ikke slutten på perioden enda

    for rad in data:
        dato = rad[2]
        nedbor = rad[5]
        
        if nedbor == "" or nedbor == "-":
            antall = 0   
            continue                        #Hopper over tom rad or rad med "-"

        nedbor = nedbor.replace(",", ".")  #Bytter , med .
        nedbor = float(nedbor) # Gjør det om til tall som kan ha desimaler

        if nedbor == 0:                  #Vil finne dager uten nedbør.
            antall += 1                  #Legges til i antall om det registreres dager uten nedbør

            if antall == 1:              #1 dag er startdato på perioden uten nedbør
                start = dato

            if antall > lengste:         # Finner lengste periode og legger til i antall
                lengste = antall
                lengste_start = start    #Husker startdatoen til den lengste perioden
                lengste_slutt = dato     #Husker sluttdatoen til den lengste perioden
        else:
            antall = 0                   # Antall blir null igjen dersom det registreres dag med nedbør
    print("Lengste perioden uten nedbør:", lengste, "dager")
    print( "Startdato:", lengste_start)
    print("Sluttdato:", lengste_slutt)
 
# OPPGAVE H 
def antall_varme_dager(data, aar):
    sommerdager = 0     # starter tellingen av sommerdager på 0
    hoysommerdager = 0  # starter tellingen av høysommerdager på 0
    tropedager = 0      # starter tellingen av tropedager på 0

# går gjennom en linje om gangen i filen
    for rad in data:
        dato = rad[2]                     # henter datoen fra kolonne 3

        if rad [3]== "-" or rad[3] =="":               # hopper over raden hvis temperaturen mangler og tomme temperaturfelt
            continue

        temperatur = float(rad[3].replace(",", "."))   # henter maksimaltemperatur fra kolonne 4. Replace bytter komma til punktum slik at float kan lese tallet.

        if dato.endswith(aar):              # sjekker om datoen tilhører året som ble skrevet inn
            if temperatur > 20:             # hvis temperaturen er over 20 garder, teller vi en sommerdag
                sommerdager += 1

            if temperatur > 25:             # hvis temperaturen er over 25 grader, teller vi en høysommerdag
                hoysommerdager += 1

            if temperatur > 30:             # hvis temperaturen er over 30 grader, teller vi en tropedag
                tropedager += 1

    print("Sommerdager:", sommerdager)          # skriver ut hvor mange sommerdager det var
    print("Høysommerdager:", hoysommerdager)    # skriver ut hvor mange høysommerdager det var
    print("Tropedager:", tropedager)            # skriver ut hvor mange tropedager det var

# KJØRER DE ULIKE OPPGAVENE  

data = les_data()
lengste_periode_uten_nedbor(data)    #kjør opg g
aar = input("Skriv inn år")          # spør bruker om år en gang
antall_varme_dager(data, aar)        # kjører opg h
plotting(data, aar)                  #kjører opg d
skifore(data, aar)                   # kjører opg e
plantevekst(data, aar)               # kjører opg f