import datetime
import sqlite3
import sys
import threading
import time

from textblob import TextBlob
import feedparser
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QComboBox
from textblob import TextBlob

import fonksiyonlar
import trSehirler

an = datetime.datetime.now()

def havaSicaklikSorgu(i):
    global sehirSicaklik
    global sehir
    global sehirSicaklikDerece
    global status
    global statusEn
    status = ""
    postaKodu = 10000  # İki satır alttaki "feeder.parser()" fonksiyonu, posta kodu değerine bağlı olmaksızın doğru çalışıyor.
    sehir = fonksiyonlar.sehirHarfReplace(i)
    parse = feedparser.parse(f"https://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&"
                             f"locCode=EUR|TR|{postaKodu}|{sehir}|")
    parse = parse["entries"][0]["summary"]
    parse = parse.split()
    sehir = sehir.lower()
    print(sehir)
    print(parse[0])
    if sehir.upper() != "hatay".upper():
        print("1")
        sehirSicaklik = parse[4]
        dereceCelcius = parse[5]
        if parse[8] == '<img':
            status = parse[7]
        else:
            status = str(parse[7] + " " + parse[8])
    else:
        print("2")
        sehirSicaklik = parse[5]
        dereceCelcius = parse[6]
        print(f"{i.capitalize()} : {sehirSicaklik} {dereceCelcius}\n{status}")
        if parse[9] == '<img':
            status = parse[8]
        else:
            status = str(parse[8] + " " + parse[9])

    print(parse)


    print("--")
    print(status)
    statusEn = status
    text = TextBlob(status)
    status = text.translate(from_lang="en", to="tr").title()
    print(status.lower())
    if status.lower() == "temizlemek":
        status = "Açık, Temiz Hava"

    sehirSicaklikDerece = f"{sehirSicaklik} {dereceCelcius}"
    return f"{i.capitalize()} : {sehirSicaklik} {dereceCelcius}\n{status}"


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
        self.setWindowTitle('Hava Durumu Öğren')
        self.setMinimumSize(450, 450)
        self.setMaximumSize(450, 450)

    def ekOzellikEkle(self):

        font = QtGui.QFont()

        self.label_img = QLabel(self)
        self.label_img.setGeometry(QtCore.QRect(1, 1, 448, 448))
        self.label_img.setScaledContents(True)
        self.label_img.setStyleSheet(
            f"background-image: url(:../../PycharmProjects/havaDurumuUyg/images/weatherConditions/weather"
            f".jpg);")

        self.label_img.setPixmap(
            QtGui.QPixmap(
                f"../../PycharmProjects/havaDurumuUyg/images/weatherConditions/weather"
                f".jpg"))

        self.label_bg = QLabel(self)
        self.label_bg.setGeometry(QtCore.QRect(1, 1, 448, 448))
        self.label_bg.setScaledContents(True)


        self.acilirListeBolge = QComboBox(self)
        self.acilirListeBolge.addItems(trSehirler.bolgeler)
        self.acilirListeBolge.setGeometry(10, 10, 200, 25)

        self.acilirListeSehirler = QComboBox(self)
        self.acilirListeSehirler.addItems(trSehirler.tumSehirler)
        self.acilirListeSehirler.setGeometry(220, 10, 200, 25)

        self.butonIceAktar = QPushButton("Şehirleri İçe Aktar", self)
        self.butonIceAktar.setGeometry(10, 50, 110, 30)

        self.butonYazdir = QPushButton("Hava Sıcaklığını Göster", self)
        self.butonYazdir.setGeometry(150, 380, 130, 30)

        self.butonKaydet = QPushButton("Veritabanına Kaydet", self)
        self.butonKaydet.setGeometry(300, 380, 130, 30)


        self.label = QLabel("", self)
        self.label.setGeometry(10, 245, 350, 100)
        font.setPointSize(16)
        self.label.setFont(font)

        self.label_saved = QLabel("", self)
        self.label_saved.setGeometry(10, 285, 350, 100)
        font.setPointSize(14)
        self.label_saved.setFont(font)
        font.setBold(True)


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


        #   Aşağıda yorum satırı halinde duran iki kod bloğu,
        #   ekrana hava durumu bilgisi istenen şehre ait bir fotoğraf bastırır.

        #self.label_img.setStyleSheet(
        #   f"background-image: url(:../../PycharmProjects/havaDurumuUyg/images/cities/{self.hangiBolge()[self.acilirListeSehirler.currentIndex()].lower()}"
        #  f".jpg);")

        #self.label_img.setPixmap(
        #    QtGui.QPixmap(
        #        f"../../PycharmProjects/havaDurumuUyg/images/cities/{self.hangiBolge()[self.acilirListeSehirler.currentIndex()].lower()}"
        #        f".jpg"))

        self.label_saved.setText("")

        if self.acilirListeSehirler.currentIndex() == -1:
            self.label.setText("Lütfen Dilediğiniz Bölgeden Bir Şehir Seçiniz.")
        else:

            self.label.setText("Yükleniyor...")
            self.label.setText(havaSicaklikSorgu(self.hangiBolge()[self.acilirListeSehirler.currentIndex()]))

        time.sleep(0.5)
        self.label_bg.setStyleSheet(
            f"background-image: url(:../../PycharmProjects/havaDurumuUyg/images/weatherConditions/{statusEn.lower()}"
            f".jpg);")

        self.label_bg.setPixmap(
            QtGui.QPixmap(
                f"../../PycharmProjects/havaDurumuUyg/images/weatherConditions/{statusEn.lower()}"
                f".jpg"))

    def butonaTiklandi(self):

        thread = threading.Thread(target=self.tiklandiYazdir)
        thread.start()

    def kaydet(self):
        if self.label.text() != "":
            database_connect = sqlite3.connect("havaDurumu.db")
            imlec = database_connect.cursor()
            imlec.execute(
                """CREATE TABLE IF NOT EXISTS havaDurumuInfo
                (tarih TEXT, saat TEXT, sicaklilk INTEGER , sehir TEXT)""")
            min = str(an.minute)
            if an.minute < 10:
                min = f"{0}{min}"

            tarih = f"{an.day}/{an.month}/{an.year}"
            saat = f"{an.hour}:{min}"

            imlec.execute(f"""INSERT INTO havaDurumuInfo 
                    VALUES(?, ?, ?, ?) """, (tarih, saat, sehirSicaklikDerece, self.hangiBolge()[self.acilirListeSehirler.currentIndex()]))

            database_connect.commit()
            database_connect.close()
            self.label_saved.setText("<font color='#068000'>Kaydedildi.</font>")
        else:
            self.label.setText("Lütfen Önce İstediğiniz Şehrin Hava Durumunu Ekrana Yazdırın.")

    def tiklandiIceAktar(self):
        self.acilirListeSehirler.clear()
        self.acilirListeSehirler.addItems(self.hangiBolge())

app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())
