"""
Fırın Verileri - Anomali Tespiti Modülü
Bu modül fırın verilerindeki anormal davranışları tespit eder.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class FirinAnomaliBulucu:
    """
    Fırın anomali tespit işlemlerini gerçekleştiren sınıf
    """
    
    def __init__(self, df):
        """
        Args:
            df (pd.DataFrame): Temizlenmiş DataFrame
        """
        self.df = df.copy()
        self.anomaliler = {}
    
    def sicaklik_kontrolu_anomalisi(self):
        """
        Hedef sıcaklık ile gerçek sıcaklık arasındaki büyük farkları tespit eder
        """
        print("\n" + "="*70)
        print("SICAKLIK KONTROL ANOMALİSİ")
        print("="*70)
        
        # SET ISI - ISI fark sütunlarını bul
        fark_sutunlari = [col for col in self.df.columns if '_FARK' in col]
        
        anomali_sayisi = 0
        
        for fark_col in fark_sutunlari:
            # 50°C üzeri fark = anomali
            anomali_mask = self.df[fark_col] > 50
            anomali_count = anomali_mask.sum()
            
            if anomali_count > 0:
                bolge = fark_col.replace('_FARK', '').replace(' SET ISI', '')
                print(f"\n⚠️  {bolge}: {anomali_count} sıcaklık kontrol anomalisi")
                
                # Anomalileri kaydet
                anomali_df = self.df[anomali_mask][['TARİH', 'SAAT', fark_col]].copy()
                self.anomaliler[f'SICAKLIK_KONTROL_{bolge}'] = anomali_df
                anomali_sayisi += anomali_count
        
        print(f"\n📊 Toplam Sıcaklık Kontrol Anomalisi: {anomali_sayisi}")
        
        return anomali_sayisi
    
    def ani_sicaklik_degisimi(self):
        """
        Ani ve beklenmeyen sıcaklık değişimlerini tespit eder
        """
        print("\n" + "="*70)
        print("ANİ SICAKLIK DEĞİŞİMİ ANALİZİ")
        print("="*70)
        
        # Ana sıcaklık sensörlerini seç
        sicaklik_sutunlari = [
            'CEH.1 ÜST1 ISI', 'CEH.2 ÜST1 ISI', 'CEH.3 ÜST1 ISI',
            'SOĞUTMA1 ISI', 'SOĞUTMA2 ISI', 'SOĞUTMA3 ISI'
        ]
        
        toplam_ani_degisim = 0
        
        for col in sicaklik_sutunlari:
            if col in self.df.columns:
                # Ardışık ölçümler arasındaki fark
                self.df[f'{col}_DEGISIM'] = self.df[col].diff().abs()
                
                # 100°C'den fazla ani değişim = anomali
                ani_degisim = (self.df[f'{col}_DEGISIM'] > 100).sum()
                
                if ani_degisim > 0:
                    print(f"   ⚠️  {col}: {ani_degisim} ani değişim")
                    toplam_ani_degisim += ani_degisim
        
        if toplam_ani_degisim > 0:
            print(f"\n📊 Toplam Ani Değişim: {toplam_ani_degisim}")
            print(f"   (100°C'den fazla ani sıcaklık değişimi)")
        else:
            print(f"\n✅ Ani sıcaklık değişimi tespit edilmedi!")
        
        return toplam_ani_degisim
    
    def enerji_verimsizligi(self):
        """
        Enerji tüketimi anomalilerini tespit eder
        """
        print("\n" + "="*70)
        print("ENERJİ VERİMLİLİĞİ ANALİZİ")
        print("="*70)
        
        # Güç yüzdelerini kontrol et
        guc_sutunlari = [col for col in self.df.columns if 'GÜÇ %' in col]
        
        yuksek_guc_kullanimi = []
        
        for col in guc_sutunlari:
            # %90 üzeri sürekli güç kullanımı = potansiyel verimlilik sorunu
            yuksek_guc = (self.df[col] > 90).sum()
            
            if yuksek_guc > len(self.df) * 0.1:  # %10'dan fazlaysa
                bolge = col.replace(' GÜÇ %', '')
                oran = yuksek_guc / len(self.df) * 100
                yuksek_guc_kullanimi.append({
                    'Bölge': bolge,
                    'Yüksek Güç Sayısı': yuksek_guc,
                    'Oran': f"{oran:.1f}%"
                })
        
        if yuksek_guc_kullanimi:
            print(f"\n⚠️  Sürekli yüksek güç kullanımı (>%90):")
            for item in yuksek_guc_kullanimi[:5]:
                print(f"   • {item['Bölge']}: {item['Yüksek Güç Sayısı']} kayıt ({item['Oran']})")
        else:
            print(f"\n✅ Enerji kullanımı normal seviyelerde!")
        
        return len(yuksek_guc_kullanimi)
    
    def sogutma_sistemi_analizi(self):
        """
        Soğutma sisteminin performansını analiz eder
        """
        print("\n" + "="*70)
        print("SOĞUTMA SİSTEMİ ANALİZİ")
        print("="*70)
        
        # Soğutma sırası kontrolü: SOĞUTMA1 > SOĞUTMA2 > SOĞUTMA3 olmalı
        yanlis_siralama = 0
        
        if all(col in self.df.columns for col in ['SOĞUTMA1 ISI', 'SOĞUTMA2 ISI', 'SOĞUTMA3 ISI']):
            # Soğutma 1 > Soğutma 2 olmalı
            yanlis_1_2 = (self.df['SOĞUTMA1 ISI'] < self.df['SOĞUTMA2 ISI']).sum()
            
            # Soğutma 2 > Soğutma 3 olmalı
            yanlis_2_3 = (self.df['SOĞUTMA2 ISI'] < self.df['SOĞUTMA3 ISI']).sum()
            
            yanlis_siralama = yanlis_1_2 + yanlis_2_3
            
            if yanlis_siralama > 0:
                print(f"\n⚠️  Anormal soğutma sıralaması:")
                print(f"   • SOĞUTMA1 < SOĞUTMA2: {yanlis_1_2} kayıt")
                print(f"   • SOĞUTMA2 < SOĞUTMA3: {yanlis_2_3} kayıt")
                print(f"   Toplam: {yanlis_siralama} anomali")
            else:
                print(f"\n✅ Soğutma sistemi normal çalışıyor!")
            
            # Ortalama sıcaklıklar
            print(f"\n📊 Ortalama Soğutma Sıcaklıkları:")
            print(f"   • SOĞUTMA1: {self.df['SOĞUTMA1 ISI'].mean():.1f}°C")
            print(f"   • SOĞUTMA2: {self.df['SOĞUTMA2 ISI'].mean():.1f}°C")
            print(f"   • SOĞUTMA3: {self.df['SOĞUTMA3 ISI'].mean():.1f}°C")
        
        return yanlis_siralama
    
    def ceh_dengesizligi(self):
        """
        Ceh'ler (bölmeler) arasındaki sıcaklık dengesizliğini tespit eder
        """
        print("\n" + "="*70)
        print("CEH (BÖLME) DENGESİZLİĞİ ANALİZİ")
        print("="*70)
        
        # Her ceh için ortalama sıcaklığı hesapla
        ceh_sicakliklar = {}
        
        for ceh in ['CEH.1', 'CEH.2', 'CEH.3']:
            ceh_sutunlari = [col for col in self.df.columns 
                            if ceh in col and 'ISI' in col and 'SET' not in col]
            
            if ceh_sutunlari:
                ortalama = self.df[ceh_sutunlari].mean().mean()
                ceh_sicakliklar[ceh] = ortalama
        
        if ceh_sicakliklar:
            print(f"\n📊 Ceh Ortalama Sıcaklıkları:")
            for ceh, sicaklik in ceh_sicakliklar.items():
                print(f"   • {ceh}: {sicaklik:.1f}°C")
            
            # Ceh'ler arası fark
            sicakliklar_list = list(ceh_sicakliklar.values())
            max_fark = max(sicakliklar_list) - min(sicakliklar_list)
            
            print(f"\n   Maksimum Ceh Arası Fark: {max_fark:.1f}°C")
            
            if max_fark > 100:
                print(f"   ⚠️  UYARI: Ceh'ler arası büyük sıcaklık farkı!")
            else:
                print(f"   ✅ Ceh'ler dengeli çalışıyor")
        
        return max_fark if ceh_sicakliklar else 0
    
    def anomali_raporu_olustur(self):
        """
        Tüm anomali analizlerinin özet raporunu oluşturur
        """
        print("\n" + "🔴"*35)
        print("GENEL ANOMALİ RAPORU")
        print("🔴"*35)
        
        toplam_anomali = sum(len(v) for v in self.anomaliler.values())
        
        print(f"\n📊 ÖZET:")
        print(f"   Toplam Kayıt: {len(self.df)}")
        print(f"   Tespit Edilen Anomali Tipi: {len(self.anomaliler)}")
        
        if self.anomaliler:
            print(f"\n⚠️  ANOMALİ DAĞILIMI:")
            for anom_tipi, anom_df in self.anomaliler.items():
                print(f"   • {anom_tipi}: {len(anom_df)} adet")
        
        # Öneriler
        print(f"\n💡 ÖNERİLER:")
        print(f"   🔧 Sıcaklık kontrol sistemlerini kalibre edin")
        print(f"   🔧 Sensör bakımlarını yapın")
        print(f"   🔧 Enerji verimliliği için optimizasyon yapın")
        print(f"   🔧 Soğutma sistemi performansını değerlendirin")
        
        print(f"\n✅ Analiz tamamlandı!")
    
    def tam_analiz_yap(self):
        """
        Tüm anomali analizlerini sırayla çalıştırır
        """
        print("\n" + "🔍"*35)
        print("ANOMALİ TESPİT SÜRECİ BAŞLIYOR")
        print("🔍"*35)
        
        # 1. Sıcaklık kontrolü
        self.sicaklik_kontrolu_anomalisi()
        
        # 2. Ani değişimler
        self.ani_sicaklik_degisimi()
        
        # 3. Enerji verimliliği
        self.enerji_verimsizligi()
        
        # 4. Soğutma sistemi
        self.sogutma_sistemi_analizi()
        
        # 5. Ceh dengesizliği
        self.ceh_dengesizligi()
        
        # 6. Genel rapor
        self.anomali_raporu_olustur()
        
        return self.anomaliler


# Test için
if __name__ == "__main__":
    from veri_yukleme import FirinVeriYukleyici
    from veri_temizleme import FirinVeriTemizleyici
    
    # Veri yükle
    yukleyici = FirinVeriYukleyici()
    df = yukleyici.firin_verileri_yukle()
    
    if df is not None:
        # Temizle
        temizleyici = FirinVeriTemizleyici(df)
        df_temiz = temizleyici.temizle()
        
        # Anomali tespit et
        bulucu = FirinAnomaliBulucu(df_temiz)
        anomaliler = bulucu.tam_analiz_yap()
        
        # Anomalileri kaydet
        if anomaliler:
            for anom_tipi, anom_df in anomaliler.items():
                dosya_adi = anom_tipi.lower().replace(' ', '_')
                anom_df.to_csv(f'data/processed/anomali_{dosya_adi}.csv', index=False)
            print(f"\n💾 {len(anomaliler)} adet anomali dosyası kaydedildi!")