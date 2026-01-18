import customtkinter as ctk
from tkinter import messagebox
from fractions import Fraction

# =============================================================================
# 1. BÖLÜM: SİRÂCİYYE HESAPLAMA MOTORU (MANTIK)
# =============================================================================
class SiraciyyeMotoru:
    def __init__(self):
        self.reset()

    def reset(self):
        self.varisler = {}
        self.paylar = {}
        self.logs = []
        self.asabe_kim = None

    def log(self, mesaj):
        self.logs.append(mesaj)

    def varis_yukle(self, veri):
        self.varisler = veri.copy()
        for k in self.varisler:
            if self.varisler[k] < 0: self.varisler[k] = 0

    def erkek_cocuk_var(self):
        return self.varisler.get('ogul', 0) > 0 or self.varisler.get('ogul_oglu', 0) > 0
    
    def cocuk_var(self):
        return self.erkek_cocuk_var() or self.varisler.get('kiz', 0) > 0 or self.varisler.get('ogul_kizi', 0) > 0

    def hesapla(self):
        self.paylar = {}
        self.logs = []
        self.asabe_kim = None
        
        # --- 1. ADIM: HACB (ENGELLEME) ---
        if self.varisler.get('baba', 0) > 0 and self.varisler.get('dede', 0) > 0:
            self.varisler['dede'] = 0
            self.log("HACB: Baba olduğu için Dede düştü.")

        if self.varisler.get('anne', 0) > 0:
            if self.varisler.get('nine_anne', 0) > 0 or self.varisler.get('nine_baba', 0) > 0:
                self.varisler['nine_anne'] = 0; self.varisler['nine_baba'] = 0
                self.log("HACB: Anne olduğu için Nineler düştü.")
        
        if self.varisler.get('baba', 0) > 0 and self.varisler.get('nine_baba', 0) > 0:
            self.varisler['nine_baba'] = 0
            self.log("HACB: Baba olduğu için Baba Annesi düştü.")

        if self.varisler.get('ogul', 0) > 0:
            if self.varisler.get('ogul_oglu', 0) > 0: self.varisler['ogul_oglu'] = 0
            if self.varisler.get('ogul_kizi', 0) > 0: self.varisler['ogul_kizi'] = 0
            self.log("HACB: Oğul olduğu için torunlar düştü.")

        engelleyen = (self.erkek_cocuk_var() or self.varisler.get('baba', 0) > 0 or self.varisler.get('dede', 0) > 0)
        kardesler_amcalar = ['erkek_kardes_oz', 'kiz_kardes_oz', 'erkek_kardes_baba', 'kiz_kardes_baba', 'kardes_anne', 'amca', 'amca_oglu']
        
        if engelleyen:
            dusecek_var_mi = any(self.varisler.get(k, 0) > 0 for k in kardesler_amcalar)
            if dusecek_var_mi:
                for k in kardesler_amcalar: self.varisler[k] = 0
                self.log("HACB: Asıl (Baba/Dede) veya Erkek Fer (Oğul) olduğu için Kardeşler/Amcalar düştü.")

        if self.varisler.get('erkek_kardes_oz', 0) > 0:
            for k in ['erkek_kardes_baba', 'kiz_kardes_baba']:
                if self.varisler.get(k, 0) > 0:
                    self.varisler[k] = 0
                    self.log(f"HACB: Öz Erkek Kardeş olduğu için {k} düştü.")

        # --- 2. ADIM: FARZ SAHİPLERİ ---
        # Koca/Karı
        if self.varisler.get('koca', 0) > 0:
            self.paylar['koca'] = Fraction(1, 4) if self.cocuk_var() else Fraction(1, 2)
            self.log(f"Koca: {'Çocuk var (1/4)' if self.cocuk_var() else 'Çocuk yok (1/2)'}.")
        elif self.varisler.get('kari', 0) > 0:
            self.paylar['kari'] = Fraction(1, 8) if self.cocuk_var() else Fraction(1, 4)
            self.log(f"Karı: {'Çocuk var (1/8)' if self.cocuk_var() else 'Çocuk yok (1/4)'}.")

        # Baba
        if self.varisler.get('baba', 0) > 0:
            if self.erkek_cocuk_var():
                self.paylar['baba'] = Fraction(1, 6)
                self.log("Baba: Erkek çocuk var (1/6).")
            elif self.varisler.get('kiz', 0) > 0 or self.varisler.get('ogul_kizi', 0) > 0:
                self.paylar['baba'] = Fraction(1, 6)
                self.log("Baba: Kız çocuk var (1/6 + Asabe).")
            else:
                self.paylar['baba'] = 0
                self.log("Baba: Çocuk yok (Asabe).")

        # Anne & Ömeriyye
        if self.varisler.get('anne', 0) > 0:
            kardes_sayisi = sum(self.varisler.get(k,0) for k in ['erkek_kardes_oz','kiz_kardes_oz','erkek_kardes_baba','kiz_kardes_baba','kardes_anne'])
            var_olanlar = [k for k,v in self.varisler.items() if v > 0]
            omeriyye = ('baba' in var_olanlar and 'anne' in var_olanlar and ('koca' in var_olanlar or 'kari' in var_olanlar))
            
            if self.cocuk_var() or kardes_sayisi >= 2:
                self.paylar['anne'] = Fraction(1, 6)
                self.log("Anne: Çocuk veya kardeşler var (1/6).")
            elif omeriyye and not self.cocuk_var():
                es_payi = self.paylar.get('koca', 0) + self.paylar.get('kari', 0)
                self.paylar['anne'] = (1 - es_payi) * Fraction(1, 3)
                self.log("Anne: Ömeriyye Hali (Kalanın 1/3'ü).")
            else:
                self.paylar['anne'] = Fraction(1, 3)
                self.log("Anne: Normal hal (1/3).")

        # Kız
        if self.varisler.get('kiz', 0) > 0 and self.varisler.get('ogul', 0) == 0:
            self.paylar['kiz'] = Fraction(1, 2) if self.varisler['kiz'] == 1 else Fraction(2, 3)
            self.log(f"Kız(lar): {'Tek (1/2)' if self.varisler['kiz']==1 else 'Çoklu (2/3)'}.")

        # Oğul Kızı
        if self.varisler.get('ogul_kizi', 0) > 0 and self.varisler.get('ogul', 0) == 0 and self.varisler.get('ogul_oglu', 0) == 0:
            kiz_sayisi = self.varisler.get('kiz', 0)
            if kiz_sayisi == 0:
                self.paylar['ogul_kizi'] = Fraction(1, 2) if self.varisler['ogul_kizi'] == 1 else Fraction(2, 3)
                self.log("Oğul Kızı: Kız gibi pay aldı.")
            elif kiz_sayisi == 1:
                self.paylar['ogul_kizi'] = Fraction(1, 6)
                self.log("Oğul Kızı: Tekmiletü's-sülüsân (1/6).")
            else:
                self.varisler['ogul_kizi'] = 0
                self.log("Oğul Kızı: Kızlar 2/3'ü doldurduğu için düştü.")

        # Nineler
        nine_toplam = self.varisler.get('nine_anne', 0) + self.varisler.get('nine_baba', 0)
        if nine_toplam > 0 and self.varisler.get('anne', 0) == 0: # Ekstra kontrol
            if self.varisler.get('nine_anne', 0) > 0 and self.varisler.get('nine_baba', 0) > 0:
                self.paylar['nine_anne'] = Fraction(1, 12)
                self.paylar['nine_baba'] = Fraction(1, 12)
                self.log("Nineler: 1/6'yı paylaştı.")
            else:
                aktif_nine = 'nine_anne' if self.varisler.get('nine_anne') else 'nine_baba'
                self.paylar[aktif_nine] = Fraction(1, 6)
                self.log("Nine: 1/6 aldı.")

        # Anne Bir Kardeş
        if self.varisler.get('kardes_anne', 0) > 0:
             # Hacb kontrolü yukarıda yapılmıştı
             self.paylar['kardes_anne'] = Fraction(1, 6) if self.varisler['kardes_anne'] == 1 else Fraction(1, 3)

        # --- 3. ADIM: AVL (PAYDA ARTIŞI) ---
        toplam_farz = sum(self.paylar.values())
        if toplam_farz > 1:
            self.log(f"AVL: Paylar toplamı ({toplam_farz}) > 1. Orantı kuruldu.")
            for k in self.paylar: self.paylar[k] /= toplam_farz
            toplam_farz = 1

        # --- 4. ADIM: ASABE ---
        kalan = 1 - toplam_farz
        asabe_bulundu = False
        
        if kalan > 0:
            # Sınıf 1: Oğul
            if self.varisler.get('ogul', 0) > 0:
                self.asabe_paylastir(['ogul', 'kiz'], kalan, 2, 1); asabe_bulundu = True
                self.log(f"ASABE: Oğul (ve varsa Kız) kalanı aldı: {kalan}")
            elif self.varisler.get('ogul_oglu', 0) > 0:
                self.asabe_paylastir(['ogul_oglu', 'ogul_kizi'], kalan, 2, 1); asabe_bulundu = True
            
            # Sınıf 2: Baba/Dede
            elif not asabe_bulundu and self.varisler.get('baba', 0) > 0:
                self.paylar['baba'] = self.paylar.get('baba', 0) + kalan; asabe_bulundu = True
                self.log("ASABE: Baba kalanı da aldı.")
            elif not asabe_bulundu and self.varisler.get('dede', 0) > 0:
                self.paylar['dede'] = self.paylar.get('dede', 0) + kalan; asabe_bulundu = True

            # Sınıf 3: Kardeşler
            elif not asabe_bulundu:
                if self.varisler.get('erkek_kardes_oz', 0) > 0:
                    self.asabe_paylastir(['erkek_kardes_oz', 'kiz_kardes_oz'], kalan, 2, 1); asabe_bulundu = True
                    self.log("ASABE: Öz Kardeşler kalanı aldı.")
                elif self.varisler.get('erkek_kardes_baba', 0) > 0:
                    self.asabe_paylastir(['erkek_kardes_baba', 'kiz_kardes_baba'], kalan, 2, 1); asabe_bulundu = True
                # Maal Gayr (Kızlarla Kardeş)
                elif (self.varisler.get('kiz', 0) > 0 or self.varisler.get('ogul_kizi',0)>0):
                    if self.varisler.get('kiz_kardes_oz', 0) > 0:
                        self.paylar['kiz_kardes_oz'] = kalan; asabe_bulundu = True
                        self.log("ASABE: Kızlarla beraber Kız Kardeş asabe oldu.")
                    elif self.varisler.get('kiz_kardes_baba', 0) > 0:
                        self.paylar['kiz_kardes_baba'] = kalan; asabe_bulundu = True

            # Sınıf 4: Amcalar
            elif not asabe_bulundu:
                if self.varisler.get('amca', 0) > 0: self.paylar['amca'] = kalan; asabe_bulundu = True
                elif self.varisler.get('amca_oglu', 0) > 0: self.paylar['amca_oglu'] = kalan; asabe_bulundu = True

        # --- 5. ADIM: RED ---
        if kalan > 0 and not asabe_bulundu:
            red_alicilar = [k for k in self.paylar if k not in ['koca', 'kari'] and self.paylar[k] > 0]
            if red_alicilar:
                toplam_pay = sum(self.paylar[k] for k in red_alicilar)
                self.log(f"RED: Kalan {kalan}, eşler hariç dağıtıldı.")
                for k in red_alicilar:
                    self.paylar[k] += (self.paylar[k] / toplam_pay) * kalan

    def asabe_paylastir(self, anahtarlar, miktar, oran_erkek, oran_kiz):
        e_key, k_key = anahtarlar
        e_sayi = self.varisler.get(e_key, 0)
        k_sayi = self.varisler.get(k_key, 0)
        toplam_hisse = (e_sayi * oran_erkek) + (k_sayi * oran_kiz)
        birim = miktar / toplam_hisse
        if e_sayi > 0: self.paylar[e_key] = birim * oran_erkek * e_sayi
        if k_sayi > 0: self.paylar[k_key] = birim * oran_kiz * k_sayi
        self.asabe_kim = e_key

    def sonuclari_getir(self):
        return self.paylar, self.logs

