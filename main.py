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
    return {
        "atlag_liter": statistics.mean(liter_lista),
        "atlag_koltseg": statistics.mean(koltseg_lista)
    }

class App_TKD:
    def __init__(self, root):
        self.root = root
        self.root.title("RoadCare TKD – Autó költségkövető")
        self.root.geometry("1000x700")
        self.root.configure(bg="#ccddee")
        self.auto = None
        self.setup_frame = tk.Frame(self.root, bg="#ccddee", padx=15, pady=15)
        self.setup_frame.pack(fill=tk.BOTH, expand=True)
        self.build_setup_ui()

    def build_setup_ui(self):
        tk.Label(self.setup_frame, text="Autó adatainak megadása", bg="#ccddee", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        labels = ["Márka:", "Típus:", "Évjárat:", "Rendszám:", "Vételkor km:", "Jelenlegi km:"]
        vars_ = []
        for i, t in enumerate(labels, start=1):
            tk.Label(self.setup_frame, text=t, bg="#ccddee").grid(row=i, column=0, sticky="e", pady=4)
            v = tk.StringVar()
            vars_.append(v)
            tk.Entry(self.setup_frame, textvariable=v).grid(row=i, column=1, sticky="we", pady=4)
        self.marka_var, self.tipus_var, self.evjarat_var, self.rendszam_var, self.vetel_km_var, self.km_var = vars_
        self.setup_frame.columnconfigure(1, weight=1)
        ttk.Button(self.setup_frame, text="Tovább", command=self.create_auto_TKD).grid(row=7, column=0, columnspan=2, pady=20)

    def create_auto_TKD(self):
        marka = self.marka_var.get().strip()
        tipus = self.tipus_var.get().strip()
        evjarat = self.evjarat_var.get().strip()
        rendszam = self.rendszam_var.get().strip()
        if not marka or not tipus or not evjarat or not rendszam:
            messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni.")
            return
        if len(rendszam) > 10:
            messagebox.showerror("Hiba", "A rendszám maximum 10 karakter lehet.")
            return
        if not rendszam[0].isalpha():
            messagebox.showerror("Hiba", "A rendszámnak betűvel kell kezdődnie.")
            return
        if not rendszam[-1].isdigit():
            messagebox.showerror("Hiba", "A rendszámnak számmal kell végződnie.")
            return
        try:
            vetel_km = int(self.vetel_km_var.get())
            akt_km = int(self.km_var.get())
        except:
            messagebox.showerror("Hiba", "Kilométer mezőkben csak szám szerepelhet.")
            return
        if vetel_km < 0 or akt_km < 0:
            messagebox.showerror("Hiba", "A kilométer nem lehet negatív.")
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
        self.display = tk.Text(self.main_frame, bg="#eef5ff", width=85, height=20)
        self.display.pack(fill=tk.BOTH, expand=True, pady=10)
        g = tk.Frame(self.main_frame, bg="#ccddee")
        g.pack()
        ttk.Button(g, text="Km frissítése", command=self.km_frissites_TKD).grid(row=0, column=0, padx=5)
        ttk.Button(g, text="Szerviz", command=self.uj_szerviz_TKD).grid(row=0, column=1, padx=5)
        ttk.Button(g, text="Tankolás", command=self.uj_tankolas_TKD).grid(row=0, column=2, padx=5)
        ttk.Button(g, text="Gumi", command=self.gumi_hasznalat_TKD).grid(row=0, column=3, padx=5)
        ttk.Button(g, text="Mentés", command=self.mentes_fajlba_TKD).grid(row=0, column=4, padx=5)
        ttk.Button(g, text="Betöltés", command=self.betoltes_fajlbol_TKD).grid(row=0, column=5, padx=5)
        ttk.Button(g, text="Kilépés", command=self.root.destroy).grid(row=0, column=6, padx=5)
        self.frissit_kijelzes_TKD()

    def frissit_kijelzes_TKD(self):
        a = self.auto
        self.fejlec.config(text=f"{a.marka} {a.tipus} ({a.evjarat}) - {a.rendszam}")
        t = []
        t.append(f"Aktuális km: {a.aktualis_km}")
        t.append(f"Vételkor km: {a.vetel_km}")
        t.append(f"Megtett km: {a.ossz_km_TKD()} km\n")
        t.append(f"Szerviz költség: {a.szerviz_koltseg_TKD():.0f} Ft")
        t.append(f"Üzemanyag költség: {a.uzemanyag_koltseg_TKD():.0f} Ft\n")
        stat = fogyasztas_statisztika_TKD(a)
        if stat:
            t.append(f"Átlag tankolás: {stat['atlag_liter']:.2f} liter")
            t.append(f"Átlag tankolási költség: {stat['atlag_koltseg']:.0f} Ft\n")
        def add(x, k):
            d = a.km_hatravan_TKD(k)
            if d is None:
                t.append(f"{x}: nincs adat")
            elif d < 0:
                t.append(f"{x}: csere ajánlott ({abs(d)} km-t túllépve)")
            else:
                t.append(f"{x}: {d} km múlva")
        add("Olajcsere", "olaj")
        add("Vezérlés", "vezerles")
        add("Fékek", "fekek")
        t.append(f"\nTéli gumi használat: {a.gumi_teli_hasznalat_km} km")
        t.append(f"Nyári gumi használat: {a.gumi_nyari_hasznalat_km} km")
        self.display.delete("1.0", tk.END)
        self.display.insert(tk.END, "\n".join(t))

    def km_frissites_TKD(self):
        uj_km = simpledialog.askinteger("Km frissítés", "Új kilométeróra érték:")
        if uj_km is None:
            return
        if uj_km <= self.auto.aktualis_km:
            messagebox.showerror("Hiba", "Az új kilométernek nagyobbnak kell lennie a jelenleginél.")
            return
        self.auto.update_km_TKD(uj_km)
        self.frissit_kijelzes_TKD()

    def uj_szerviz_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Szerviz")
        ablak.geometry("400x200")
        tk.Label(ablak, text="Km:").grid(row=0, column=0)
        km_var = tk.StringVar()
        tk.Entry(ablak, textvariable=km_var).grid(row=0, column=1)
        tk.Label(ablak, text="Költség:").grid(row=1, column=0)
        kolt_var = tk.StringVar()
        tk.Entry(ablak, textvariable=kolt_var).grid(row=1, column=1)
        tk.Label(ablak, text="Típus:").grid(row=2, column=0)
        tip = ttk.Combobox(ablak, values=["olaj", "vezerles", "fekek", "gumi", "egyeb"])
        tip.grid(row=2, column=1)

        def ment():
            try:
                km = int(km_var.get())
                kolt = float(kolt_var.get())
            except:
                messagebox.showerror("Hiba", "Számot adj meg.")
                return
            if km < 0 or kolt < 0:
                messagebox.showerror("Hiba", "Negatív érték nem adható meg.")
                return
            self.auto.add_service_TKD(tip.get(), km, kolt)
            if km > self.auto.aktualis_km:
                self.auto.update_km_TKD(km)
            self.frissit_kijelzes_TKD()
            ablak.destroy()

        ttk.Button(ablak, text="Mentés", command=ment).grid(row=3, column=0)
        ttk.Button(ablak, text="Mégse", command=ablak.destroy).grid(row=3, column=1)

    def uj_tankolas_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Tankolás")
        ablak.geometry("400x200")
        tk.Label(ablak, text="Megtet km:").grid(row=0, column=0)
        km_var = tk.StringVar()
        tk.Entry(ablak, textvariable=km_var).grid(row=0, column=1)
        tk.Label(ablak, text="Liter:").grid(row=1, column=0)
        l_var = tk.StringVar()
        tk.Entry(ablak, textvariable=l_var).grid(row=1, column=1)
        tk.Label(ablak, text="Ft:").grid(row=2, column=0)
        k_var = tk.StringVar()
        tk.Entry(ablak, textvariable=k_var).grid(row=2, column=1)

        def ment():
            try:
                tkm = int(km_var.get())
                lit = float(l_var.get())
                ft = float(k_var.get())
            except:
                messagebox.showerror("Hiba", "Számot adj meg.")
                return
            if tkm < 0 or lit <= 0 or ft < 0:
                messagebox.showerror("Hiba", "Negatív érték nem adható meg.")
                return
            uj_km = self.auto.aktualis_km + tkm
            self.auto.add_fuel_TKD(tkm, lit, ft)
            self.auto.update_km_TKD(uj_km)
            self.frissit_kijelzes_TKD()
            ablak.destroy()

        ttk.Button(ablak, text="Mentés", command=ment).grid(row=3, column=0)
        ttk.Button(ablak, text="Mégse", command=ablak.destroy).grid(row=3, column=1)

    def gumi_hasznalat_TKD(self):
        ablak = tk.Toplevel(self.root)
        ablak.title("Gumi")
        ablak.geometry("300x150")
        tk.Label(ablak, text="Évszak:").grid(row=0, column=0)
        e = ttk.Combobox(ablak, values=["teli", "nyari"])
        e.grid(row=0, column=1)
        tk.Label(ablak, text="Megtett km:").grid(row=1, column=0)
        k = tk.StringVar()
        tk.Entry(ablak, textvariable=k).grid(row=1, column=1)

        def ment():
            try:
                km = int(k.get())
            except:
                messagebox.showerror("Hiba", "Számot adj meg.")
                return
            if km < 0:
                messagebox.showerror("Hiba", "Negatív érték nem adható meg.")
                return
            self.auto.add_gumi_hasznalat_TKD(e.get(), km)
            self.frissit_kijelzes_TKD()
            ablak.destroy()

        ttk.Button(ablak, text="Mentés", command=ment).grid(row=2, column=0)
        ttk.Button(ablak, text="Mégse", command=ablak.destroy).grid(row=2, column=1)

    def mentes_fajlba_TKD(self):
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if not f:
            return
        with open(f, "w", encoding="utf-8") as t:
            json.dump(self.auto.__dict__, t, ensure_ascii=False, indent=2)
        messagebox.showinfo("OK", "Mentve.")

    def betoltes_fajlbol_TKD(self):
        f = filedialog.askopenfilename()
        if not f:
            return
        with open(f, "r", encoding="utf-8") as t:
            a = json.load(t)
        auto = Auto_TKD(a["marka"], a["tipus"], a["evjarat"], a["rendszam"], a["vetel_km"], a["aktualis_km"])
        auto.szervizek_TKD = a["szervizek_TKD"]
        auto.tankolasok_TKD = a["tankolasok_TKD"]
        auto.gumi_teli_hasznalat_km = a["gumi_teli_hasznalat_km"]
        auto.gumi_nyari_hasznalat_km = a["gumi_nyari_hasznalat_km"]
        auto.utolso_olaj_km = a["utolso_olaj_km"]
        auto.utolso_vezerles_km = a["utolso_vezerles_km"]
        auto.utolso_fek_km = a["utolso_fek_km"]
        self.auto = auto
        self.frissit_kijelzes_TKD()

if __name__ == "__main__":
    root = tk.Tk()
    app = App_TKD(root)
    root.mainloop()
