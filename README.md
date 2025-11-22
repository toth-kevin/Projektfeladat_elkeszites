# RoadCare TKD – Autós költségkövető alkalmazás

## Hallgatói adatok

- Hallgató neve: **Tóth Kevin Dorián**
- Neptun-kód: **MAX-EBH**
- Tárgy: **Skript nyelvek – Python projektfeladat**
- Projekt neve: **RoadCare TKD – Autó szerviz és költségkövető**

---

## A program rövid leírása

A program egy **autós költségkövető alkalmazás**, amely azoknak készült, akik szeretnék nyomon követni:

- az autójuk **futásteljesítményét**,
- a használat közben felmerülő **szervizköltségeket**,
- az **üzemanyag-fogyasztást** és üzemanyagköltséget,
- valamint a különböző szervizek **esedékességét** (olajcsere, vezérlés, fékek),
- a **téli és nyári gumi** használatából adódó kopást (km alapján).

A felhasználó:

- megadja az autó alapadatait (márka, típus, évjárat, rendszám, vételkori km, aktuális km),
- ezután egy grafikus felületen:
  - frissítheti a km-óra állást,
  - rögzíthet **szervizeket** (olaj, vezérlés, fékek, gumi, egyéb),
  - rögzíthet **tankolásokat** (megtett km az előző tankolás óta, liter, Ft),
  - rögzítheti a **gumi használatát** külön a téli és nyári szettre,
  - lementheti a pillanatnyi összefoglalót egy `roadcare_TKD_jelentes.txt` fájlba.

A program kiszámolja:

- az autóval a vásárlás óta megtett km-t,
- a szervizköltségek összegét,
- az üzemanyag-költés összegét,
- az **átlagfogyasztást** (l/100 km),
- a **tankolások átlagos mennyiségét** (liter/tankolás),
- a **tankolások átlagos költségét** (Ft/tankolás),
- az egyes szervizekhez hátralévő km-t, vagy ha már túl van lépve az intervallumon, figyelmeztet:
  - „Kérjük, ellenőrizze, csere ajánlott!”
- a téli és nyári gumi esetén:
  - az adott gumin megtett km-t,
  - a becsült hátralévő km-t egy kb. **40 000 km-es** élettartamhoz viszonyítva.

---

## Fájlstruktúra

- `main.py` – a program belépési pontja, grafikus felület és eseménykezelés.
- `auto_TKD.py` – saját modul, benne az autó adatait és számításait kezelő osztály.
- `wheel.png` – opcionális ikon a főablakhoz.
- `roadcare_TKD_jelentes.txt` – futás közben generált jelentés fájl (mentés gombbal).

---

## Használt Python modulok

### Beépített / standard modulok

1. **tkinter**
   - A grafikus felület felépítésére és eseménykezelésre.
   - Használt elemek:
     - `tkinter.Tk` – főablak létrehozása
     - `tkinter.Frame`, `Label`, `Entry`, `Text`
     - `tkinter.Toplevel` – felugró ablakok (szerviz, tankolás, gumi használat)
     - `tkinter.Radiobutton` – téli/nyári gumi választás
     - `tkinter.StringVar`, `tkinter.IntVar` – kötött változók az űrlapmezőkhöz
   - Almodulok:
     - `from tkinter import ttk` – modern gombok: `ttk.Button`
     - `from tkinter import messagebox` – hibaüzenetek, visszajelzések
     - `from tkinter import simpledialog` – egyszerű, egymezős beviteli ablak (km-frissítésnél)

2. **statistics**
   - Tankolási statisztikákhoz.
   - Használt függvények:
     - `statistics.mean` – átlagolt érték számítása (liter és Ft tankolásonként)

3. **datetime**
   - A szerviz- és tankolás-bejegyzések dátumának rögzítéséhez.
   - Használt elem:
     - `datetime.now().date().isoformat()` – mai dátum ISO formátumban

### Saját modul

4. **`auto_TKD.py`**
   - Saját modul TKD monogrammal, benne az **Auto_TKD** osztály.
   - A modul importálása:
     - `from auto_TKD import Auto_TKD, GUMI_INTERVAL_KM`

---

## Saját osztályok

### 1. `Auto_TKD` (auto_TKD.py)

Az autó állapotát és a hozzá kapcsolódó számításokat végzi.

**Főbb adattagok:**

- `marka`, `tipus`, `evjarat`, `rendszam`
- `vetel_km` – km-óra állás vásárláskor
- `aktualis_km` – aktuális km-óra állás
- `utolso_olaj_km`, `utolso_vezerles_km`, `utolso_fek_km` – utolsó szerviz km-értéke
- `szervizek_TKD` – lista a szerviz-bejegyzésekről (tipus, km, dátum, költség)
- `tankolasok_TKD` – lista a tankolásokról (azóta megtett km, liter, dátum, költség)
- `gumi_teli_hasznalat_km`, `gumi_nyari_hasznalat_km` – téli és nyári gumin megtett km

