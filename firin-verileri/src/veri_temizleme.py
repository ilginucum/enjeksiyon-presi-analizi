"""
Fırın Verileri - Veri Temizleme Modülü
Bu modül eksik değerleri, aykırı değerleri ve veri kalitesi sorunlarını ele alır.
"""

import pandas as pd
import numpy as np

class FirinVeriTemizleyici:
    """
    Fırın verileri için temizleme işlemleri yapan sınıf
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
    
    def sensor_hatalarini_duzelt(self):
        """
        Sıcaklık sensörü hatalarını düzeltir
        (-3276 gibi imkansız değerler)
        """
        print("\n" + "="*60)
        print("SENSÖR HATALARI DÜZELTİLİYOR")
        print("="*60)
        
        # Sıcaklık sütunlarını bul
        sicaklik_sutunlari = [col for col in self.df.columns if 'ISI' in col.upper()]
        
        duzeltilen_toplam = 0
        
        for col in sicaklik_sutunlari:
            # İmkansız değerler (negatif veya çok yüksek)
            # Sıcaklık -273°C'den düşük olamaz (mutlak sıfır)
            # Endüstriyel fırın 2000°C'den yüksek olamaz
            
            hata_mask = (self.df[col] < -100) | (self.df[col] > 2000)
            hata_sayisi = hata_mask.sum()
            
            if hata_sayisi > 0:
                print(f"\n⚠️  {col}: {hata_sayisi} hatalı değer bulundu")
                
                # Hatalı değerleri NaN yap, sonra interpolate et
                self.df.loc[hata_mask, col] = np.nan
                self.df[col] = self.df[col].interpolate(method='linear', limit_direction='both')
                
                duzeltilen_toplam += hata_sayisi
                print(f"   ✅ Düzeltildi (interpolasyon)")
        
        if duzeltilen_toplam > 0:
            print(f"\n✅ Toplam {duzeltilen_toplam} sensör hatası düzeltildi!")
            self.temizlik_raporu['duzeltilen_deger'] += duzeltilen_toplam
        else:
            print(f"\n✅ Sensör hatası bulunamadı!")
        
        return self
    
    def eksik_degerleri_kontrol_et(self):
        """
        Eksik değerleri analiz eder
        """
        print("\n" + "="*60)
        print("EKSİK DEĞER ANALİZİ")
        print("="*60)
        
        eksik = self.df.isnull().sum()
        eksik_toplam = eksik.sum()
        
        if eksik_toplam > 0:
            print(f"\n⚠️  Toplam {eksik_toplam} eksik değer bulundu:")
            eksik_sutunlar = eksik[eksik > 0].sort_values(ascending=False)
            for col, sayi in eksik_sutunlar.items():
                print(f"   • {col}: {sayi} adet")
            
            # Eksik değerleri doldur (forward fill)
            self.df = self.df.fillna(method='ffill').fillna(method='bfill')
            print(f"\n✅ Eksik değerler dolduruldu (forward/backward fill)")
            
            self.temizlik_raporu['sorunlar'].append(
                f"{eksik_toplam} eksik değer bulundu ve dolduruldu"
            )
        else:
            print(f"\n✅ Eksik değer yok!")
        
        return self
    
    def set_isi_kontrolu(self):
        """
        SET ISI (hedef sıcaklık) ile gerçek ISI farkını kontrol eder
        """
        print("\n" + "="*60)
        print("SET ISI vs GERÇEK ISI KONTROLÜ")
        print("="*60)
        
        # SET ISI ve ISI çiftlerini bul
        set_isi_sutunlari = [col for col in self.df.columns if 'SET ISI' in col]
        
        buyuk_farklar = []
        
        for set_col in set_isi_sutunlari:
            # Karşılık gelen gerçek ISI sütununu bul
            gercek_col = set_col.replace('SET ISI', 'ISI').replace('SET', '').strip()
            
            # Eğer sütun varsa
            if gercek_col in self.df.columns and gercek_col != set_col:
                # Farkı hesapla
                self.df[f'{set_col}_FARK'] = abs(self.df[set_col] - self.df[gercek_col])
                
                # Ortalama fark
                ort_fark = self.df[f'{set_col}_FARK'].mean()
                max_fark = self.df[f'{set_col}_FARK'].max()
                
                # Büyük fark varsa uyar (>50°C)
                if max_fark > 50:
                    buyuk_fark_sayisi = (self.df[f'{set_col}_FARK'] > 50).sum()
                    buyuk_farklar.append({
                        'Bölge': set_col.replace(' SET ISI', ''),
                        'Ortalama Fark': f"{ort_fark:.1f}°C",
                        'Max Fark': f"{max_fark:.1f}°C",
                        'Büyük Fark Sayısı': buyuk_fark_sayisi
                    })
        
        if buyuk_farklar:
            print(f"\n⚠️  Hedef-Gerçek sıcaklık farkı >50°C olan bölgeler:")
            for fark in buyuk_farklar:
                print(f"\n   • {fark['Bölge']}:")
                print(f"     Ortalama Fark: {fark['Ortalama Fark']}")
                print(f"     Maksimum Fark: {fark['Max Fark']}")
                print(f"     Problem Sayısı: {fark['Büyük Fark Sayısı']} kayıt")
            
            self.temizlik_raporu['sorunlar'].append(
                f"{len(buyuk_farklar)} bölgede büyük sıcaklık farkı var"
            )
        else:
            print(f"\n✅ Tüm bölgelerde sıcaklık kontrolü normal!")
        
        return self
    
    def aykiri_deger_analizi(self):
        """
        Aykırı değerleri tespit eder (IQR metodu)
        """
        print("\n" + "="*60)
        print("AYKIRI DEĞER ANALİZİ")
        print("="*60)
        
        # Sadece sıcaklık sütunları için
        sicaklik_sutunlari = [col for col in self.df.columns 
                             if 'ISI' in col.upper() and 'SET' not in col.upper()]
        
        aykiri_rapor = []
        
        for col in sicaklik_sutunlari:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            aykirilar = ((self.df[col] < lower) | (self.df[col] > upper)).sum()
            
            if aykirilar > 0 and aykirilar > len(self.df) * 0.01:  # %1'den fazlaysa
                aykiri_rapor.append({
                    'Sütun': col,
                    'Aykırı Sayı': aykirilar,
                    'Aykırı %': f"{aykirilar/len(self.df)*100:.2f}%"
                })
        
        if aykiri_rapor:
            print(f"\n⚠️  Toplam {len(aykiri_rapor)} sütunda aykırı değer bulundu:")
            for item in aykiri_rapor[:10]:  # İlk 10 tanesini göster
                print(f"   • {item['Sütun']}: {item['Aykırı Sayı']} ({item['Aykırı %']})")
        else:
            print(f"\n✅ Önemli aykırı değer yok!")
        
        return self
    
    def zaman_tutarsizligi_kontrol(self):
        """
        Zaman serisi tutarlılığını kontrol eder
        """
        print("\n" + "="*60)
        print("ZAMAN SERİSİ TUTARLILIĞI")
        print("="*60)
        
        # Tarih sütununu sırala
        self.df = self.df.sort_values('TARİH').reset_index(drop=True)
        
        # Zaman farkını hesapla
        self.df['ZAMAN_FARKI'] = self.df['TARİH'].diff().dt.total_seconds() / 60  # dakika
        
        # Normal aralık: 1-10 dakika (fırın her 3 dakikada kayıt alıyor gibi)
        anormal_aralikar = ((self.df['ZAMAN_FARKI'] < 0) | 
                           (self.df['ZAMAN_FARKI'] > 30)).sum()
        
        if anormal_aralikar > 0:
            print(f"\n⚠️  {anormal_aralikar} anormal zaman aralığı bulundu")
            print(f"   (30 dakikadan uzun veya negatif)")
        else:
            print(f"\n✅ Zaman serisi tutarlı!")
        
        # Geçici sütunu sil
        self.df = self.df.drop('ZAMAN_FARKI', axis=1)
        
        return self
    
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
        
        # 1. Sensör hatalarını düzelt
        self.sensor_hatalarini_duzelt()
        
        # 2. Eksik değerleri kontrol et
        self.eksik_degerleri_kontrol_et()
        
        # 3. SET ISI kontrolü
        self.set_isi_kontrolu()
        
        # 4. Aykırı değer analizi
        self.aykiri_deger_analizi()
        
        # 5. Zaman tutarlılığı
        self.zaman_tutarsizligi_kontrol()
        
        # 6. Rapor oluştur
        self.temizlik_raporu_olustur()
        
        print("\n✅ VERİ TEMİZLEME TAMAMLANDI!")
        
        return self.df


# Test için
if __name__ == "__main__":
    from veri_yukleme import FirinVeriYukleyici
    
    # Veri yükle
    yukleyici = FirinVeriYukleyici()
    df = yukleyici.firin_verileri_yukle()
    
    if df is not None:
        # Temizle
        temizleyici = FirinVeriTemizleyici(df)
        df_temiz = temizleyici.temizle()
        
        # Temizlenmiş veriyi kaydet
        df_temiz.to_csv('data/processed/firin_temiz.csv', index=False)
        print("\n💾 Temizlenmiş veri 'data/processed/firin_temiz.csv' olarak kaydedildi!")