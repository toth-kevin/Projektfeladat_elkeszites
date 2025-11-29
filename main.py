import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import statistics
from auto_TKD import Auto_TKD, GUMI_INTERVAL_KM

def fogyasztas_statisztika_TKD(auto):
    if not auto.tankolasok_TKD:
        return None
    liter_lista = [t["liter"] for t in auto.tankolasok_TKD]
    koltseg_lista = [t["koltseg"] for t in auto.tankolasok_TKD]
    atlag_liter = statistics.mean(liter_lista)
    atlag_koltseg = statistics.mean(koltseg_lista)
    median_liter = statistics.median(liter_lista)
    szoras_liter = statistics.pstdev(liter_lista) if len(liter_lista) > 1 else 0.0
    return {
        "atlag_liter": atlag_liter,
        "atlag_koltseg": atlag_koltseg,
        "median_liter": median_liter,
        "szoras_liter": szoras_liter
    }

class App_TKD:
    def __init__(self, root):
        self.root = root
        self.root.title("RoadCare TKD – Autó szerviz és költségkövető")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ccddee")
        self.icon_image = None
        try:
            self.icon_image = tk.PhotoImage(file="assets/wheel.png")
            self.root.iconphoto(False, self.icon_image)
        except Exception:
            try:
                self.icon_image = tk.PhotoImage(file="wheel.png")
                self.root.iconphoto(False, self.icon_image)
            except Exception:
                self.icon_image = None
        self.auto = None
        self.setup_frame = tk.Frame(self.root, bg="#ccddee", padx=15, pady=15)
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        self.build_setup_ui()

    def build_setup_ui(self):
        tk.Label(self.setup_frame, text="Autó adatainak megadása", bg="#ccddee", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        labels = ["Márka:", "Típus:", "Évjárat:", "Rendszám:", "Vételkor km:", "Jelenlegi km:"]
        vars_ = []
        for i, t in enumerate(labels, start=1):
            tk.Label(self.setup_frame, text=t, bg="#ccddee").grid(row=i, column=0, sticky="e", pady=4, padx=4)
            v = tk.StringVar()
            vars_.append(v)
            tk.Entry(self.setup_frame, textvariable=v).grid(row=i, column=1, sticky="we", pady=4, padx=4)
        self.marka_var, self.tipus_var, self.evjarat_var, self.rendszam_var, self.vetel_km_var, self.km_var = vars_
        self.setup_frame.columnconfigure(1, weight=1)
        ttk.Button(self.setup_frame, text="Tovább", command=self.create_auto_TKD).grid(row=7, column=0, columnspan=2, pady=20)

    def create_auto_TKD(self):
        marka = self.marka_var.get().strip()
        tipus = self.tipus_var.get().strip()
        evjarat = self.evjarat_var.get().strip()
        rendszam = self.rendszam_var.get().strip()
        if not marka or not tipus or not evjarat or not rendszam:
            messagebox.showerror("Hiba", "Kérlek töltsd ki az összes adatmezőt (Márka, Típus, Évjárat, Rendszám).")
            return
        if len(rendszam) > 10:
            messagebox.showerror("Hiba", "A rendszám nem lehet hosszabb 10 karakternél.")
            return
        if not rendszam[0].isalpha():
            messagebox.showerror("Hiba", "A rendszámnak betűvel kell, hogy kezdődjön.")
            return
        if not rendszam[-1].isdigit():
            messagebox.showerror("Hiba", "A rendszámnak számmal kell, hogy végződjön.")
            return
        try:
            vetel_km = int(self.vetel_km_var.get())
            akt_km = int(self.km_var.get())
        except ValueError:
            messagebox.showerror("Hiba", "A km mezőkbe egész számot írj.")
            return
        if vetel_km < 0 or akt_km < 0:
            messagebox.showerror("Hiba", "A kilométer értékek nem lehetnek negatívak.")
            return
        if akt_km < vetel_km:
            messagebox.showerror("Hiba", "A jelenlegi kilométer nem lehet kisebb a vételkori kilométernél.")
            return
        self.auto = Auto_TKD(marka, tipus, evjarat, rendszam, vetel_km, akt_km)
        self.setup_frame.destroy()
        self.build_main_ui()

    def build_main_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#ccddee", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.fejlec = tk.Label(self.main_frame, font=("Arial", 14, "bold"), bg="#ccddee")
        self.fejlec.pack()
        utmutato = (
            "Útmutató:\n"
            "- A gombokkal frissítheted a km-órát, rögzítheted a szervizeket és tankolásokat.\n"
            "- A \"Gumi használat\" gombbal megadhatod, mennyit mentél téli/nyári gumival.\n"
            "- A \"Mentés\" gombbal elmentheted az állapotot saját fájlnévvel.\n"
            "- A \"Betöltés\" gombbal korábban mentett adatokat tölthetsz vissza."
        )
        tk.Label(self.main_frame, text=utmutato, justify="left", bg="#ccddee", font=("Arial", 9)).pack(pady=5, anchor="w")
        self.display = tk.Text(self.main_frame, bg="#eef5ff", width=85, height=20)
        self.display.pack(fill=tk.BOTH, expand=True, pady=10)
        g = tk.Frame(self.main_frame, bg="#ccddee")
        g.pack(pady=5)
        ttk.Button(g, text="Km frissítése", command=self.km_frissites_TKD).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(g, text="Szerviz rögzítése", command=self.uj_szerviz_TKD).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(g, text="Tankolás rögzítése", command=self.uj_tankolas_TKD).grid(row=0, column=2, padx=8, pady=8)
        ttk.Button(g, text="Gumi használat", command=self.gumi_hasznalat_TKD).grid(row=0, column=3, padx=8, pady=8)
        ttk.Button(g, text="Mentés", command=self.mentes_fajlba_TKD).grid(row=0, column=4, padx=8, pady=8)
        ttk.Button(g, text="Betöltés", command=self.betoltes_fajlbol_TKD).grid(row=0, column=5, padx=8, pady=8)
        ttk.Button(g, text="Kilépés", command=self.root.destroy).grid(row=0, column=6, padx=8, pady=8)
        self.frissit_kijelzes_TKD()

    def frissit_kijelzes_TKD(self):
        a = self.auto
        self.fejlec.config(text=f"{a.marka} {a.tipus} ({a.evjarat}) - {a.rendszam}")
        sorok = []
        sorok.append("Autó adatai")
        sorok.append(f"Aktuális km: {a.aktualis_km}")
        sorok.append(f"Vételkor km: {a.vetel_km}")
        sorok.append(f"Megtett km: {a.ossz_km_TKD()} km")
        sorok.append("")
        szerviz = a.szerviz_koltseg_TKD()
        uzemanyag = a.uzemanyag_koltseg_TKD()
        atlag = a.atlag_fogyasztas_TKD()
        sorok.append("Költségek összesen")
        sorok.append(f"Szervizköltség összesen: {szerviz:.0f} Ft")
        if atlag is None:
            sorok.append(f"Üzemanyagköltség összesen: {uzemanyag:.0f} Ft (átlagfogyasztás: nincs elég adat)")
        else:
            sorok.append(f"Üzemanyagköltség összesen: {uzemanyag:.0f} Ft (átlag: {atlag:.2f} l/100 km)")
        sorok.append("")
        sorok.append("Tankolási statisztika")
        stat = fogyasztas_statisztika_TKD(a)
        if stat is None:
            sorok.append("Tankolások: nincs elegendő adat.")
        else:
            sorok.append(f"Átlagosan {stat['atlag_liter']:.2f} litert tankolsz tankolásonként.")
            sorok.append(f"Átlagosan {stat['atlag_koltseg']:.0f} Ft-ot fizetsz tankolásonként.")
        sorok.append("")
        sorok.append("Szervizek esedékessége")
        def add_line(cim, key):
            diff = a.km_hatravan_TKD(key)
            if diff is None:
                sorok.append(f"{cim}: még nincs adat")
            elif diff < 0:
                sorok.append(f"{cim}: Kérjük, ellenőrizze, csere ajánlott! ({abs(diff)} km-rel túllépve)")
            else:
                sorok.append(f"{cim}: {diff} km múlva esedékes")
        add_line("Olajcsere", "olaj")
        add_line("Vezérlés csere", "vezerles")
        add_line("Fékek cseréje", "fekek")
        sorok.append("")
        sorok.append("Gumik használata")
        for evszak, cim in [("teli", "Téli gumi"), ("nyari", "Nyári gumi")]:
            felhasznalt = a.gumi_hasznalat_TKD(evszak)
            if felhasznalt <= 0:
                sorok.append(f"{cim}: nincs adat.")
            else:
                diff = a.gumi_elettartam_TKD(evszak)
                if diff >= 0:
                    sorok.append(f"{cim}: összesen {felhasznalt} km, becsült hátralévő: {diff} km (kb. {GUMI_INTERVAL_KM} km-ig, 8 éves korban ajánlott nagycserére.)")
                else:
                    sorok.append(f"{cim}: összesen {felhasznalt} km – Kérjük, ellenőrizze, csere ajánlott! ({abs(diff)} km-rel túllépve, kb. {GUMI_INTERVAL_KM} km felett, 8 éves korban ajánlott nagycserére.)")
        sorok.append("")
        sorok.append("Költségek típusonként")
        nevek = {"olaj": "Olajcsere", "vezerles": "Vezérlés", "fekek": "Fékek", "gumi": "Gumi", "egyeb": "Egyéb"}
        for kod, nev in nevek.items():
            sorok.append(f"{nev}: {a.koltseg_tipus_szerint_TKD(kod):.0f} Ft")
        self.display.delete("1.0", tk.END)
        self.display.insert(tk.END, "\n".join(sorok))

    def km_frissites_TKD(self):
        uj_km = simpledialog.askinteger("Km frissítés", "Új kilométeróra-állás:")
        if uj_km is None:
            return
        if uj_km <= self.auto.aktualis_km:
            messagebox.showerror("Hiba", "Az új kilométeróra-állásnak nagyobbnak kell lennie a jelenleginél.")
            return
        self.auto.update_km_TKD(uj_km)
        self.frissit_kijelzes_TKD()

    def uj_szerviz_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Szerviz rögzítése")
        ablak.geometry("500x360")
        ablak.configure(bg="#dde7ff")
        tk.Label(ablak, text="Szerviz km-állás:", bg="#dde7ff").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        km_var = tk.StringVar(value=str(self.auto.aktualis_km))
        tk.Entry(ablak, textvariable=km_var).grid(row=0, column=1, sticky="we", pady=5, padx=5)
        tipusok = [("Olajcsere", "olaj"), ("Vezérlés", "vezerles"), ("Fékek", "fekek"), ("Gumi", "gumi"), ("Egyéb", "egyeb")]
        valasztok = []
        koltseg_vars = []
        for i, (felirat, kod) in enumerate(tipusok, start=1):
            val = tk.IntVar()
            koltseg = tk.StringVar(value="0")
            tk.Checkbutton(ablak, text=felirat, variable=val, bg="#dde7ff").grid(row=i, column=0, sticky="w", padx=5)
            tk.Entry(ablak, textvariable=koltseg).grid(row=i, column=1, sticky="we", pady=3, padx=5)
            valasztok.append((kod, val))
            koltseg_vars.append(koltseg)
        ablak.columnconfigure(1, weight=1)
        def ment():
            try:
                km = int(km_var.get())
                if km < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Hiba", "A km mezőben pozitív egész számot adj meg.")
                return
            legalabb_egy = False
            for (kod, val), koltseg_var in zip(valasztok, koltseg_vars):
                if val.get() == 1:
                    try:
                        koltseg = float(koltseg_var.get())
                        if koltseg < 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Hiba", "A költség mezőkben pozitív számot adj meg.")
                        return
                    self.auto.add_service_TKD(kod, km, koltseg)
                    legalabb_egy = True
            if not legalabb_egy:
                messagebox.showerror("Hiba", "Válassz legalább egy szerviztípust.")
                return
            if km > self.auto.aktualis_km:
                self.auto.update_km_TKD(km)
            self.frissit_kijelzes_TKD()
            ablak.destroy()
        g = tk.Frame(ablak, bg="#dde7ff")
        g.grid(row=len(tipusok) + 1, column=0, columnspan=2, pady=10)
        ttk.Button(g, text="Mentés", command=ment).grid(row=0, column=0, padx=10)
        ttk.Button(g, text="Mégse", command=ablak.destroy).grid(row=0, column=1, padx=10)

    def uj_tankolas_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Tankolás rögzítése")
        ablak.geometry("420x220")
        ablak.configure(bg="#dde7ff")
        tk.Label(ablak, text="Tankoláskor mindig nullázd le a napi számlálót! ⛽🙂", bg="#dde7ff", font=("Arial", 9)).grid(row=0, column=0, columnspan=2, pady=8)
        tk.Label(ablak, text="Azóta megtett km:", bg="#dde7ff").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        tk.Label(ablak, text="Tankolt mennyiség (liter):", bg="#dde7ff").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        tk.Label(ablak, text="Tankolás összege (Ft):", bg="#dde7ff").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        km_var = tk.StringVar(value="0")
        liter_var = tk.StringVar(value="0")
        koltseg_var = tk.StringVar(value="0")
        tk.Entry(ablak, textvariable=km_var).grid(row=1, column=1, sticky="we", pady=5, padx=5)
        tk.Entry(ablak, textvariable=liter_var).grid(row=2, column=1, sticky="we", pady=5, padx=5)
        tk.Entry(ablak, textvariable=koltseg_var).grid(row=3, column=1, sticky="we", pady=5, padx=5)
        ablak.columnconfigure(1, weight=1)
        def ment():
            try:
                megtett = int(km_var.get())
                liter = float(liter_var.get())
                koltseg = float(koltseg_var.get())
                if megtett < 0 or liter <= 0 or koltseg < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Hiba", "Minden mezőbe pozitív számot írj, a liter nem lehet 0 vagy negatív.")
                return
            uj_km = self.auto.aktualis_km + megtett
            self.auto.add_fuel_TKD(megtett, liter, koltseg)
            self.auto.update_km_TKD(uj_km)
            self.frissit_kijelzes_TKD()
            ablak.destroy()
        g = tk.Frame(ablak, bg="#dde7ff")
        g.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(g, text="Mentés", command=ment).grid(row=0, column=0, padx=10)
        ttk.Button(g, text="Mégse", command=ablak.destroy).grid(row=0, column=1, padx=10)

    def gumi_hasznalat_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Gumi használat rögzítése")
        ablak.geometry("420x220")
        ablak.configure(bg="#dde7ff")
        tk.Label(ablak, text="Válassz évszakot:", bg="#dde7ff").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        evszak_var = tk.StringVar(value="teli")
        rb1 = tk.Radiobutton(ablak, text="Téli gumi", variable=evszak_var, value="teli", bg="#dde7ff")
        rb2 = tk.Radiobutton(ablak, text="Nyári gumi", variable=evszak_var, value="nyari", bg="#dde7ff")
        rb1.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        rb2.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        tk.Label(ablak, text="Ebben az évszakban megtett km:", bg="#dde7ff").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        km_var = tk.StringVar(value="0")
        tk.Entry(ablak, textvariable=km_var).grid(row=2, column=1, sticky="we", pady=5, padx=5)
        ablak.columnconfigure(1, weight=1)
        def ment():
            try:
                km = int(km_var.get())
                if km < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Hiba", "A km mezőben pozitív egész számot adj meg.")
                return
            self.auto.add_gumi_hasznalat_TKD(evszak_var.get(), km)
            self.frissit_kijelzes_TKD()
            ablak.destroy()
        gomb = tk.Frame(ablak, bg="#dde7ff")
        gomb.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(gomb, text="Mentés", command=ment).grid(row=0, column=0, padx=10)
        ttk.Button(gomb, text="Mégse", command=ablak.destroy).grid(row=0, column=1, padx=10)

    def mentes_fajlba_TKD(self):
        if self.auto is None:
            return
        filename = filedialog.asksaveasfilename(title="Mentés", defaultextension=".json", filetypes=[("JSON fájl", "*.json"), ("Minden fájl", "*.*")])
        if not filename:
            return
        a = self.auto
        adat = {
            "marka": a.marka,
            "tipus": a.tipus,
            "evjarat": a.evjarat,
            "rendszam": a.rendszam,
            "vetel_km": a.vetel_km,
            "aktualis_km": a.aktualis_km,
            "utolso_olaj_km": a.utolso_olaj_km,
            "utolso_vezerles_km": a.utolso_vezerles_km,
            "utolso_fek_km": a.utolso_fek_km,
            "szervizek_TKD": a.szervizek_TKD,
            "tankolasok_TKD": a.tankolasok_TKD,
            "gumi_teli_hasznalat_km": a.gumi_teli_hasznalat_km,
            "gumi_nyari_hasznalat_km": a.gumi_nyari_hasznalat_km
        }
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(adat, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Mentés", "Adatok sikeresen elmentve.")
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült menteni: {e}")

    def betoltes_fajlbol_TKD(self):
        filename = filedialog.askopenfilename(title="Betöltés", filetypes=[("JSON fájl", "*.json"), ("Minden fájl", "*.*")])
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                adat = json.load(f)
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült betölteni: {e}")
            return
        try:
            marka = adat.get("marka", "")
            tipus = adat.get("tipus", "")
            evjarat = adat.get("evjarat", "")
            rendszam = adat.get("rendszam", "")
            vetel_km = adat.get("vetel_km", 0)
            aktualis_km = adat.get("aktualis_km", vetel_km)
            auto = Auto_TKD(marka, tipus, evjarat, rendszam, vetel_km, aktualis_km)
            auto.utolso_olaj_km = adat.get("utolso_olaj_km")
            auto.utolso_vezerles_km = adat.get("utolso_vezerles_km")
            auto.utolso_fek_km = adat.get("utolso_fek_km")
            auto.szervizek_TKD = adat.get("szervizek_TKD", [])
            auto.tankolasok_TKD = adat.get("tankolasok_TKD", [])
            auto.gumi_teli_hasznalat_km = adat.get("gumi_teli_hasznalat_km", 0)
            auto.gumi_nyari_hasznalat_km = adat.get("gumi_nyari_hasznalat_km", 0)
        except Exception:
            messagebox.showerror("Hiba", "A betöltött fájl formátuma érvénytelen.")
            return
        self.auto = auto
        self.frissit_kijelzes_TKD()

if __name__ == "__main__":
    root = tk.Tk()
    app = App_TKD(root)
    root.mainloop()
