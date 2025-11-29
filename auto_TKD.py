from datetime import datetime

OLAJ_INTERVAL_KM = 10000
VEZERLES_INTERVAL_KM = 100000
FEKEK_INTERVAL_KM = 75000
GUMI_INTERVAL_KM = 40000
GUMI_INTERVAL_YEARS = 8

class Auto_TKD:
    def __init__(self, marka, tipus, evjarat, rendszam, vetel_km, aktualis_km=0):
        self.marka = marka
        self.tipus = tipus
        self.evjarat = evjarat
        self.rendszam = rendszam
        self.vetel_km = int(vetel_km)
        self.aktualis_km = int(aktualis_km)
        self.utolso_olaj_km = None
        self.utolso_vezerles_km = None
        self.utolso_fek_km = None
        self.szervizek_TKD = []
        self.tankolasok_TKD = []
        self.gumi_teli_hasznalat_km = 0
        self.gumi_nyari_hasznalat_km = 0

    def update_km_TKD(self, uj_km):
        uj_km = int(uj_km)
        if uj_km > self.aktualis_km:
            self.aktualis_km = uj_km

    def add_service_TKD(self, tipus, km, koltseg):
        km = int(km)
        koltseg = float(koltseg)
        datum = datetime.now().date().isoformat()
        bejegyzes = {"tipus": tipus, "km": km, "datum": datum, "koltseg": koltseg}
        self.szervizek_TKD.append(bejegyzes)
        if tipus == "olaj":
            self.utolso_olaj_km = km
        elif tipus == "vezerles":
            self.utolso_vezerles_km = km
        elif tipus == "fekek":
            self.utolso_fek_km = km

    def add_fuel_TKD(self, megtett_km, liter, koltseg):
        megtett_km = int(megtett_km)
        liter = float(liter)
        koltseg = float(koltseg)
        datum = datetime.now().date().isoformat()
        bejegyzes = {"km": megtett_km, "liter": liter, "datum": datum, "koltseg": koltseg}
        self.tankolasok_TKD.append(bejegyzes)

    def add_gumi_hasznalat_TKD(self, evszak, km):
        km = int(km)
        if evszak == "teli":
            self.gumi_teli_hasznalat_km += km
        elif evszak == "nyari":
            self.gumi_nyari_hasznalat_km += km

    def gumi_hasznalat_TKD(self, evszak):
        if evszak == "teli":
            return self.gumi_teli_hasznalat_km
        if evszak == "nyari":
            return self.gumi_nyari_hasznalat_km
        return 0

    def gumi_elettartam_TKD(self, evszak):
        felhasznalt = self.gumi_hasznalat_TKD(evszak)
        return GUMI_INTERVAL_KM - felhasznalt

    def ossz_km_TKD(self):
        return max(0, self.aktualis_km - self.vetel_km)

    def atlag_fogyasztas_TKD(self):
        if not self.tankolasok_TKD:
            return None
        tav = sum(t["km"] for t in self.tankolasok_TKD)
        if tav <= 0:
            return None
        ossz_liter = sum(t["liter"] for t in self.tankolasok_TKD)
        return (ossz_liter / tav) * 100.0

    def km_hatravan_TKD(self, tipus):
        if tipus == "olaj":
            interval = OLAJ_INTERVAL_KM
            last = self.utolso_olaj_km
        elif tipus == "vezerles":
            interval = VEZERLES_INTERVAL_KM
            last = self.utolso_vezerles_km
        elif tipus == "fekek":
            interval = FEKEK_INTERVAL_KM
            last = self.utolso_fek_km
        else:
            return None
        if last is None:
            return None
        esedekes = last + interval
        return esedekes - self.aktualis_km

    def szerviz_koltseg_TKD(self):
        return sum(s["koltseg"] for s in self.szervizek_TKD)

    def uzemanyag_koltseg_TKD(self):
        return sum(t["koltseg"] for t in self.tankolasok_TKD)

    def koltseg_tipus_szerint_TKD(self, tipus):
        return sum(s["koltseg"] for s in self.szervizek_TKD if s["tipus"] == tipus)
