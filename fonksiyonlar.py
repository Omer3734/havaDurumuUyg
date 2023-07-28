import sys
import feedparser
import main

def sehirHarfReplace(sehirGirdi):
    sehir = sehirGirdi.replace("ç", "c")
    sehir = sehir.replace("ö", "o")
    sehir = sehir.replace("ü", "u")
    sehir = sehir.replace("ı", "i")
    sehir = sehir.replace("ğ", "g")
    sehir = sehir.replace("ş", "s")

    sehir = sehir.replace("Ç", "C")
    sehir = sehir.replace("Ö", "O")
    sehir = sehir.replace("Ü", "U")
    sehir = sehir.replace("İ", "I")
    sehir = sehir.replace("Ğ", "G")
    sehir = sehir.replace("Ş", "S")
    sehir = sehir.upper()
    return sehir


def havaSicaklikSorgu(i):
    print("checkpoint 1")
    postaKodu = 10000  # İki satır alttaki "feeder.parser()" fonksiyonu, posta kodu değerine bağlı olmaksızın doğru çalışıyor.
    sehir = sehirHarfReplace(i)
    print("checkpoint 2")
    parse = feedparser.parse(f"https://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&"
                             f"locCode=EUR|TR|{postaKodu}|{sehir}|")
    print("checkpoint 3")
    parse = parse["entries"][0]["summary"]
    parse = parse.split()
    print("checkpoint 4")
    print(sehir)

    if sehir != "hatay".upper():
        sehirIsmi = parse[2]
        sehirSicaklik = parse[4]
        dereceCelcius = parse[5]
    else:
        sehirIsmi = parse[2]
        sehirSicaklik = parse[5]
        dereceCelcius = parse[6]

    print(f"{sehirIsmi} {sehirSicaklik} {dereceCelcius}")
    return f"{sehirIsmi} {sehirSicaklik} {dereceCelcius}"