# =============================================================================
# 2. BÖLÜM: MODERN KOYU ARAYÜZ (CustomTkinter)
# =============================================================================

# Tema Ayarları
ctk.set_appearance_mode("Dark")  # Koyu mod
ctk.set_default_color_theme("dark-blue")  # Mavi vurgular

class ModernSayac(ctk.CTkFrame):
    """Girdi için özel +/- butonu olan bileşen"""
    def __init__(self, master, label_text, variable):
        super().__init__(master, fg_color="transparent")
        self.variable = variable
        
        # Etiket
        self.lbl = ctk.CTkLabel(self, text=label_text, font=("Roboto Medium", 13), width=120, anchor="w")
        self.lbl.pack(side="left", padx=(0, 10))
        
        # Eksi Butonu
        self.btn_minus = ctk.CTkButton(self, text="-", width=30, height=30, 
                                       fg_color="#3a3a3a", hover_color="#c0392b",
                                       command=self.azalt)
        self.btn_minus.pack(side="left")
        
        # Değer Göstergesi
        self.ent_val = ctk.CTkEntry(self, textvariable=self.variable, width=40, justify="center", 
                                    font=("Roboto", 14, "bold"), fg_color="transparent", border_width=0)
        self.ent_val.pack(side="left", padx=5)
        
        # Artı Butonu
        self.btn_plus = ctk.CTkButton(self, text="+", width=30, height=30, 
                                      fg_color="#3a3a3a", hover_color="#27ae60",
                                      command=self.artir)
        self.btn_plus.pack(side="left")

    def azalt(self):
        try:
            val = int(self.variable.get())
            if val > 0: self.variable.set(str(val - 1))
        except: self.variable.set("0")

    def artir(self):
        try:
            val = int(self.variable.get())
            self.variable.set(str(val + 1))
        except: self.variable.set("0")

class ModernMirasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("Sirâciyye Miras Hesaplayıcı Pro")
        self.geometry("1100x750")
        
        self.motor = SiraciyyeMotoru()
        self.girdi_vars = {}

        # --- ANA DÜZEN (Grid) ---
        self.grid_columnconfigure(0, weight=1) # Sol Panel (Girdiler)
        self.grid_columnconfigure(1, weight=2) # Sağ Panel (Sonuçlar)
        self.grid_rowconfigure(0, weight=1)

        # === SOL PANEL (GİRDİLER) ===
        self.sol_panel = ctk.CTkScrollableFrame(self, label_text="VARİS BİLGİLERİ", label_font=("Roboto", 16, "bold"))
        self.sol_panel.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # Varis Grupları
        self.grup_olustur("EŞLER", [('koca', 'Koca'), ('kari', 'Karı')])
        self.grup_olustur("FÜRÛ (ALT SOY)", [('ogul', 'Oğul'), ('kiz', 'Kız'), ('ogul_oglu', 'Oğlun Oğlu'), ('ogul_kizi', 'Oğlun Kızı')])
        self.grup_olustur("USÛL (ÜST SOY)", [('baba', 'Baba'), ('anne', 'Anne'), ('dede', 'Dede (Baba T.)'), ('nine_anne', 'Nine (Anne T.)'), ('nine_baba', 'Nine (Baba T.)')])
        self.grup_olustur("KARDEŞLER & AMCALAR", [('erkek_kardes_oz', 'Öz Erkek Kar.'), ('kiz_kardes_oz', 'Öz Kız Kar.'), ('erkek_kardes_baba', 'Baba Bir Erk.K.'), ('kiz_kardes_baba', 'Baba Bir Kız K.'), ('kardes_anne', 'Anne Bir Kar.'), ('amca', 'Amca (Öz)'), ('amca_oglu', 'Amca Oğlu')])

        # Hesapla ve Temizle Butonları
        self.btn_frame = ctk.CTkFrame(self.sol_panel, fg_color="transparent")
        self.btn_frame.pack(pady=20, fill="x")

        self.btn_hesapla = ctk.CTkButton(self.btn_frame, text="HESAPLA", height=40, 
                                         font=("Roboto", 15, "bold"), fg_color="#2ecc71", hover_color="#27ae60",
                                         text_color="white", command=self.hesapla)
        self.btn_hesapla.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_reset = ctk.CTkButton(self.btn_frame, text="SIFIRLA", height=40, 
                                       font=("Roboto", 15, "bold"), fg_color="#e74c3c", hover_color="#c0392b",
                                       command=self.sifirla)
        self.btn_reset.pack(side="right", expand=True, fill="x", padx=5)

        # === SAĞ PANEL (SONUÇLAR) ===
        self.sag_panel = ctk.CTkFrame(self)
        self.sag_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.sag_panel.grid_rowconfigure(1, weight=1)
        self.sag_panel.grid_columnconfigure(0, weight=1)

        # Başlık
        self.lbl_sonuc_baslik = ctk.CTkLabel(self.sag_panel, text="MİRAS DAĞITIM RAPORU", 
                                             font=("Roboto", 20, "bold"), text_color="#3498db")
        self.lbl_sonuc_baslik.grid(row=0, column=0, pady=15)

        # Sonuç Metin Alanı
        self.txt_sonuc = ctk.CTkTextbox(self.sag_panel, font=("Consolas", 12), activate_scrollbars=True)
        self.txt_sonuc.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_sonuc.configure(state="disabled")

    def grup_olustur(self, baslik, varisler):
        """Bir grup için çerçeve ve girdiler oluşturur"""
        frame = ctk.CTkFrame(self.sol_panel)
        frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(frame, text=baslik, font=("Roboto", 12, "bold"), text_color="#bdc3c7").pack(anchor="w", padx=10, pady=5)
        
        for key, label in varisler:
            var = ctk.StringVar(value="0")
            self.girdi_vars[key] = var
            sayac = ModernSayac(frame, label, var)
            sayac.pack(fill="x", padx=10, pady=2)

    def sifirla(self):
        for var in self.girdi_vars.values():
            var.set("0")
        self.txt_sonuc.configure(state="normal")
        self.txt_sonuc.delete("1.0", "end")
        self.txt_sonuc.configure(state="disabled")

    def hesapla(self):
        # Girdileri al
        girdiler = {}
        try:
            for k, var in self.girdi_vars.items():
                val = int(var.get())
                if val < 0: raise ValueError
                girdiler[k] = val
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayı giriniz.")
            return

        if girdiler['koca'] > 0 and girdiler['kari'] > 0:
            messagebox.showwarning("Mantık Hatası", "Hem Koca hem Karı aynı anda mirasçı olamaz.")
            return

        # Hesapla
        self.motor.varis_yukle(girdiler)
        self.motor.hesapla()
        paylar, logs = self.motor.sonuclari_getir()

        # Sonuç Yazdır
        self.txt_sonuc.configure(state="normal")
        self.txt_sonuc.delete("1.0", "end")
        
        # 1. Bölüm: Adımlar
        self.txt_sonuc.insert("end", "=== HESAPLAMA MANTIĞI VE DELİLLER ===\n\n")
        if not logs:
            self.txt_sonuc.insert("end", "Herhangi bir varis girilmedi veya miras engeli oluştu.\n")
        for log in logs:
            self.txt_sonuc.insert("end", f"• {log}\n")

        # 2. Bölüm: Tablo
        self.txt_sonuc.insert("end", "\n\n" + "="*55 + "\n")
        self.txt_sonuc.insert("end", f"{'VARİS':<20} {'ADET':<8} {'HİSSE':<15} {'PAY (%)':<10}\n")
        self.txt_sonuc.insert("end", "="*55 + "\n")

        toplam_oran = 0.0
        
        # Etiket eşleşmesi için ters sözlük
        etiketler = {}
        for grup in [('koca', 'Koca'), ('kari', 'Karı'), ('ogul', 'Oğul'), ('kiz', 'Kız'),
                     ('baba', 'Baba'), ('anne', 'Anne'), ('dede', 'Dede'), ('nine_anne', 'Nine (Anne)'),
                     ('nine_baba', 'Nine (Baba)'), ('erkek_kardes_oz', 'Öz Erk. Kar.'),
                     ('kiz_kardes_oz', 'Öz Kız Kar.'), ('amca', 'Amca'), ('amca_oglu', 'Amca Oğlu'),
                     ('ogul_oglu', 'Oğlun Oğlu'), ('ogul_kizi', 'Oğlun Kızı'),
                     ('erkek_kardes_baba', 'Baba Bir Erk.K.'), ('kiz_kardes_baba', 'Baba Bir Kız K.'),
                     ('kardes_anne', 'Anne Bir Kar.')]:
            etiketler[grup[0]] = grup[1]

        for k, pay in paylar.items():
            if pay > 0:
                adet = girdiler.get(k, 1) # Nine ortak paylasımında adet 1 gelebilir
                yuzde = float(pay) * 100
                toplam_oran += yuzde
                ad = etiketler.get(k, k)
                self.txt_sonuc.insert("end", f"{ad:<20} {adet:<8} {str(pay):<15} %{yuzde:.2f}\n")

        self.txt_sonuc.insert("end", "-"*55 + "\n")
        self.txt_sonuc.insert("end", f"{'TOPLAM':<45} %{toplam_oran:.2f}\n")
        
        self.txt_sonuc.configure(state="disabled")

if __name__ == "__main__":
    app = ModernMirasApp()
    app.mainloop()