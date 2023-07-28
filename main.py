import sys
import feedparser
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QComboBox
import threading
import datetime
from datetime import date
import trSehirler
import sqlite3

an = datetime.datetime.now()

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
    global sehirSicaklik
    global sehir
    global sehirSicaklikDerece
    postaKodu = 10000  # İki satır alttaki "feeder.parser()" fonksiyonu, posta kodu değerine bağlı olmaksızın doğru çalışıyor.
    sehir = sehirHarfReplace(i)
    parse = feedparser.parse(f"https://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&"
                             f"locCode=EUR|TR|{postaKodu}|{sehir}|")
    parse = parse["entries"][0]["summary"]
    parse = parse.split()

    if sehir != "hatay".upper():
        sehirSicaklik = parse[4]
        dereceCelcius = parse[5]
    else:
        sehirSicaklik = parse[5]
        dereceCelcius = parse[6]

    sehirSicaklikDerece = f"{sehirSicaklik} {dereceCelcius}"
    return f"{i.capitalize()} : {sehirSicaklik} {dereceCelcius}"


class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        self.ozellikEkle()
        self.ekOzellikEkle()
        self.butonYazdir.clicked.connect(self.butonaTiklandi)
        self.butonIceAktar.clicked.connect(self.tiklandiIceAktar)
        self.butonKaydet.clicked.connect(self.kaydet)

    def ozellikEkle(self):
        self.resize(500, 500)
        self.move(700, 100)
        self.setWindowTitle('Basit Pencere')
        self.setMinimumSize(500, 500)
        self.setMaximumSize(500, 500)

    def ekOzellikEkle(self):
        self.acilirListeBolge = QComboBox(self)
        self.acilirListeBolge.addItems(trSehirler.bolgeler)
        self.acilirListeBolge.setGeometry(10, 10, 200, 25)

        self.acilirListeSehirler = QComboBox(self)
        self.acilirListeSehirler.addItems(trSehirler.tumSehirler)
        self.acilirListeSehirler.setGeometry(220, 10, 200, 25)

        self.butonIceAktar = QPushButton("Şehirleri İçe Aktar", self)
        self.butonIceAktar.setGeometry(10, 50, 110, 30)

        self.butonYazdir = QPushButton("Yazdır", self)
        self.butonYazdir.setGeometry(250, 250, 100, 40)

        self.butonKaydet = QPushButton("Kaydet", self)
        self.butonKaydet.setGeometry(250, 300, 100, 50)

        self.label = QLabel("", self)
        self.label.setGeometry(10, 400, 350, 100)

    def hangiBolge(self):
        if self.acilirListeBolge.currentIndex() == 0:
            return trSehirler.tumSehirler
        elif self.acilirListeBolge.currentIndex() == 1:
            return trSehirler.marmaraSehirleri
        elif self.acilirListeBolge.currentIndex() == 2:
            return trSehirler.karadenizSehirleri
        elif self.acilirListeBolge.currentIndex() == 3:
            return trSehirler.egeSehirleri
        elif self.acilirListeBolge.currentIndex() == 4:
            return trSehirler.akdenizSehirleri
        elif self.acilirListeBolge.currentIndex() == 5:
            return trSehirler.icAnadoluSehirleri
        elif self.acilirListeBolge.currentIndex() == 6:
            return trSehirler.doguAnadoluSehirleri
        else:
            return trSehirler.guneydoguAnadoluSehirleri

    def tiklandiYazdir(self):

        if self.acilirListeSehirler.currentIndex() == -1:
            self.label.setText("Lütfen Dilediğiniz Bölgeden Bir Şehir Seçiniz.")
        else:
            self.label.setText("Yükleniyor...")
            self.label.setText(havaSicaklikSorgu(self.hangiBolge()[self.acilirListeSehirler.currentIndex()]))

    def butonaTiklandi(self):
        thread = threading.Thread(target=self.tiklandiYazdir)
        thread.start()

    def kaydet(self):
        database_connect = sqlite3.connect("havaDurumu.db")
        imlec = database_connect.cursor()
        imlec.execute(
            """CREATE TABLE IF NOT EXISTS havaDurumuInfo
            (tarih TEXT, saat TEXT, sicaklilk INTEGER , sehir TEXT)""")
        print(date.today())
        print("checkpoint 1")
        min = an.minute
        if min < 10:
            min = str(0,min)
        print(min)
        tarih = f"{an.day}/{an.month}/{an.year}"
        saat = f"{an.hour}:{an.minute}"
        print("checkpoint 2")
        imlec.execute(f"""INSERT INTO havaDurumuInfo 
        VALUES(?, ?, ?, ?) """,(tarih, saat, sehirSicaklikDerece, sehir))
        print("checkpoint 3")
        database_connect.commit()
        database_connect.close()

    def tiklandiIceAktar(self):
        self.acilirListeSehirler.clear()
        self.acilirListeSehirler.addItems(self.hangiBolge())

app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())