**Főbb metódusok:**

- `__init__(...)` – az autó példányosítása, kezdeti értékek beállítása.
- `update_km_TKD(uj_km)` – az aktuális km-óra állás frissítése.
- `add_service_TKD(tipus, km, koltseg)` – új szervizbejegyzés hozzáadása, intervallum-követéshez az utolsó km frissítése.
- `add_fuel_TKD(megtett_km, liter, koltseg)` – új tankolás rögzítése (azóta megtett km, liter, Ft).
- `add_gumi_hasznalat_TKD(evszak, km)` – téli vagy nyári gumi használatának rögzítése km-ben.
- `gumi_hasznalat_TKD(evszak)` – visszaadja a téli / nyári gumi eddig megtett km-ét.
- `gumi_elettartam_TKD(evszak)` – 40 000 km-es becsült élettartamból számolja a még hátralévő km-et.
- `ossz_km_TKD()` – visszaadja az autóval megtett km-t (aktualis_km – vetel_km).
- `atlag_fogyasztas_TKD()` – átlagfogyasztás l/100 km-ben (tankolások alapján).
- `km_hatravan_TKD(tipus)` – megmondja, hány km van hátra az adott szervizig (olaj, vezérlés, fékek), vagy mennyivel lépte túl az intervallumot.
- `szerviz_koltseg_TKD()` – szervizköltségek összesítése.
- `uzemanyag_koltseg_TKD()` – üzemanyagköltségek összesítése.
- `koltseg_tipus_szerint_TKD(tipus)` – szervizköltségek összesítése típusonként (pl. olaj, gumi, egyéb).

---

### 2. `App_TKD` (main.py)

A teljes **grafikus felületet** és az eseménykezelést valósítja meg.

**Főbb metódusok:**

- `__init__(self, root)`
  - főablak beállítása (méret, cím, háttérszín, ikon),
  - bejelentkező/induló felület megjelenítése.
- `build_setup_ui(self)`
  - az induló ablak felépítése: autó alapadatainak bekérése.
- `create_auto_TKD(self)`
  - a megadott adatokból létrehoz egy `Auto_TKD` példányt,
  - továbblép a fő (költségkövető) felületre.
- `build_main_ui(self)`
  - fő felület felépítése (fejléc, szövegmező, gombok).
- `frissit_kijelzes_TKD(self)`
  - kiírja az aktuális állapotot a szövegmezőbe:
    - km adatok,
    - szerviz- és üzemanyagköltségek,
    - átlagfogyasztás,
    - tankolások statisztikája (átlagos liter / átlagos Ft tankolásonként),
    - szervizek hátralévő km-e vagy túllépése,
    - téli/nyári gumi használata és becsült élettartama,
    - költségek típusonként.
- `km_frissites_TKD(self)`
  - km-óra frissítése egy dialogusablakból (simpledialog).
- `uj_szerviz_TKD(self)`
  - felugró ablak, ahol több szerviztípust is ki lehet választani,
  - mindegyikhez külön költség megadásával.
- `uj_tankolas_TKD(self)`
  - tankolás rögzítése:
    - azóta megtett km,
    - tankolt liter,
    - tankolás összege Ft-ban.
- `gumi_hasznalat_TKD(self)`
  - felugró ablak:
    - évszak választása (téli / nyári),
    - az adott szezonban megtett km megadása.
- `mentes_fajlba_TKD(self)`
  - a fő szövegmező tartalmának mentése `roadcare_TKD_jelentes.txt` fájlba.

---

### 3. Globális függvény TKD monogrammal

- `fogyasztas_statisztika_TKD(auto: Auto_TKD)`
  - bemenet: egy `Auto_TKD` példány,
  - kimenet: a tankolások alapján:
    - átlagosan tankolt liter mennyisége,
    - átlagosan fizetett összeg (Ft),
  - a `statistics.mean` függvényt használja mindkét értékhez.

---

## Eseménykezelés és GUI

Az eseménykezelés gombnyomásokra történik:

- **Km frissítése** → `km_frissites_TKD`
- **Szerviz rögzítése** → `uj_szerviz_TKD`
- **Tankolás rögzítése** → `uj_tankolas_TKD`
- **Gumi használat** → `gumi_hasznalat_TKD`
- **Mentés fájlba** → `mentes_fajlba_TKD`
- **Kilépés** → `root.destroy()`

Minden gomb egy-egy metódust hív az `App_TKD` osztályban, ez teljesíti a feladat eseménykezelési és grafikus felületre vonatkozó követelményeit.

---

## A program futtatása

1. A projekt gyökerében legyenek az alábbi fájlok:
   - `main.py`
   - `auto_TKD.py`
   - opcionálisan `wheel.png` (ikon)
2. Python-ból vagy PyCharm-ból futtatható:
   - `python main.py`
3. Először az autó adatait kell megadni,
   majd megjelenik a fő felület, ahol a költségek és szervizek rögzíthetők.

