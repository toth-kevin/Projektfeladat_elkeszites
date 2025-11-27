# 🚗 RoadCare TKD – Autós költségkövető alkalmazás

**Hallgató:** Tóth Kevin Dorian  
**Neptun kód:** MAXEBH  
**Tantárgy:** Script nyelvek / Projekt feladat

---

## 📌 Projekt célja

A RoadCare TKD egy autófenntartási és költségkezelési alkalmazás.  
Segítséget nyújt a felhasználóknak abban, hogy nyomon kövessék az autójuk:

- futásteljesítményét,
- tankolási szokásait,
- átlagos fogyasztását,
- szervizköltségeit és intervallumait,
- gumiabroncsok használatát.

A program célja egy átlátható, egyszerűen kezelhető rendszer biztosítása,  
amely hosszú távon segíti a jármű fenntartásának tervezését.

---

# 🧠 Használt modulok

## ✔️ 1. Saját modul – `auto_TKD.py`
Tartalmazza a projekt fő adatszerkezeti és logikai részeit:

- **Auto_TKD osztály** autóadatokhoz
- tankolási lista
- szerviz lista
- gumi használat
- intervallum számítás
- átlagfogyasztás és költség számítás

A projekt követelményeinek megfelelően a modul neve `_TKD` végződéssel rendelkezik.

---

## ✔️ 2. Standard modul – `datetime`
Szerviz és tankolás rögzítésekor automatikusan menti:
- aktuális dátum ISO formátumban

---

## ✔️ 3. Standard modul – `statistics`
A tankolási adatok elemzésére:
- átlag liter / tankolás
- átlag tankolási költség

---

# 📦 Mappa szerkezet
PythonProject/
│
├── main.py # GUI és logika
├── auto_TKD.py # Osztályok és adatkezelés
├── assets/ # képek, ikonok
├── auto_adatok_TKD.json # állapot mentés (opcionális)
└── README.md


---

# 🏎️ Program működése — lépéseiben

## 1️⃣ Indítás
A program induláskor bekéri az autó alapadatait:

- márka
- típus
- évjárat
- rendszám (validálva!)
- vételkori kilométer
- aktuális kilométer

### Rendszám validáció:
- maximum 10 karakter
- **első karakter betű**
- **utolsó karakter szám**
- egyébként hibaüzenet
- Rugalmasnak kell lennie mivel több szabványos, illetve egyedi rendszám is elérhető

### Kilométer validáció:
- nem lehet negatív
- aktuális KM ≥ vételkori KM

---

## 2️⃣ Főoldal (GUI)

Megjelenít:

### ✔ Aktuális adatok
- jelenlegi kilométer
- vételkori kilométer
- összes megtett km

### ✔ Tankolási statisztika
- liter / tankolás átlag
- Ft / tankolás átlag
- összes üzemanyagköltség

### ✔ Szerviz intervallumok
- olajcsere
- vezérlés
- fékek

Ha intervallum lejárt → **„csere ajánlott”**

### ✔ Gumi használat
- téli gumi km
- nyári gumi km
- hátralévő élettartam km-ben

---

# 🛠️ Funkciók

## ➤ Kilométer frissítés
- értéknek nagyobbnak kell lennie a jelenleginél
- magyar nyelvű hibaüzenet

## ➤ Szerviz rögzítés
Megadható:
- km
- költség
- típus:
  - olaj
  - vezérlés
  - fékek
  - gumi
  - egyéb

Negatív érték tiltott.

## ➤ Tankolás
Megadható:
- megtett km
- tankolt liter
- fizetett Ft

Értékszabályok:
- liter > 0
- km ≥ 0
- Ft ≥ 0

Automatikusan frissíti a kilométer állást.

## ➤ Gumi használat
- téli vagy nyári szezon
- megtett km / szezon

Nem a futóműhöz, hanem a szezonhoz kötött használat.

## ➤ Mentés fájlba
- JSON formátum
- felhasználó által megadott fájlnév
- bármely mappába menthető

## ➤ Betöltés
- előző mentés visszaállítása
- biztonságos adatbetöltés

---

# 🏗️ Osztályok és metódusok

## `Auto_TKD` — adatkezelő osztály

### Tulajdonságok:
- márka, típus, évjárat
- rendszám
- km adatok
- szervizek
- tankolások
- gumi használat

### Fő metódusok:
| Metódus | Leírás |
|---|---|
| `update_km_TKD()` | km növelés |
| `add_service_TKD()` | szerviz rögzítés |
| `add_fuel_TKD()` | tankolás rögzítés |
| `add_gumi_hasznalat_TKD()` | szezon gumi használat |
| `km_hatravan_TKD()` | intervallum visszaszámolás |
| `atlag_fogyasztas_TKD()` | l/100 km számítás |
| `szerviz_koltseg_TKD()` | teljes szerviz költség |
| `uzemanyag_koltseg_TKD()` | tankolás költség |
| `gumi_elettartam_TKD()` | hátralévő életkilométer |

---

# 💾 Mentés formátuma (JSON)

