#a)
maaleenheter = {
    "centimeter": 0.01,
    "tomme": 0.0254,
    "fot": 0.3048,
    "yard": 0.9144,
    "meter": 1,
    "kilometer": 1000,
    "miles": 1609,
    "nautiske_mil": 1852,
    "mil": 10000}
#b)
Tall = float(input("Oppgi et tall:"))
fra_enhet = input("Fra hvilke måleenhet?:")
til_enhet = input("Til hvilke måleenhet?")

resultat = Tall * maaleenheter[fra_enhet]/maaleenheter[til_enhet]
print(resultat) 
