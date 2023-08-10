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
