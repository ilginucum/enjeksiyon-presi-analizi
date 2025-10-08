"""
Fırın Performans Analizi Modülü
Bu modül fırın performans metriklerini hesaplar ve raporlar.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class FirinPerformansAnalizci:
    """
    Fırın performans analizlerini gerçekleştiren sınıf
    """
    
    def __init__(self, df):
        """
        Args:
            df (pd.DataFrame): Analiz edilecek DataFrame
        """
        self.df = df.copy()
        self.performans_raporu = {}
        
    def sicaklik_kontrol_performansi(self):
        """
        Sıcaklık kontrol sisteminin performansını değerlendirir
        Her bölge için Set ISI vs Gerçek ISI farkını analiz eder
        """
        print("\n" + "="*70)
        print("SICAKLIK KONTROL PERFORMANSI")
        print("="*70)
        
        # Set-Gerçek ISI çiftleri
        set_gercek_pairs = [
            ('ÖN ISITMA', 'ÖN ISITMA SET ISI', 'ÖN ISITMA ISI'),
            ('CEH.1 ÜST1', 'CEH.1 ÜST1 SET ISI', 'CEH.1 ÜST1 ISI'),
            ('CEH.1 ÜST2', 'CEH.1 ÜST2 SET ISI', 'CEH.1 ÜST2  ISI'),
            ('CEH.1 ALT1', 'CEH.1 ALT1 SET ISI', 'CEH.1 ALT1 ISI'),
            ('CEH.2 ÜST1', 'CEH.2 ÜST1 SET ISI', 'CEH.2 ÜST1 ISI'),
            ('CEH.2 ÜST2', 'CEH.2 ÜST2 SET ISI', 'CEH.2 ÜST2 ISI'),
            ('CEH.2 ALT1', 'CEH.2 ALT1 SET ISI', 'CEH.2 ALT1 ISI'),
            ('CEH.2 ALT2', 'CEH.2 ALT2 SET ISI', 'CEH.2 ALT2 ISI'),
            ('CEH.3 ÜST1', 'CEH.3 ÜST1 SET ISI', 'CEH.3 ÜST1 ISI'),
            ('CEH.3 ÜST2', 'CEH.3 ÜST2 SET ISI', 'CEH.3 ÜST2 ISI'),
            ('CEH.3 ALT1', 'CEH.3 ALT1 SET ISI', 'CEH.3 ALT1 ISI'),
            ('CEH.3 ALT2', 'CEH.3 ALT2 SET ISI', 'CEH.3 ALT2 ISI'),
        ]
        
        kontrol_performanslari = {}
        toplam_basari = 0
        
        for bolge, set_col, gercek_col in set_gercek_pairs:
            # Fark hesapla
            fark = abs(self.df[set_col] - self.df[gercek_col])
            
            # Başarı oranı (±10°C tolerans)
            tolerans = 10
            basarili = (fark <= tolerans).sum()
            basari_orani = (basarili / len(self.df)) * 100
            
            # Ortalama fark
            ortalama_fark = fark.mean()
            max_fark = fark.max()
            
            kontrol_performanslari[bolge] = {
                'basari_orani': basari_orani,
                'ortalama_fark': ortalama_fark,
                'max_fark': max_fark
            }
            
            toplam_basari += basari_orani
            
            print(f"   • {bolge}: {basari_orani:.1f}% başarı oranı")
        
        ortalama_kontrol_basarisi = toplam_basari / len(set_gercek_pairs)
        
        print(f"\n📊 Ortalama Kontrol Başarısı: {ortalama_kontrol_basarisi:.1f}%")
        
        if ortalama_kontrol_basarisi >= 90:
            print("   ✅ MÜKEMMEL: Sıcaklık kontrol sistemi çok iyi çalışıyor")
        elif ortalama_kontrol_basarisi >= 75:
            print("   ✅ İYİ: Kabul edilebilir seviyede")
        elif ortalama_kontrol_basarisi >= 60:
            print("   🟠 ORTA: İyileştirme gerekli")
        else:
            print("   🔴 DÜŞÜK: Acil kalibrasyon gerekli")
        
        self.performans_raporu['sicaklik_kontrolu'] = {
            'ortalama_basari': ortalama_kontrol_basarisi,
            'bolge_detaylari': kontrol_performanslari
        }
        
        return ortalama_kontrol_basarisi
    
    def enerji_verimlilik_skoru(self):
        """
        Enerji verimliliği skorunu hesaplar
        """
        print("\n" + "="*70)
        print("ENERJİ VERİMLİLİK SKORU")
        print("="*70)
        
        # Güç kullanım yüzdeleri
        guc_cols = [col for col in self.df.columns if 'GÜÇ %' in col]
        
        if guc_cols:
            ortalama_guc_kullanimi = self.df[guc_cols].mean().mean()
            
            print(f"\n📊 Ortalama Güç Kullanımı: {ortalama_guc_kullanimi:.1f}%")
            
            # Verimlilik skoru (düşük güç = yüksek verimlilik)
            # İdeal: %50-70 arası
            if 50 <= ortalama_guc_kullanimi <= 70:
                verimlilik_skoru = 100
                durum = "OPTIMAL"
            elif ortalama_guc_kullanimi < 50:
                # Çok düşük güç - belki kapasite altı çalışıyor
                verimlilik_skoru = 70 + (ortalama_guc_kullanimi * 0.6)
                durum = "DÜŞÜK KAPASİTE"
            else:
                # Çok yüksek güç - enerji israfı
                verimlilik_skoru = max(0, 100 - (ortalama_guc_kullanimi - 70))
                durum = "YÜKSEK TÜKETİM"
            
            print(f"⚡ Enerji Verimlilik Skoru: {verimlilik_skoru:.1f}/100")
            print(f"   Durum: {durum}")
            
            # Günlük güç kullanımı trendi
            gunluk_guc = self.df.groupby(self.df['TARİH'].dt.date)[guc_cols].mean().mean(axis=1)
            trend_artis = gunluk_guc.iloc[-1] - gunluk_guc.iloc[0]
            
            if abs(trend_artis) < 5:
                print(f"   📈 Trend: Kararlı ({trend_artis:+.1f}%)")
            elif trend_artis > 0:
                print(f"   📈 Trend: Artış ({trend_artis:+.1f}%) - Dikkat!")
            else:
                print(f"   📈 Trend: Azalış ({trend_artis:+.1f}%) - İyi!")
            
        else:
            ortalama_guc_kullanimi = 0
            verimlilik_skoru = 0
            print("⚠️ Güç kullanım verisi bulunamadı!")
        
        self.performans_raporu['enerji_verimliligi'] = {
            'ortalama_guc': ortalama_guc_kullanimi,
            'verimlilik_skoru': verimlilik_skoru
        }
        
        return verimlilik_skoru
    
    def sogutma_sistemi_etkinligi(self):
        """
        Soğutma sistemi etkinliğini değerlendirir
        """
        print("\n" + "="*70)
        print("SOĞUTMA SİSTEMİ ETKİNLİĞİ")
        print("="*70)
        
        # Soğutma sıcaklıkları
        sogutma1 = self.df['SOĞUTMA1 ISI'].mean()
        sogutma2 = self.df['SOĞUTMA2 ISI'].mean()
        sogutma3 = self.df['SOĞUTMA3 ISI'].mean()
        
        # Soğutma farkı (ideal: 150-250°C arası)
        toplam_sogutma = sogutma1 - sogutma3
        
        print(f"\n📊 Ortalama Soğutma Farkı: {toplam_sogutma:.1f}°C")
        print(f"   (SOĞUTMA1 - SOĞUTMA3)")
        
        # Etkinlik skoru
        if 150 <= toplam_sogutma <= 250:
            etkinlik_skoru = 100
            durum = "OPTIMAL"
        elif toplam_sogutma < 150:
            etkinlik_skoru = (toplam_sogutma / 150) * 100
            durum = "DÜŞÜK - Soğutma yetersiz"
        else:
            etkinlik_skoru = max(0, 100 - ((toplam_sogutma - 250) / 5))
            durum = "YÜKSEK - Enerji israfı olabilir"
        
        print(f"❄️  Soğutma Etkinliği: {etkinlik_skoru:.1f}%")
        print(f"   Durum: {durum}")
        
        # Aşamalı soğutma kontrolü
        fark1_2 = sogutma1 - sogutma2
        fark2_3 = sogutma2 - sogutma3
        
        print(f"\n📉 Aşamalı Soğutma:")
        print(f"   1→2: {fark1_2:.1f}°C")
        print(f"   2→3: {fark2_3:.1f}°C")
        
        if abs(fark1_2 - fark2_3) < 50:
            print("   ✅ Dengeli soğutma")
        else:
            print("   ⚠️ Dengesiz soğutma - kontrol gerekli")
        
        self.performans_raporu['sogutma_etkinligi'] = {
            'toplam_sogutma': toplam_sogutma,
            'etkinlik_skoru': etkinlik_skoru,
            'asamali_sogutma': {
                'fark1_2': fark1_2,
                'fark2_3': fark2_3
            }
        }
        
        return etkinlik_skoru
    
    def ceh_dengesizlik_analizi(self):
        """
        Ceh bölmeleri arasındaki sıcaklık dengesizliğini analiz eder
        """
        print("\n" + "="*70)
        print("CEH DENGESİZLİK ANALİZİ")
        print("="*70)
        
        # Her ceh'in ortalama sıcaklığı
        ceh1_cols = [col for col in self.df.columns if 'CEH.1' in col and 'ISI' in col and 'SET' not in col]
        ceh2_cols = [col for col in self.df.columns if 'CEH.2' in col and 'ISI' in col and 'SET' not in col]
        ceh3_cols = [col for col in self.df.columns if 'CEH.3' in col and 'ISI' in col and 'SET' not in col]
        
        ceh1_ort = self.df[ceh1_cols].mean().mean()
        ceh2_ort = self.df[ceh2_cols].mean().mean()
        ceh3_ort = self.df[ceh3_cols].mean().mean()
        
        print(f"\n📊 Ceh Ortalama Sıcaklıkları:")
        print(f"   • CEH.1: {ceh1_ort:.1f}°C")
        print(f"   • CEH.2: {ceh2_ort:.1f}°C")
        print(f"   • CEH.3: {ceh3_ort:.1f}°C")
        
        # Maksimum fark
        ceh_sicakliklar = [ceh1_ort, ceh2_ort, ceh3_ort]
        max_fark = max(ceh_sicakliklar) - min(ceh_sicakliklar)
        
        print(f"\n   Maksimum Ceh Arası Fark: {max_fark:.1f}°C")
        
        # Denge skoru
        if max_fark < 50:
            denge_skoru = 100
            durum = "MÜKEMMEL - Dengeli"
        elif max_fark < 100:
            denge_skoru = 100 - ((max_fark - 50) * 2)
            durum = "İYİ"
        elif max_fark < 150:
            denge_skoru = 50 - ((max_fark - 100))
            durum = "ORTA - İyileştirme gerekli"
        else:
            denge_skoru = max(0, 50 - (max_fark - 150) * 0.5)
            durum = "DÜŞÜK - Acil müdahale"
        
        print(f"   Denge Skoru: {denge_skoru:.1f}/100")
        print(f"   Durum: {durum}")
        
        if max_fark >= 100:
            print(f"\n   ⚠️  UYARI: Ceh'ler arası büyük sıcaklık farkı!")
            print(f"   Öneri: Sıcaklık sensörleri kalibre edilmeli")
        
        self.performans_raporu['ceh_dengesizlik'] = {
            'ceh1_ortalama': ceh1_ort,
            'ceh2_ortalama': ceh2_ort,
            'ceh3_ortalama': ceh3_ort,
            'max_fark': max_fark,
            'denge_skoru': denge_skoru
        }
        
        return denge_skoru
    
    def operasyonel_verimlilik(self):
        """
        Operasyonel verimlilik analizi
        """
        print("\n" + "="*70)
        print("OPERASYONEL VERİMLİLİK")
        print("="*70)
        
        # Toplam analiz dönemi
        baslangic = self.df['TARİH'].min()
        bitis = self.df['TARİH'].max()
        toplam_gun = (bitis - baslangic).days + 1
        toplam_saat = toplam_gun * 24
        
        print(f"\n📅 Analiz Dönemi:")
        print(f"   Başlangıç: {baslangic.date()}")
        print(f"   Bitiş: {bitis.date()}")
        print(f"   Toplam: {toplam_gun} gün ({toplam_saat} saat)")
        
        # Kayıt sayısı analizi
        toplam_kayit = len(self.df)
        beklenen_kayit = toplam_saat * 20  # Saatte ~20 kayıt bekleniyor
        
        print(f"\n📊 Veri Kayıt Analizi:")
        print(f"   Gerçek Kayıt: {toplam_kayit:,}")
        print(f"   Beklenen Kayıt: {beklenen_kayit:,}")
        print(f"   Kayıt Oranı: {(toplam_kayit/beklenen_kayit)*100:.1f}%")
        
        # Günlük kayıt dağılımı
        gunluk_kayit = self.df.groupby(self.df['TARİH'].dt.date).size()
        
        print(f"\n📈 Günlük Veri Dağılımı:")
        print(f"   Ortalama: {gunluk_kayit.mean():.0f} kayıt/gün")
        print(f"   En Az: {gunluk_kayit.min()} kayıt")
        print(f"   En Çok: {gunluk_kayit.max()} kayıt")
        print(f"   Std Sapma: {gunluk_kayit.std():.0f}")
        
        # Tutarlılık skoru
        tutarlilik = (gunluk_kayit.std() / gunluk_kayit.mean()) * 100
        
        if tutarlilik < 20:
            tutarlilik_skoru = 100
            durum = "ÇOK TUTARLI"
        elif tutarlilik < 40:
            tutarlilik_skoru = 80
            durum = "TUTARLI"
        elif tutarlilik < 60:
            tutarlilik_skoru = 60
            durum = "ORTA"
        else:
            tutarlilik_skoru = 40
            durum = "TUTARSIZ"
        
        print(f"\n   Tutarlılık Skoru: {tutarlilik_skoru:.1f}/100 ({durum})")
        
        self.performans_raporu['operasyonel_verimlilik'] = {
            'toplam_gun': toplam_gun,
            'toplam_kayit': toplam_kayit,
            'gunluk_ortalama': gunluk_kayit.mean(),
            'tutarlilik_skoru': tutarlilik_skoru
        }
        
        return tutarlilik_skoru
    
    def genel_performans_skoru(self):
        """
        Fırının genel performans skorunu hesaplar (0-100)
        """
        print("\n" + "="*70)
        print("GENEL PERFORMANS SKORU")
        print("="*70)
        
        # Farklı metriklerin skorları ve ağırlıkları
        
        # 1. Sıcaklık Kontrolü (50% - en önemli)
        sicaklik_skoru = (self.performans_raporu['sicaklik_kontrolu']['ortalama_basari'] / 100) * 50
        
        # 2. Enerji Verimliliği (30%)
        enerji_skoru = (self.performans_raporu['enerji_verimliligi']['verimlilik_skoru'] / 100) * 30
        
        # 3. Soğutma Etkinliği (20%)
        sogutma_skoru = (self.performans_raporu['sogutma_etkinligi']['etkinlik_skoru'] / 100) * 20
        
        # Toplam skor
        toplam_skor = sicaklik_skoru + enerji_skoru + sogutma_skoru
        
        print(f"\n📊 Skor Detayları:")
        print(f"   Sıcaklık Kontrolü: {sicaklik_skoru:.1f}/50 (Ağırlık: %50)")
        print(f"   Enerji Verimliliği: {enerji_skoru:.1f}/30 (Ağırlık: %30)")
        print(f"   Soğutma Etkinliği: {sogutma_skoru:.1f}/20 (Ağırlık: %20)")
        print(f"   " + "="*50)
        print(f"   GENEL PERFORMANS: {toplam_skor:.1f}/100")
        
        # Değerlendirme
        if toplam_skor >= 90:
            durum = "MÜKEMMEL ✅"
            renk = "🟢"
        elif toplam_skor >= 75:
            durum = "İYİ ✅"
            renk = "🟢"
        elif toplam_skor >= 60:
            durum = "ORTA 🟠"
            renk = "🟠"
        else:
            durum = "DÜŞÜK 🔴"
            renk = "🔴"
        
        print(f"\n{renk} Fırın Durumu: {durum}")
        
        self.performans_raporu['genel_skor'] = {
            'toplam': toplam_skor,
            'sicaklik': sicaklik_skoru,
            'enerji': enerji_skoru,
            'sogutma': sogutma_skoru,
            'durum': durum
        }
        
        return toplam_skor
    
    def onleyici_bakim_onerileri(self):
        """
        Verilere dayalı önleyici bakım önerileri sunar
        """
        print("\n" + "="*70)
        print("ÖNLEYİCİ BAKIM ÖNERİLERİ")
        print("="*70)
        
        oneriler = []
        
        # Sıcaklık kontrol sorunları
        sicaklik_basari = self.performans_raporu['sicaklik_kontrolu']['ortalama_basari']
        if sicaklik_basari < 75:
            oneriler.append({
                'oncelik': 'YÜKSEK',
                'kategori': 'Sıcaklık Kontrolü',
                'sorun': f'Sıcaklık kontrol başarısı düşük (%{sicaklik_basari:.1f})',
                'oneri': 'Tüm sıcaklık sensörleri kalibre edilmeli ve kontrol sistemi gözden geçirilmeli',
                'sure': '6-8 saat'
            })
        
        # Ceh dengesizliği
        ceh_fark = self.performans_raporu['ceh_dengesizlik']['max_fark']
        if ceh_fark > 100:
            oneriler.append({
                'oncelik': 'YÜKSEK',
                'kategori': 'Ceh Dengesi',
                'sorun': f'Ceh bölmeleri arası büyük sıcaklık farkı ({ceh_fark:.1f}°C)',
                'oneri': 'Ceh bölmelerinin ısıtma elemanları ve sensörleri kontrol edilmeli',
                'sure': '4-6 saat'
            })
        
        # Enerji verimliliği
        enerji_skoru = self.performans_raporu['enerji_verimliligi']['verimlilik_skoru']
        ortalama_guc = self.performans_raporu['enerji_verimliligi']['ortalama_guc']
        
        if enerji_skoru < 70:
            if ortalama_guc > 70:
                oneriler.append({
                    'oncelik': 'ORTA',
                    'kategori': 'Enerji Verimliliği',
                    'sorun': f'Yüksek enerji tüketimi (%{ortalama_guc:.1f} ortalama güç)',
                    'oneri': 'Isıtma elemanlarının temizliği ve yalıtım kontrolü yapılmalı',
                    'sure': '3-4 saat'
                })
            else:
                oneriler.append({
                    'oncelik': 'DÜŞÜK',
                    'kategori': 'Kapasite Kullanımı',
                    'sorun': f'Düşük güç kullanımı (%{ortalama_guc:.1f})',
                    'oneri': 'Üretim kapasitesi değerlendirilmeli, fırın tam kapasite kullanılmıyor olabilir',
                    'sure': '2-3 saat (analiz)'
                })
        
        # Soğutma etkinliği
        sogutma_fark = self.performans_raporu['sogutma_etkinligi']['toplam_sogutma']
        if sogutma_fark < 150:
            oneriler.append({
                'oncelik': 'ORTA',
                'kategori': 'Soğutma Sistemi',
                'sorun': f'Soğutma etkinliği düşük ({sogutma_fark:.1f}°C)',
                'oneri': 'Soğutma fanları ve havalandırma sistemi kontrol edilmeli',
                'sure': '2-3 saat'
            })
        elif sogutma_fark > 250:
            oneriler.append({
                'oncelik': 'DÜŞÜK',
                'kategori': 'Soğutma Optimizasyonu',
                'sorun': f'Aşırı soğutma ({sogutma_fark:.1f}°C)',
                'oneri': 'Soğutma sistemi ayarları optimize edilebilir, enerji tasarrufu sağlanabilir',
                'sure': '1-2 saat'
            })
        
        # En kritik sorunlu bölgeler
        bolge_detaylari = self.performans_raporu['sicaklik_kontrolu']['bolge_detaylari']
        kritik_bolgeler = [bolge for bolge, veri in bolge_detaylari.items() 
                          if veri['basari_orani'] < 60]
        
        if kritik_bolgeler:
            oneriler.append({
                'oncelik': 'YÜKSEK',
                'kategori': 'Kritik Bölgeler',
                'sorun': f'{len(kritik_bolgeler)} bölgede kritik kontrol sorunu: {", ".join(kritik_bolgeler[:3])}',
                'oneri': 'Bu bölgelerin sensör ve ısıtıcıları acil kontrol edilmeli',
                'sure': '4-6 saat'
            })
        
        # Önerileri yazdır
        if oneriler:
            print(f"\n⚠️  Toplam {len(oneriler)} öneri tespit edildi:\n")
            
            for i, oneri in enumerate(oneriler, 1):
                oncelik_emoji = "🔴" if oneri['oncelik'] == 'YÜKSEK' else "🟠" if oneri['oncelik'] == 'ORTA' else "🟡"
                print(f"{i}. {oncelik_emoji} [{oneri['oncelik']}] {oneri['kategori']}")
                print(f"   Sorun: {oneri['sorun']}")
                print(f"   Öneri: {oneri['oneri']}")
                print(f"   Tahmini Süre: {oneri['sure']}")
                print()
        else:
            print("\n✅ Hiçbir acil bakım önerisi yok! Fırın iyi durumda.")
        
        self.performans_raporu['bakim_onerileri'] = oneriler
        
        return oneriler
    
    def tam_performans_analizi(self):
        """
        Tüm performans analizlerini sırayla çalıştırır
        """
        print("\n" + "⚙️"*35)
        print("FIRIN PERFORMANS ANALİZİ BAŞLIYOR")
        print("⚙️"*35)
        
        # 1. Sıcaklık kontrol performansı
        self.sicaklik_kontrol_performansi()
        
        # 2. Enerji verimliliği
        self.enerji_verimlilik_skoru()
        
        # 3. Soğutma sistemi
        self.sogutma_sistemi_etkinligi()
        
        # 4. Ceh dengesizliği
        self.ceh_dengesizlik_analizi()
        
        # 5. Operasyonel verimlilik
        self.operasyonel_verimlilik()
        
        # 6. Genel performans skoru
        self.genel_performans_skoru()
        
        # 7. Önleyici bakım önerileri
        self.onleyici_bakim_onerileri()
        
        print("\n" + "="*70)
        print("✅ PERFORMANS ANALİZİ TAMAMLANDI!")
        print("="*70)
        
        return self.performans_raporu


# Test için
if __name__ == "__main__":
    # Temizlenmiş veriyi yükle
    print("\n📂 Temizlenmiş fırın verisi yükleniyor...")
    df = pd.read_csv('data/processed/firin_temiz.csv')
    df['TARİH'] = pd.to_datetime(df['TARİH'])
    
    print(f"✅ Veri yüklendi: {len(df)} satır, {len(df.columns)} sütun")
    print(f"📅 Tarih aralığı: {df['TARİH'].min()} - {df['TARİH'].max()}")
    
    # Performans analizi yap
    analizci = FirinPerformansAnalizci(df)
    rapor = analizci.tam_performans_analizi()
    
    # Raporu JSON olarak kaydet
    # NumPy tiplerini Python tiplerine dönüştür
    def convert_to_serializable(obj):
        """NumPy ve pandas tiplerini JSON serileştirilebilir tiplere dönüştürür"""
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        return obj
    
    rapor_serializable = convert_to_serializable(rapor)
    
    with open('reports/firin_performans_raporu.json', 'w', encoding='utf-8') as f:
        json.dump(rapor_serializable, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Performans raporu 'reports/firin_performans_raporu.json' olarak kaydedildi!")
    
    # Özet rapor oluştur
    print("\n" + "="*70)
    print("📋 PERFORMANS RAPORU ÖZETİ")
    print("="*70)
    
    print(f"\n🎯 GENEL PERFORMANS: {rapor['genel_skor']['toplam']:.1f}/100")
    print(f"   Durum: {rapor['genel_skor']['durum']}")
    
    print(f"\n📊 DETAYLI SKORLAR:")
    print(f"   • Sıcaklık Kontrolü: {rapor['sicaklik_kontrolu']['ortalama_basari']:.1f}%")
    print(f"   • Enerji Verimliliği: {rapor['enerji_verimliligi']['verimlilik_skoru']:.1f}/100")
    print(f"   • Soğutma Etkinliği: {rapor['sogutma_etkinligi']['etkinlik_skoru']:.1f}%")
    print(f"   • Ceh Dengesi: {rapor['ceh_dengesizlik']['denge_skoru']:.1f}/100")
    
    print(f"\n⚠️  BAKIM ÖNERİLERİ: {len(rapor['bakim_onerileri'])} adet")
    
    if rapor['bakim_onerileri']:
        yuksek = sum(1 for o in rapor['bakim_onerileri'] if o['oncelik'] == 'YÜKSEK')
        orta = sum(1 for o in rapor['bakim_onerileri'] if o['oncelik'] == 'ORTA')
        dusuk = sum(1 for o in rapor['bakim_onerileri'] if o['oncelik'] == 'DÜŞÜK')
        
        print(f"   🔴 Yüksek Öncelikli: {yuksek}")
        print(f"   🟠 Orta Öncelikli: {orta}")
        print(f"   🟡 Düşük Öncelikli: {dusuk}")
    
    print(f"\n📈 OPERASYONEL VERİMLİLİK:")
    print(f"   • Toplam Analiz: {rapor['operasyonel_verimlilik']['toplam_gun']} gün")
    print(f"   • Toplam Kayıt: {rapor['operasyonel_verimlilik']['toplam_kayit']:,}")
    print(f"   • Günlük Ortalama: {rapor['operasyonel_verimlilik']['gunluk_ortalama']:.0f} kayıt")
    
    print("\n✨ Analiz tamamlandı!")
    print("💾 Detaylı rapor JSON dosyasında mevcut.")