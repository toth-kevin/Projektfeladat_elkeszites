import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from auto_TKD import Auto_TKD

class App_TKD:
    def __init__(self, root):
        self.root = root
        self.root.title("RoadCare TKD – Autó szerviz és költségkövető")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ccddee")

        self.icon_image = None
        try:
            self.icon_image = tk.PhotoImage(file="wheel.png")
            self.root.iconphoto(False, self.icon_image)
        except Exception:
            pass

        self.auto = None
        self.setup_frame = tk.Frame(self.root, bg="#ccddee", padx=15, pady=15)
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        self.build_setup_ui()

    def build_setup_ui(self):
        tk.Label(self.setup_frame, text="Autó adatainak megadása",
                 bg="#ccddee", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Márka:", "Típus:", "Évjárat:", "Rendszám:", "Vételkor km:", "Jelenlegi km:"]
        vars_ = []

        for i, text in enumerate(labels, start=1):
            tk.Label(self.setup_frame, text=text, bg="#ccddee").grid(row=i, column=0, sticky="e", pady=4)
            var = tk.StringVar()
            vars_.append(var)
            tk.Entry(self.setup_frame, textvariable=var).grid(row=i, column=1, sticky="we", pady=4)

        self.marka_var, self.tipus_var, self.evjarat_var, self.rendszam_var, self.vetel_km_var, self.km_var = vars_
        self.vetel_km_var.set("0")
        self.km_var.set("0")

        ttk.Button(self.setup_frame, text="Tovább", command=self.create_auto_TKD)\
            .grid(row=7, column=0, columnspan=2, pady=20)

        self.setup_frame.columnconfigure(1, weight=1)

    def create_auto_TKD(self):
        try:
            vetel_km = int(self.vetel_km_var.get())
            akt_km = int(self.km_var.get())
        except ValueError:
            messagebox.showerror("Hiba", "A km mezőkbe számot írj!")
            return

        self.auto = Auto_TKD(
            self.marka_var.get(),
            self.tipus_var.get(),
            self.evjarat_var.get(),
            self.rendszam_var.get(),
            vetel_km,
            akt_km
        )

        self.setup_frame.destroy()
        self.build_main_ui()

    def build_main_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#ccddee", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.fejlec = tk.Label(self.main_frame, font=("Arial", 14, "bold"), bg="#ccddee")
        self.fejlec.pack()

        self.display = tk.Text(self.main_frame, bg="#eef5ff", width=85, height=20)
        self.display.pack(fill=tk.BOTH, expand=True, pady=10)

        g = tk.Frame(self.main_frame, bg="#ccddee")
        g.pack(pady=5)

        ttk.Button(g, text="Km frissítése", command=self.km_frissites_TKD).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(g, text="Szerviz rögzítése", command=self.uj_szerviz_TKD).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(g, text="Tankolás rögzítése", command=self.uj_tankolas_TKD).grid(row=0, column=2, padx=8, pady=8)
        ttk.Button(g, text="Mentés fájlba", command=self.mentes_fajlba_TKD).grid(row=0, column=3, padx=8, pady=8)
        ttk.Button(g, text="Kilépés", command=self.root.destroy).grid(row=0, column=4, padx=8, pady=8)

        self.frissit_kijelzes_TKD()

    def frissit_kijelzes_TKD(self):
        a = self.auto
        self.fejlec.config(text=f"{a.marka} {a.tipus} ({a.evjarat}) - {a.rendszam}")
        self.display.delete("1.0", tk.END)

        sorok = []
        sorok.append(f"Aktuális km: {a.aktualis_km}")
        sorok.append(f"Vételkor km: {a.vetel_km}")
        sorok.append(f"Megtett km: {a.ossz_km_TKD()} km")
        sorok.append("")

        szerviz = a.szerviz_koltseg_TKD()
        uzemanyag = a.uzemanyag_koltseg_TKD()
        atlag = a.atlag_fogyasztas_TKD()

        sorok.append(f"Szervizköltség összesen: {szerviz:.0f} Ft")
        if atlag is None:
            sorok.append(f"Üzemanyagköltség összesen: {uzemanyag:.0f} Ft (átlagfogyasztás: nincs elég adat)")
        else:
            sorok.append(f"Üzemanyagköltség összesen: {uzemanyag:.0f} Ft (átlag: {atlag:.2f} l/100 km)")
        sorok.append("")

        def add_line(cim, key, extra=""):
            km = a.km_hatravan_TKD(key)
            if km is not None:
                if extra:
                    sorok.append(f"{cim}: {km} km múlva {extra}")
                else:
                    sorok.append(f"{cim}: {km} km múlva")
            else:
                sorok.append(f"{cim}: még nincs adat")

        add_line("Olajcsere", "olaj")
        add_line("Vezérlés csere", "vezerles")
        add_line("Fékek cseréje", "fekek")
        add_line("Téli gumi csere", "gumi_teli", "(8 éves korban ajánlott nagycserére.)")
        add_line("Nyári gumi csere", "gumi_nyari", "(8 éves korban ajánlott nagycserére.)")

        sorok.append("")
        sorok.append("Költségek típusonként:")
        nevek = {
            "olaj": "Olajcsere",
            "vezerles": "Vezérlés",
            "fekek": "Fékek",
            "gumi_teli": "Téli gumi",
            "gumi_nyari": "Nyári gumi"
        }
        for kod, nev in nevek.items():
            sorok.append(f"{nev}: {a.koltseg_tipus_szerint_TKD(kod):.0f} Ft")

        self.display.insert(tk.END, "\n".join(sorok))

    def km_frissites_TKD(self):
        uj_km = simpledialog.askinteger(
            "Km frissítés",
            "Új kilométeróra-állás:",
            initialvalue=self.auto.aktualis_km,
            minvalue=self.auto.aktualis_km
        )
        if uj_km is None:
            return
        self.auto.update_km_TKD(uj_km)
        self.frissit_kijelzes_TKD()

    def uj_szerviz_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Szerviz rögzítése")
        ablak.geometry("500x320")
        ablak.configure(bg="#dde7ff")

        tk.Label(ablak, text="Szerviz km-állás:", bg="#dde7ff").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        km_var = tk.StringVar(value=str(self.auto.aktualis_km))
        tk.Entry(ablak, textvariable=km_var).grid(row=0, column=1, sticky="we", pady=5, padx=5)

        tipusok = [
            ("Olajcsere", "olaj"),
            ("Vezérlés", "vezerles"),
            ("Fékek", "fekek"),
            ("Téli gumi", "gumi_teli"),
            ("Nyári gumi", "gumi_nyari")
        ]

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
            except ValueError:
                messagebox.showerror("Hiba", "A km mezőben számot adj meg.")
                return

            legalabb_egy = False
            for (kod, val), koltseg_var in zip(valasztok, koltseg_vars):
                if val.get() == 1:
                    try:
                        koltseg = float(koltseg_var.get())
                    except ValueError:
                        messagebox.showerror("Hiba", "A költség mezőben számot adj meg.")
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
        g.grid(row=len(tipusok)+1, column=0, columnspan=2, pady=10)
        ttk.Button(g, text="Mentés", command=ment).grid(row=0, column=0, padx=10)
        ttk.Button(g, text="Mégse", command=ablak.destroy).grid(row=0, column=1, padx=10)

    def uj_tankolas_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Tankolás rögzítése")
        ablak.geometry("420x220")
        ablak.configure(bg="#dde7ff")

        tk.Label(
            ablak,
            text="Tankoláskor mindig nullázd le a napi számlálót! ⛽🙂",
            bg="#dde7ff",
            font=("Arial", 9)
        ).grid(row=0, column=0, columnspan=2, pady=8)

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
            except ValueError:
                messagebox.showerror("Hiba", "Minden mezőbe számot írj.")
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

    def mentes_fajlba_TKD(self):
        szoveg = self.display.get("1.0", tk.END)
        try:
            with open("roadcare_TKD_jelentes.txt", "w", encoding="utf-8") as f:
                f.write(szoveg)
            messagebox.showinfo("Mentés", "Adatok elmentve: roadcare_TKD_jelentes.txt")
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült menteni: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App_TKD(root)
    root.mainloop()
