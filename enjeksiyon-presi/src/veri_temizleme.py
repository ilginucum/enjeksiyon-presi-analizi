"""
Veri Temizleme Modülü
Bu modül eksik değerleri, aykırı değerleri ve veri kalitesi sorunlarını ele alır.
"""

import pandas as pd
import numpy as np
from datetime import datetime

class VeriTemizleyici:
    """
    Veri kalitesini artırmak için temizleme işlemleri yapan sınıf
    """
    
    def __init__(self, df):
        """
        Args:
            df (pd.DataFrame): Temizlenecek DataFrame
        """
        self.df = df.copy()
        self.temizlik_raporu = {
            'baslangic_satir': len(df),
            'silinen_satir': 0,
            'duzeltilen_deger': 0,
            'sorunlar': []
        }
    
    def eksik_degerleri_analiz_et(self):
        """
        Eksik değerleri analiz eder ve raporlar
        
        Returns:
            pd.DataFrame: Eksik değer raporu
        """
        print("\n" + "="*60)
        print("EKSİK DEĞER ANALİZİ")
        print("="*60)
        
        eksik = self.df.isnull().sum()
        eksik_yuzde = (eksik / len(self.df)) * 100
        
        eksik_df = pd.DataFrame({
            'Sütun': eksik.index,
            'Eksik Sayı': eksik.values,
            'Eksik Yüzde (%)': eksik_yuzde.values
        })
        
        eksik_df = eksik_df[eksik_df['Eksik Sayı'] > 0].sort_values(
            'Eksik Sayı', ascending=False
        )
        
        if len(eksik_df) > 0:
            print("\n⚠️  Eksik Değerler Bulundu:")
            print(eksik_df.to_string(index=False))
            self.temizlik_raporu['sorunlar'].append(
                f"Toplam {len(eksik_df)} sütunda eksik değer var"
            )
        else:
            print("\n✅ Eksik değer yok!")
        
        return eksik_df
    
    def baslik_satirini_temizle(self):
        """
        Başlık satırından kalan veriyi temizler
        """
        print("\n" + "="*60)
        print("BAŞLIK SATIRI TEMİZLEME")
        print("="*60)
        
        # İlk satırda 'tarih', 'kalip' gibi değerler varsa, o satırı sil
        if self.df['TARİH'].iloc[0] == 'tarih':
            print("\n🧹 Başlık satırı bulundu ve siliniyor...")
            self.df = self.df[1:].reset_index(drop=True)
            self.temizlik_raporu['silinen_satir'] += 1
            print("✅ Başlık satırı temizlendi!")
        else:
            print("\n✅ Başlık satırı zaten temiz!")
        
        return self
    
    def veri_tiplerini_duzelt(self):
        """
        Sütunların doğru veri tiplerine dönüştürülmesini sağlar
        """
        print("\n" + "="*60)
        print("VERİ TİPLERİNİ DÜZELTME")
        print("="*60)
        
        # Tarih sütununu datetime'a çevir
        if 'TARİH' in self.df.columns:
            try:
                self.df['TARİH'] = pd.to_datetime(self.df['TARİH'])
                print("\n✅ TARİH sütunu datetime'a çevrildi")
            except:
                print("\n⚠️  TARİH sütunu dönüştürülemedi")
        
        # KALIP NO'yu integer'a çevir
        if 'KALIP NO' in self.df.columns:
            try:
                self.df['KALIP NO'] = pd.to_numeric(self.df['KALIP NO'], errors='coerce').astype('Int64')
                print("✅ KALIP NO sütunu integer'a çevrildi")
            except:
                print("⚠️  KALIP NO sütunu dönüştürülemedi")
        
        # BASKI NO'yu integer'a çevir
        if 'BASKI NO' in self.df.columns:
            try:
                self.df['BASKI NO'] = pd.to_numeric(self.df['BASKI NO'], errors='coerce').astype('Int64')
                print("✅ BASKI NO sütunu integer'a çevrildi")
            except:
                print("⚠️  BASKI NO sütunu dönüştürülemedi")
        
        # MAKİNE KODU kategorik olmalı
        if 'MAKİNE KODU' in self.df.columns:
            # Eğer tamamen boşsa, 'MAK1' olarak doldur
            if self.df['MAKİNE KODU'].isna().all():
                self.df['MAKİNE KODU'] = 'MAK1'
                print("✅ MAKİNE KODU 'MAK1' olarak dolduruldu")
                self.temizlik_raporu['duzeltilen_deger'] += len(self.df)
        
        # Sayısal sütunları float'a çevir
        numeric_columns = [
            'BİRİNCİ FAZ HIZI', 'PİSTON SÜRTÜNME BASINCI', 'İKİNCİ FAZ HIZI',
            'İKİNCİ FAZ MESAFE', '3. FAZ BASINC YÜKSELME ZAMANI', '3. FAZ BASINCI',
            'TOPUK BOYU', 'KALIP DOLUM ZAMANI', 'SPESİFİK BASINÇ BAR'
        ]
        
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        print("\n✅ Tüm sayısal sütunlar float'a çevrildi")
        
        return self
    
    def aykiri_degerleri_bul(self, col_name, method='iqr', threshold=3):
        """
        Belirtilen sütunda aykırı değerleri bulur
        
        Args:
            col_name (str): Sütun adı
            method (str): 'iqr' veya 'zscore'
            threshold (float): Z-score için eşik değeri
            
        Returns:
            pd.Series: Aykırı değerlerin bool maskesi
        """
        if col_name not in self.df.columns:
            return pd.Series([False] * len(self.df))
        
        col = self.df[col_name].dropna()
        
        if method == 'iqr':
            Q1 = col.quantile(0.25)
            Q3 = col.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = (self.df[col_name] < lower_bound) | (self.df[col_name] > upper_bound)
            
        elif method == 'zscore':
            mean = col.mean()
            std = col.std()
            
            z_scores = np.abs((self.df[col_name] - mean) / std)
            outliers = z_scores > threshold
        
        else:
            outliers = pd.Series([False] * len(self.df))
        
        return outliers
    
    def aykiri_deger_analizi(self):
        """
        Tüm sayısal sütunlarda aykırı değer analizi yapar
        """
        print("\n" + "="*60)
        print("AYKIRI DEĞER ANALİZİ (IQR Metodu)")
        print("="*60)
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        aykiri_rapor = []
        
        for col in numeric_columns:
            outliers = self.aykiri_degerleri_bul(col, method='iqr')
            outlier_count = outliers.sum()
            
            if outlier_count > 0:
                outlier_percent = (outlier_count / len(self.df)) * 100
                aykiri_rapor.append({
                    'Sütun': col,
                    'Aykırı Sayı': outlier_count,
                    'Aykırı Yüzde (%)': round(outlier_percent, 2),
                    'Min': self.df[col].min(),
                    'Max': self.df[col].max()
                })
        
        if aykiri_rapor:
            aykiri_df = pd.DataFrame(aykiri_rapor)
            print("\n⚠️  Aykırı Değerler Bulundu:")
            print(aykiri_df.to_string(index=False))
            self.temizlik_raporu['sorunlar'].append(
                f"Toplam {len(aykiri_rapor)} sütunda aykırı değer var"
            )
        else:
            print("\n✅ Aykırı değer yok!")
        
        return aykiri_rapor
    
    def negatif_degerleri_kontrol_et(self):
        """
        Negatif olmaması gereken değerleri kontrol eder
        """
        print("\n" + "="*60)
        print("NEGATİF DEĞER KONTROLÜ")
        print("="*60)
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        negatif_bulundu = False
        
        for col in numeric_columns:
            negatif_count = (self.df[col] < 0).sum()
            if negatif_count > 0:
                print(f"\n⚠️  {col}: {negatif_count} negatif değer bulundu!")
                negatif_bulundu = True
                self.temizlik_raporu['sorunlar'].append(
                    f"{col} sütununda {negatif_count} negatif değer"
                )
        
        if not negatif_bulundu:
            print("\n✅ Negatif değer yok!")
    
    def sifir_degerleri_kontrol_et(self):
        """
        Sıfır olmaması gereken değerleri kontrol eder
        """
        print("\n" + "="*60)
        print("SIFIR DEĞER KONTROLÜ")
        print("="*60)
        
        # Sıfır olmaması gereken sütunlar
        critical_columns = [
            'BİRİNCİ FAZ HIZI', 'İKİNCİ FAZ HIZI', 
            'KALIP DOLUM ZAMANI', 'SPESİFİK BASINÇ BAR'
        ]
        
        sifir_bulundu = False
        
        for col in critical_columns:
            if col in self.df.columns:
                sifir_count = (self.df[col] == 0).sum()
                if sifir_count > 0:
                    print(f"\n⚠️  {col}: {sifir_count} sıfır değer bulundu!")
                    sifir_bulundu = True
                    self.temizlik_raporu['sorunlar'].append(
                        f"{col} sütununda {sifir_count} sıfır değer"
                    )
        
        if not sifir_bulundu:
            print("\n✅ Kritik sütunlarda sıfır değer yok!")
    
    def temizlik_raporu_olustur(self):
        """
        Temizlik sürecinin detaylı raporunu oluşturur
        """
        print("\n" + "="*60)
        print("VERİ TEMİZLİK RAPORU")
        print("="*60)
        
        print(f"\n📊 Başlangıç Satır Sayısı: {self.temizlik_raporu['baslangic_satir']}")
        print(f"📊 Son Satır Sayısı: {len(self.df)}")
        print(f"🗑️  Silinen Satır: {self.temizlik_raporu['silinen_satir']}")
        print(f"✏️  Düzeltilen Değer: {self.temizlik_raporu['duzeltilen_deger']}")
        
        if self.temizlik_raporu['sorunlar']:
            print(f"\n⚠️  Tespit Edilen Sorunlar:")
            for i, sorun in enumerate(self.temizlik_raporu['sorunlar'], 1):
                print(f"  {i}. {sorun}")
        else:
            print("\n✅ Hiçbir sorun tespit edilmedi!")
        
        print(f"\n✅ Temizlenmiş veri boyutu: {self.df.shape}")
    
    def temizle(self):
        """
        Tüm temizleme işlemlerini sırayla çalıştırır
        
        Returns:
            pd.DataFrame: Temizlenmiş DataFrame
        """
        print("\n" + "🧹"*30)
        print("VERİ TEMİZLEME SÜRECİ BAŞLIYOR")
        print("🧹"*30)
        
        # 1. Başlık satırını temizle
        self.baslik_satirini_temizle()
        
        # 2. Veri tiplerini düzelt
        self.veri_tiplerini_duzelt()
        
        # 3. Eksik değer analizi
        self.eksik_degerleri_analiz_et()
        
        # 4. Aykırı değer analizi
        self.aykiri_deger_analizi()
        
        # 5. Negatif değer kontrolü
        self.negatif_degerleri_kontrol_et()
        
        # 6. Sıfır değer kontrolü
        self.sifir_degerleri_kontrol_et()
        
        # 7. Rapor oluştur
        self.temizlik_raporu_olustur()
        
        print("\n✅ VERİ TEMİZLEME TAMAMLANDI!")
        
        return self.df


# Test için
if __name__ == "__main__":
    from veri_yukleme import VeriYukleyici
    
    # Veri yükle
    yukleyici = VeriYukleyici()
    df = yukleyici.enjeksiyon_presi_yukle()
    
    if df is not None:
        # Temizle
        temizleyici = VeriTemizleyici(df)
        df_temiz = temizleyici.temizle()
        
        # Temizlenmiş veriyi kaydet
        df_temiz.to_csv('data/processed/enjeksiyon_temiz.csv', index=False)
        print("\n💾 Temizlenmiş veri 'data/processed/enjeksiyon_temiz.csv' olarak kaydedildi!")