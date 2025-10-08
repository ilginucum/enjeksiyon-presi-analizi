"""
Anomali Tespiti Modülü
Bu modül enjeksiyon presi verilerindeki anormal davranışları tespit eder.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AnomaliBulucu:
    """
    Anomali tespit işlemlerini gerçekleştiren sınıf
    """
    
    def __init__(self, df):
        """
        Args:
            df (pd.DataFrame): Temizlenmiş DataFrame
        """
        self.df = df.copy()
        self.anomaliler = {}
        
        # Grafik stilini ayarla
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def istatistiksel_anomali_bul(self, col_name, method='iqr', threshold=1.5):
        """
        İstatistiksel yöntemlerle anomali bulur
        
        Args:
            col_name (str): Sütun adı
            method (str): 'iqr' veya 'zscore'
            threshold (float): Eşik değeri
            
        Returns:
            pd.DataFrame: Anomali içeren satırlar
        """
        if col_name not in self.df.columns:
            return pd.DataFrame()
        
        if method == 'iqr':
            # IQR (Interquartile Range) Metodu
            Q1 = self.df[col_name].quantile(0.25)
            Q3 = self.df[col_name].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            anomali_mask = (self.df[col_name] < lower_bound) | (self.df[col_name] > upper_bound)
            
            print(f"\n📊 {col_name} - IQR Analizi:")
            print(f"   Alt Sınır: {lower_bound:.2f}")
            print(f"   Üst Sınır: {upper_bound:.2f}")
            print(f"   Q1 (25%): {Q1:.2f}, Q3 (75%): {Q3:.2f}")
            
        elif method == 'zscore':
            # Z-Score Metodu
            mean = self.df[col_name].mean()
            std = self.df[col_name].std()
            
            z_scores = np.abs((self.df[col_name] - mean) / std)
            anomali_mask = z_scores > threshold
            
            print(f"\n📊 {col_name} - Z-Score Analizi:")
            print(f"   Ortalama: {mean:.2f}")
            print(f"   Std. Sapma: {std:.2f}")
            print(f"   Eşik: ±{threshold} std")
        
        anomaliler = self.df[anomali_mask].copy()
        
        if len(anomaliler) > 0:
            print(f"   ⚠️  {len(anomaliler)} anomali tespit edildi ({len(anomaliler)/len(self.df)*100:.2f}%)")
            self.anomaliler[col_name] = anomaliler
        else:
            print(f"   ✅ Anomali bulunamadı")
        
        return anomaliler
    
    def surtuname_basinci_analizi(self):
        """
        Piston sürtünme basıncı anomalilerini analiz eder
        """
        print("\n" + "="*70)
        print("PİSTON SÜRTÜNME BASINCI ANOMALİ ANALİZİ")
        print("="*70)
        
        col = 'PİSTON SÜRTÜNME BASINCI'
        
        # İstatistikler
        print(f"\n📊 Temel İstatistikler:")
        print(f"   Ortalama: {self.df[col].mean():.2f} bar")
        print(f"   Medyan: {self.df[col].median():.2f} bar")
        print(f"   Min: {self.df[col].min():.2f} bar")
        print(f"   Max: {self.df[col].max():.2f} bar")
        print(f"   Std Sapma: {self.df[col].std():.2f} bar")
        
        # Anomali tespiti
        anomaliler = self.istatistiksel_anomali_bul(col, method='iqr', threshold=1.5)
        
        if len(anomaliler) > 0:
            print(f"\n⚠️  Anormal Basınç Değerleri:")
            print(f"   En Düşük Anormal: {anomaliler[col].min():.2f} bar")
            print(f"   En Yüksek Anormal: {anomaliler[col].max():.2f} bar")
            
            # Tarih bazlı analiz
            anomaliler_gunluk = anomaliler.groupby(anomaliler['TARİH'].dt.date).size()
            print(f"\n📅 En Çok Anomali Olan Günler:")
            print(anomaliler_gunluk.sort_values(ascending=False).head())
        
        return anomaliler
    
    def dolum_zamani_analizi(self):
        """
        Kalıp dolum zamanı anomalilerini analiz eder
        """
        print("\n" + "="*70)
        print("KALIP DOLUM ZAMANI ANOMALİ ANALİZİ")
        print("="*70)
        
        col = 'KALIP DOLUM ZAMANI'
        
        # İstatistikler
        print(f"\n📊 Temel İstatistikler:")
        print(f"   Ortalama: {self.df[col].mean():.0f} ms")
        print(f"   Medyan: {self.df[col].median():.0f} ms")
        print(f"   Min: {self.df[col].min():.0f} ms")
        print(f"   Max: {self.df[col].max():.0f} ms")
        print(f"   Std Sapma: {self.df[col].std():.0f} ms")
        
        # Anomali tespiti
        anomaliler = self.istatistiksel_anomali_bul(col, method='iqr', threshold=1.5)
        
        if len(anomaliler) > 0:
            print(f"\n⚠️  Anormal Dolum Süreleri:")
            print(f"   En Kısa Anormal: {anomaliler[col].min():.0f} ms")
            print(f"   En Uzun Anormal: {anomaliler[col].max():.0f} ms")
            
            # Çok uzun sürenler (performans problemi)
            cok_uzun = anomaliler[anomaliler[col] > 1200]
            if len(cok_uzun) > 0:
                print(f"\n🔴 KRİTİK: {len(cok_uzun)} adet 1200ms'den uzun dolum süresi!")
                print(f"   Bu ürünler kalite kontrolünden geçmeli!")
        
        return anomaliler
    
    def hiz_degisikligi_analizi(self):
        """
        Hız parametrelerindeki anomalileri analiz eder
        """
        print("\n" + "="*70)
        print("HIZ PARAMETRELERİ ANOMALİ ANALİZİ")
        print("="*70)
        
        # Birinci Faz Hızı
        print("\n🔹 BİRİNCİ FAZ HIZI:")
        anomaliler_faz1 = self.istatistiksel_anomali_bul('BİRİNCİ FAZ HIZI', method='iqr')
        
        # İkinci Faz Hızı
        print("\n🔹 İKİNCİ FAZ HIZI:")
        anomaliler_faz2 = self.istatistiksel_anomali_bul('İKİNCİ FAZ HIZI', method='iqr')
        
        # Hız oranı analizi (beklenmeyen hız değişimleri)
        if 'BİRİNCİ FAZ HIZI' in self.df.columns and 'İKİNCİ FAZ HIZI' in self.df.columns:
            self.df['HIZ_ORANI'] = self.df['İKİNCİ FAZ HIZI'] / self.df['BİRİNCİ FAZ HIZI']
            
            print(f"\n📊 Hız Oranı Analizi (Faz2/Faz1):")
            print(f"   Ortalama Oran: {self.df['HIZ_ORANI'].mean():.2f}x")
            print(f"   Min Oran: {self.df['HIZ_ORANI'].min():.2f}x")
            print(f"   Max Oran: {self.df['HIZ_ORANI'].max():.2f}x")
        
        return anomaliler_faz1, anomaliler_faz2
    
    def basinc_yükselme_analizi(self):
        """
        3. Faz basınç yükselme zamanı anomalilerini analiz eder
        """
        print("\n" + "="*70)
        print("3. FAZ BASINÇ YÜKSELME ZAMANI ANOMALİ ANALİZİ")
        print("="*70)
        
        col = '3. FAZ BASINC YÜKSELME ZAMANI'
        
        # İstatistikler
        print(f"\n📊 Temel İstatistikler:")
        print(f"   Ortalama: {self.df[col].mean():.0f} ms")
        print(f"   Medyan: {self.df[col].median():.0f} ms")
        print(f"   Min: {self.df[col].min():.0f} ms")
        print(f"   Max: {self.df[col].max():.0f} ms")
        
        # Anomali tespiti
        anomaliler = self.istatistiksel_anomali_bul(col, method='iqr', threshold=2.0)
        
        # Çok yüksek değerler (potansiyel arıza)
        cok_yuksek = self.df[self.df[col] > 1000]
        if len(cok_yuksek) > 0:
            print(f"\n🔴 UYARI: {len(cok_yuksek)} adet 1000ms'den uzun basınç yükselme zamanı!")
            print(f"   Bu MAKİNE ARIZASI göstergesi olabilir!")
            print(f"\n   Problemli Baskı Numaraları:")
            print(f"   {cok_yuksek['BASKI NO'].tolist()[:5]}...")
        
        return anomaliler
    
    def kalip_bazli_analiz(self):
        """
        Kalıp numarasına göre performans analizi yapar
        """
        print("\n" + "="*70)
        print("KALIP BAZLI PERFORMANS ANALİZİ")
        print("="*70)
        
        # Kalıp başına istatistikler
        kalip_stats = self.df.groupby('KALIP NO').agg({
            'KALIP DOLUM ZAMANI': ['mean', 'std', 'count'],
            'PİSTON SÜRTÜNME BASINCI': ['mean', 'std'],
            'SPESİFİK BASINÇ BAR': ['mean', 'std']
        }).round(2)
        
        print(f"\n📊 Kalıp Bazlı Ortalama Değerler:")
        print(kalip_stats)
        
        # En problemli kalıplar
        print(f"\n⚠️  En Uzun Dolum Süresi Olan Kalıplar:")
        en_yavas = self.df.groupby('KALIP NO')['KALIP DOLUM ZAMANI'].mean().sort_values(ascending=False).head()
        print(en_yavas)
        
        return kalip_stats
    
    def zaman_serisi_analizi(self):
        """
        Zamana göre anomali trendlerini analiz eder
        """
        print("\n" + "="*70)
        print("ZAMAN SERİSİ ANOMALİ ANALİZİ")
        print("="*70)
        
        # Günlük ortalamalar
        gunluk = self.df.groupby(self.df['TARİH'].dt.date).agg({
            'KALIP DOLUM ZAMANI': 'mean',
            'PİSTON SÜRTÜNME BASINCI': 'mean',
            'SPESİFİK BASINÇ BAR': 'mean'
        }).round(2)
        
        print(f"\n📅 Günlük Ortalama Değerler:")
        print(gunluk)
        
        # Trend analizi
        ilk_gun = gunluk.iloc[0]['KALIP DOLUM ZAMANI']
        son_gun = gunluk.iloc[-1]['KALIP DOLUM ZAMANI']
        degisim = ((son_gun - ilk_gun) / ilk_gun) * 100
        
        print(f"\n📈 Dolum Zamanı Trendi:")
        print(f"   İlk Gün Ort: {ilk_gun:.0f} ms")
        print(f"   Son Gün Ort: {son_gun:.0f} ms")
        print(f"   Değişim: {degisim:+.1f}%")
        
        if degisim > 10:
            print(f"   🔴 UYARI: Dolum süresi artıyor! Bakım gerekebilir!")
        elif degisim < -10:
            print(f"   ✅ İYİ: Dolum süresi iyileşiyor!")
        else:
            print(f"   ✅ NORMAL: Stabil performans")
        
        return gunluk
    
    def anomali_raporu_olustur(self):
        """
        Tüm anomali analizlerini birleştiren genel rapor
        """
        print("\n" + "🔴"*35)
        print("GENEL ANOMALİ RAPORU")
        print("🔴"*35)
        
        # Toplam anomali sayısı
        toplam_anomali = sum(len(v) for v in self.anomaliler.values())
        
        print(f"\n📊 ÖZET:")
        print(f"   Toplam Kayıt: {len(self.df)}")
        print(f"   Toplam Anomali: {toplam_anomali} ({toplam_anomali/len(self.df)*100:.2f}%)")
        print(f"   Anomali Bulunan Parametre Sayısı: {len(self.anomaliler)}")
        
        if self.anomaliler:
            print(f"\n⚠️  ANOMALİ DAĞILIMI:")
            for param, anomali_df in self.anomaliler.items():
                print(f"   • {param}: {len(anomali_df)} adet")
        
        # Kritik öneriler
        print(f"\n💡 ÖNERİLER:")
        
        # Dolum zamanı kontrolü
        if 'KALIP DOLUM ZAMANI' in self.anomaliler:
            uzun_dolum = len(self.anomaliler['KALIP DOLUM ZAMANI'])
            if uzun_dolum > 30:
                print(f"   🔴 {uzun_dolum} adet uzun dolum süresi tespit edildi!")
                print(f"      → Kalıp sıcaklığını kontrol edin")
                print(f"      → Malzeme akışkanlığını test edin")
        
        # Basınç kontrolü
        if 'PİSTON SÜRTÜNME BASINCI' in self.anomaliler:
            print(f"   🔴 Anormal piston basınçları mevcut!")
            print(f"      → Hidrolik sistem bakımı yapın")
            print(f"      → Yağ seviyesini kontrol edin")
        
        # Basınç yükselme zamanı
        if '3. FAZ BASINC YÜKSELME ZAMANI' in self.anomaliler:
            print(f"   🔴 Basınç yükselme problemleri var!")
            print(f"      → Acil makine bakımı gerekli!")
            print(f"      → Valf sistemi kontrol edilmeli")
        
        print(f"\n✅ Analiz tamamlandı!")
    
    def tam_analiz_yap(self):
        """
        Tüm anomali analizlerini sırayla çalıştırır
        """
        print("\n" + "🔍"*35)
        print("ANOMALİ TESPİT SÜRECİ BAŞLIYOR")
        print("🔍"*35)
        
        # 1. Sürtünme Basıncı
        self.surtuname_basinci_analizi()
        
        # 2. Dolum Zamanı
        self.dolum_zamani_analizi()
        
        # 3. Hız Değişiklikleri
        self.hiz_degisikligi_analizi()
        
        # 4. Basınç Yükselme
        self.basinc_yükselme_analizi()
        
        # 5. Kalıp Bazlı Analiz
        self.kalip_bazli_analiz()
        
        # 6. Zaman Serisi
        self.zaman_serisi_analizi()
        
        # 7. Genel Rapor
        self.anomali_raporu_olustur()
        
        return self.anomaliler


# Test için
if __name__ == "__main__":
    # Temizlenmiş veriyi yükle
    df = pd.read_csv('data/processed/enjeksiyon_temiz.csv')
    df['TARİH'] = pd.to_datetime(df['TARİH'])
    
    print(f"✅ Temizlenmiş veri yüklendi: {len(df)} satır")
    
    # Anomali analizi yap
    bulucu = AnomaliBulucu(df)
    anomaliler = bulucu.tam_analiz_yap()
    
    # Anomalileri kaydet
    if anomaliler:
        # Her parametre için ayrı dosya
        for param, anomali_df in anomaliler.items():
            dosya_adi = param.replace(' ', '_').replace('.', '').lower()
            anomali_df.to_csv(f'data/processed/anomali_{dosya_adi}.csv', index=False)
            print(f"💾 {param} anomalileri kaydedildi!")
    
    print(f"\n✅ Anomali tespiti tamamlandı!")
    
    
