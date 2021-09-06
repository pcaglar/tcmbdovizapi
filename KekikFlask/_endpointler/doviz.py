import xml.etree.ElementTree as ET
from urllib.request import urlopen
import re
from datetime import date
import datetime

class DovizKur():

    def __init__(self):
        pass

    def veri_al(self, zaman="Bugun"):
        try:
            if zaman == "Bugun":
                self.url = "http://www.tcmb.gov.tr/kurlar/today.xml"
            else:
                self.url = zaman
            tree = ET.parse(urlopen(self.url))
            root = tree.getroot()
            self.son = {}
            self.Kur_Liste = []
            i = 0
            for kurlar in root.findall("Currency"):
                Kod = kurlar.get('Kod')
                Unit = kurlar.find('Unit').text
                isim = kurlar.find('Isim').text
                CurrencyName = kurlar.find('CurrencyName').text
                ForexBuying = kurlar.find('ForexBuying').text
                ForexSelling = kurlar.find('ForexSelling').text
                BanknoteBuying = kurlar.find('BanknoteBuying').text
                BanknoteSelling = kurlar.find('BanknoteSelling').text
                CrossRateUSD = kurlar.find('CrossRateUSD').text

                self.Kur_Liste.append(Kod)
                self.son[Kod] = {
                    "Kod": Kod,
                    "isim": isim,
                    "CurrencyName": CurrencyName,
                    "Unit": Unit,
                    "ForexBuying": ForexBuying,
                    "ForexSelling": ForexSelling,
                    "BanknoteBuying": BanknoteBuying,
                    "BanknoteSelling": BanknoteSelling,
                    "CrossRateUSD": CrossRateUSD
                    }
            return self.son
        except:
            return "HATA"

    def DegerSor(self, *sor):
        self.veri_al()
        if not(any(sor)):
            return self.son
        else:
            return self.son.get(sor[0]).get(sor[1])

    def Arsiv(self, Gun, Ay, Yil, *sor):
        a = self.veri_al(self.__Url_Yap(Gun, Ay, Yil))
        if not(any(sor)):
            if a == "HATA":
                return {"Hata": "TATIL GUNU"}
            return self.son
        else:
            if a == "HATA":
                return "Tatil Gunu"
            else:
                return self.son.get(sor[0]).get(sor[1])

    def Arsiv_tarih(self, Tarih="", *sor):
        yil = re.findall(r"\d\d\d\d(\d{4})", Tarih)[0]
        ay = re.findall(r"(\d{2})", Tarih)[1]
        gun = re.findall(r"(\d{2})", Tarih)[0]
        a = self.veri_al(self.__Url_Yap(gun, ay, yil))
        if not(any(sor)):
            if a == "HATA":
                return {"Hata": "TATIL GUNU"}
            return self.son
        else:
            if a == "HATA":
                return "Tatil Gunu"
            else:
                return self.son.get(sor[0]).get(sor[1])

    def __Url_Yap(self, gun, ay, yil):
        bugun_tarih = datetime.datetime.now()
        bugun_gun = bugun_tarih.strftime("%d")
        bugun_ay = bugun_tarih.strftime("%m")
        bugun_yil = bugun_tarih.strftime("%Y")
        if len(str(gun)) == 1:
            gun = "0"+str(gun)
        if len(str(ay)) == 1:
            ay = "0"+str(ay)
        if ay == bugun_ay and gun == bugun_gun:
            self.url = "https://www.tcmb.gov.tr/kurlar/today.xml"
        else:
            self.url = ("http://www.tcmb.gov.tr/kurlar/"+str(yil) +
                        str(ay)+"/"+str(gun)+str(ay)+str(yil)+".xml")
        return self.url
    
    def hesapla(self,*sor):
        self.veri_al(zaman="Bugun")
        deger=self.son.get(sor[0]).get(sor[1])
        miktar=float(sor[2].replace(',','.'))
        sonuc=str(float(deger)*(miktar))
        return sonuc


    """def hesapla(self,*sor):
        self.veri_al(zaman="Bugun")
        deger=self.son.get("USD").get(sor[0])
        
        miktar=float(sor[1].replace(',','.'))
        sonuc=str(float(deger)*(miktar))

        return sonuc"""
    
    """def hesapla(self,*sor):
        self.veri_al()
        deger=self.son.get(sor[0]).get(sor[1])
        miktar=float(sor[2].replace(',','.'))
        sonuc=str(float(deger)*(miktar))

        return sonuc"""
    
  