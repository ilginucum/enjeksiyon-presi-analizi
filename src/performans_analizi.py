"""
Performans Analizi Modülü
Bu modül makine performans metriklerini hesaplar ve raporlar.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PerformansAnalizci:
    """
    Makine performans analizlerini gerçekleştiren sınıf
    """
    
    def __init__(self, df):
        """
        Args:
            df (pd.DataFrame): Analiz edilecek DataFrame
        """
        self.df = df.copy()
        self.performans_raporu = {}
        
    def cevrim_suresi_analizi(self):
        """
        Çevrim süresi (cycle time) analizi yapar
        Çevrim süresi = Bir ürün üretiminin toplam süresi
        """
        print("\n" + "="*70)
        print("ÇEVRİM SÜRESİ ANALİZİ")
        print("="*70)
        
        # Toplam çevrim süresi tahmini (dolum + basınç yükselme + soğuma)
        # Not: Soğuma süresi yok, sadece dolum ve basınç yükselme var
        self.df['TOPLAM_CEVRIM'] = (self.df['KALIP DOLUM ZAMANI'] + 
                                     self.df['3. FAZ BASINC YÜKSELME ZAMANI'])
        
        ortalama_cevrim = self.df['TOPLAM_CEVRIM'].mean()
        min_cevrim = self.df['TOPLAM_CEVRIM'].min()
        max_cevrim = self.df['TOPLAM_CEVRIM'].max()
        std_cevrim = self.df['TOPLAM_CEVRIM'].std()
        
        print(f"\n📊 Çevrim Süresi İstatistikleri:")
        print(f"   Ortalama: {ortalama_cevrim:.0f} ms ({ortalama_cevrim/1000:.2f} saniye)")
        print(f"   En Hızlı: {min_cevrim:.0f} ms ({min_cevrim/1000:.2f} saniye)")
        print(f"   En Yavaş: {max_cevrim:.0f} ms ({max_cevrim/1000:.2f} saniye)")
        print(f"   Std Sapma: {std_cevrim:.0f} ms")
        
        # Hedef çevrim süresi (ideal: 1.5 saniye)
        hedef_cevrim = 1500  # ms
        
        hedefin_altinda = (self.df['TOPLAM_CEVRIM'] <= hedef_cevrim).sum()
        hedefin_ustunde = (self.df['TOPLAM_CEVRIM'] > hedef_cevrim).sum()
        
        print(f"\n🎯 Hedef Çevrim Süresi: {hedef_cevrim} ms")
        print(f"   Hedefin Altında: {hedefin_altinda} adet ({hedefin_altinda/len(self.df)*100:.1f}%)")
        print(f"   Hedefin Üstünde: {hedefin_ustunde} adet ({hedefin_ustunde/len(self.df)*100:.1f}%)")
        
        # Saatlik üretim kapasitesi
        saniyede_uretim = 1000 / ortalama_cevrim  # ürün/saniye
        saatte_uretim = saniyede_uretim * 3600  # ürün/saat
        
        print(f"\n⚙️ Üretim Kapasitesi:")
        print(f"   Teorik: {saatte_uretim:.0f} ürün/saat")
        print(f"   Günlük (24 saat): {saatte_uretim*24:.0f} ürün")
        
        self.performans_raporu['cevrim_suresi'] = {
            'ortalama': ortalama_cevrim,
            'min': min_cevrim,
            'max': max_cevrim,
            'hedef_altinda_oran': hedefin_altinda/len(self.df)*100,
            'saatlik_kapasite': saatte_uretim
        }
        
        return self.df
    
    def verimlilik_orani_hesapla(self):
        """
        Makine verimlilik oranlarını hesaplar
        """
        print("\n" + "="*70)
        print("VERİMLİLİK ORANI ANALİZİ")
        print("="*70)
        
        # Toplam üretim süresi (7 gün)
        baslangic = self.df['TARİH'].min()
        bitis = self.df['TARİH'].max()
        toplam_gun = (bitis - baslangic).days + 1
        toplam_saat = toplam_gun * 24
        
        print(f"\n📅 Analiz Dönemi:")
        print(f"   Başlangıç: {baslangic.date()}")
        print(f"   Bitiş: {bitis.date()}")
        print(f"   Toplam Gün: {toplam_gun} gün")
        print(f"   Toplam Saat: {toplam_saat} saat")
        
        # Gerçek üretim
        gercek_uretim = len(self.df)
        
        # Teorik üretim (eğer makine hiç durmadan çalışsaydı)
        ortalama_cevrim_saniye = self.df['TOPLAM_CEVRIM'].mean() / 1000
        teorik_uretim = (toplam_saat * 3600) / ortalama_cevrim_saniye
        
        # Verimlilik oranı
        verimlilik = (gercek_uretim / teorik_uretim) * 100
        
        print(f"\n📊 Üretim Karşılaştırması:")
        print(f"   Gerçek Üretim: {gercek_uretim} ürün")
        print(f"   Teorik Üretim: {teorik_uretim:.0f} ürün")
        print(f"   Verimlilik Oranı: {verimlilik:.1f}%")
        
        if verimlilik < 50:
            print(f"\n   🔴 DİKKAT: Verimlilik çok düşük! Makine çok fazla duruyor.")
        elif verimlilik < 70:
            print(f"\n   🟠 UYARI: Verimlilik ortalamanın altında.")
        else:
            print(f"\n   ✅ İYİ: Verimlilik kabul edilebilir seviyede.")
        
        # Günlük ortalama üretim
        gunluk_uretim = self.df.groupby(self.df['TARİH'].dt.date).size()
        
        print(f"\n📈 Günlük Üretim:")
        print(f"   Ortalama: {gunluk_uretim.mean():.0f} ürün/gün")
        print(f"   En Az: {gunluk_uretim.min()} ürün")
        print(f"   En Çok: {gunluk_uretim.max()} ürün")
        
        self.performans_raporu['verimlilik'] = {
            'verimlilik_orani': verimlilik,
            'gercek_uretim': gercek_uretim,
            'teorik_uretim': teorik_uretim,
            'gunluk_ortalama': gunluk_uretim.mean()
        }
        
        return gunluk_uretim
    
    def kalite_metrikleri(self):
        """
        Kalite metriklerini hesaplar
        """
        print("\n" + "="*70)
        print("KALİTE METRİKLERİ ANALİZİ")
        print("="*70)
        
        # Anomali oranları (kalite sorunları)
        toplam_uretim = len(self.df)
        
        # Basınç anomalileri
        Q1_basinc = self.df['PİSTON SÜRTÜNME BASINCI'].quantile(0.25)
        Q3_basinc = self.df['PİSTON SÜRTÜNME BASINCI'].quantile(0.75)
        IQR_basinc = Q3_basinc - Q1_basinc
        basinc_anomali = ((self.df['PİSTON SÜRTÜNME BASINCI'] < Q1_basinc - 1.5*IQR_basinc) | 
                         (self.df['PİSTON SÜRTÜNME BASINCI'] > Q3_basinc + 1.5*IQR_basinc)).sum()
        
        # Dolum anomalileri
        Q1_dolum = self.df['KALIP DOLUM ZAMANI'].quantile(0.25)
        Q3_dolum = self.df['KALIP DOLUM ZAMANI'].quantile(0.75)
        IQR_dolum = Q3_dolum - Q1_dolum
        dolum_anomali = ((self.df['KALIP DOLUM ZAMANI'] < Q1_dolum - 1.5*IQR_dolum) | 
                        (self.df['KALIP DOLUM ZAMANI'] > Q3_dolum + 1.5*IQR_dolum)).sum()
        
        # Toplam kalite sorunlu ürün
        kalite_sorunlu = basinc_anomali + dolum_anomali
        
        # Kalite oranı
        kalite_orani = ((toplam_uretim - kalite_sorunlu) / toplam_uretim) * 100
        
        print(f"\n📊 Kalite Durumu:")
        print(f"   Toplam Üretim: {toplam_uretim} ürün")
        print(f"   Kalite Sorunlu: {kalite_sorunlu} ürün")
        print(f"   Kalite Oranı: {kalite_orani:.1f}%")
        
        print(f"\n🔍 Sorun Dağılımı:")
        print(f"   Basınç Problemi: {basinc_anomali} ürün ({basinc_anomali/toplam_uretim*100:.1f}%)")
        print(f"   Dolum Problemi: {dolum_anomali} ürün ({dolum_anomali/toplam_uretim*100:.1f}%)")
        
        # Kabul edilebilirlik
        if kalite_orani >= 95:
            print(f"\n   ✅ MÜKEMMEL: Kalite hedefine ulaşıldı (>95%)")
        elif kalite_orani >= 90:
            print(f"\n   ✅ İYİ: Kabul edilebilir kalite seviyesi (90-95%)")
        elif kalite_orani >= 85:
            print(f"\n   🟠 ORTA: İyileştirme gerekli (85-90%)")
        else:
            print(f"\n   🔴 DÜŞÜK: Acil iyileştirme gerekli (<85%)")
        
        self.performans_raporu['kalite'] = {
            'kalite_orani': kalite_orani,
            'sorunlu_urun': kalite_sorunlu,
            'basinc_problemi': basinc_anomali,
            'dolum_problemi': dolum_anomali
        }
        
        return kalite_orani
    
    def makine_saglik_skoru(self):
        """
        Makinenin genel sağlık skorunu hesaplar (0-100)
        """
        print("\n" + "="*70)
        print("MAKİNE SAĞLIK SKORU")
        print("="*70)
        
        # Farklı metriklerin skorları
        
        # 1. Çevrim Süresi Skoru (25 puan)
        hedef_cevrim = 1500
        ortalama_cevrim = self.df['TOPLAM_CEVRIM'].mean()
        cevrim_skoru = max(0, 25 - ((ortalama_cevrim - hedef_cevrim) / hedef_cevrim * 25))
        
        # 2. Anomali Skoru (25 puan)
        anomali_orani = len(self.df[self.df['TOPLAM_CEVRIM'] > 2000]) / len(self.df) * 100
        anomali_skoru = max(0, 25 - anomali_orani)
        
        # 3. Verimlilik Skoru (25 puan)
        verimlilik_orani = self.performans_raporu['verimlilik']['verimlilik_orani']
        verimlilik_skoru = (verimlilik_orani / 100) * 25
        
        # 4. Kalite Skoru (25 puan)
        kalite_orani = self.performans_raporu['kalite']['kalite_orani']
        kalite_skoru = (kalite_orani / 100) * 25
        
        # Toplam skor
        toplam_skor = cevrim_skoru + anomali_skoru + verimlilik_skoru + kalite_skoru
        
        print(f"\n📊 Skor Detayları:")
        print(f"   Çevrim Süresi: {cevrim_skoru:.1f}/25")
        print(f"   Anomali Kontrolü: {anomali_skoru:.1f}/25")
        print(f"   Verimlilik: {verimlilik_skoru:.1f}/25")
        print(f"   Kalite: {kalite_skoru:.1f}/25")
        print(f"   " + "="*40)
        print(f"   TOPLAM SKOR: {toplam_skor:.1f}/100")
        
        # Değerlendirme
        if toplam_skor >= 85:
            durum = "MÜKEMMEL ✅"
            renk = "🟢"
        elif toplam_skor >= 70:
            durum = "İYİ ✅"
            renk = "🟢"
        elif toplam_skor >= 50:
            durum = "ORTA 🟠"
            renk = "🟠"
        else:
            durum = "KÖTÜ 🔴"
            renk = "🔴"
        
        print(f"\n{renk} Makine Durumu: {durum}")
        
        self.performans_raporu['saglik_skoru'] = {
            'toplam': toplam_skor,
            'cevrim': cevrim_skoru,
            'anomali': anomali_skoru,
            'verimlilik': verimlilik_skoru,
            'kalite': kalite_skoru,
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
        
        # Basınç kontrolleri
        ortalama_basinc = self.df['PİSTON SÜRTÜNME BASINCI'].mean()
        if ortalama_basinc > 6.0:
            oneriler.append({
                'oncelik': 'YÜKSEK',
                'kategori': 'Hidrolik Sistem',
                'sorun': f'Ortalama piston basıncı yüksek ({ortalama_basinc:.2f} bar)',
                'oneri': 'Hidrolik sistem bakımı, yağ değişimi ve pompa kontrolü yapılmalı',
                'sure': '4-6 saat'
            })
        
        # Çevrim süresi kontrolleri
        ortalama_cevrim = self.df['TOPLAM_CEVRIM'].mean()
        if ortalama_cevrim > 1800:
            oneriler.append({
                'oncelik': 'ORTA',
                'kategori': 'Performans',
                'sorun': f'Çevrim süresi hedefin üstünde ({ortalama_cevrim:.0f} ms)',
                'oneri': 'Kalıp sıcaklığı ayarları ve enjeksiyon hızı optimize edilmeli',
                'sure': '2-3 saat'
            })
        
        # Anomali kontrolleri
        basinc_yükselme_sorunlu = (self.df['3. FAZ BASINC YÜKSELME ZAMANI'] > 1000).sum()
        if basinc_yükselme_sorunlu > 50:
            oneriler.append({
                'oncelik': 'YÜKSEK',
                'kategori': 'Valf Sistemi',
                'sorun': f'{basinc_yükselme_sorunlu} adet basınç yükselme problemi',
                'oneri': 'Valf sistemi kontrolü ve temizliği acil yapılmalı',
                'sure': '3-4 saat'
            })
        
        # Verimlilik kontrolleri
        verimlilik = self.performans_raporu['verimlilik']['verimlilik_orani']
        if verimlilik < 60:
            oneriler.append({
                'oncelik': 'ORTA',
                'kategori': 'Üretim Planlaması',
                'sorun': f'Verimlilik düşük (%{verimlilik:.1f})',
                'oneri': 'Duruş sürelerinin analizi ve üretim planlamasının optimizasyonu',
                'sure': '1-2 gün (analiz)'
            })
        
        # Kalite kontrolleri
        kalite_orani = self.performans_raporu['kalite']['kalite_orani']
        if kalite_orani < 90:
            oneriler.append({
                'oncelik': 'YÜKSEK',
                'kategori': 'Kalite Kontrol',
                'sorun': f'Kalite oranı hedefin altında (%{kalite_orani:.1f})',
                'oneri': 'Anomali tespit edilen ürünlerin detaylı incelenmesi ve kalıp bakımı',
                'sure': '4-6 saat'
            })
        
        # Önerileri yazdır
        if oneriler:
            print(f"\n⚠️  Toplam {len(oneriler)} öneri tespit edildi:\n")
            
            for i, oneri in enumerate(oneriler, 1):
                oncelik_emoji = "🔴" if oneri['oncelik'] == 'YÜKSEK' else "🟠"
                print(f"{i}. {oncelik_emoji} [{oneri['oncelik']}] {oneri['kategori']}")
                print(f"   Sorun: {oneri['sorun']}")
                print(f"   Öneri: {oneri['oneri']}")
                print(f"   Tahmini Süre: {oneri['sure']}")
                print()
        else:
            print("\n✅ Hiçbir acil bakım önerisi yok! Makine iyi durumda.")
        
        self.performans_raporu['bakim_onerileri'] = oneriler
        
        return oneriler
    
    def tam_performans_analizi(self):
        """
        Tüm performans analizlerini sırayla çalıştırır
        """
        print("\n" + "⚙️"*35)
        print("PERFORMANS ANALİZİ BAŞLIYOR")
        print("⚙️"*35)
        
        # 1. Çevrim süresi
        self.cevrim_suresi_analizi()
        
        # 2. Verimlilik
        self.verimlilik_orani_hesapla()
        
        # 3. Kalite
        self.kalite_metrikleri()
        
        # 4. Sağlık skoru
        self.makine_saglik_skoru()
        
        # 5. Önleyici bakım
        self.onleyici_bakim_onerileri()
        
        print("\n" + "="*70)
        print("✅ PERFORMANS ANALİZİ TAMAMLANDI!")
        print("="*70)
        
        return self.performans_raporu


# Test için
if __name__ == "__main__":
    # Temizlenmiş veriyi yükle
    df = pd.read_csv('data/processed/enjeksiyon_temiz.csv')
    df['TARİH'] = pd.to_datetime(df['TARİH'])
    
    print(f"✅ Temizlenmiş veri yüklendi: {len(df)} satır")
    
    # Performans analizi yap
    analizci = PerformansAnalizci(df)
    rapor = analizci.tam_performans_analizi()
    
    # Raporu JSON olarak kaydet
    import json
    
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
    
    with open('reports/performans_raporu.json', 'w', encoding='utf-8') as f:
        json.dump(rapor_serializable, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Performans raporu 'reports/performans_raporu.json' olarak kaydedildi!")