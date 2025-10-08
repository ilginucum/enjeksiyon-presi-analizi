"""
Fırın Verileri - Veri Yükleme Modülü
Bu modül Excel dosyalarını okuyup pandas DataFrame'e dönüştürür.
"""

import pandas as pd
import os
from datetime import datetime

class FirinVeriYukleyici:
    """
    Fırın Excel dosyalarını yüklemek ve temel bilgileri göstermek için sınıf
    """
    
    def __init__(self, data_path='data/raw/'):
        """
        Args:
            data_path (str): Veri dosyalarının bulunduğu klasör
        """
        self.data_path = data_path
        
    def excel_oku(self, dosya_adi):
        """
        Excel dosyasını okur ve DataFrame olarak döndürür
        
        Args:
            dosya_adi (str): Okunacak Excel dosyasının adı
            
        Returns:
            pd.DataFrame: Yüklenen veri
        """
        try:
            dosya_yolu = os.path.join(self.data_path, dosya_adi)
            print(f"📂 Dosya okunuyor: {dosya_yolu}")
            
            # Excel dosyasını oku
            df = pd.read_excel(dosya_yolu)
            
            print(f"✅ Dosya başarıyla yüklendi!")
            print(f"📊 Satır sayısı: {len(df)}")
            print(f"📊 Sütun sayısı: {len(df.columns)}")
            
            return df
            
        except FileNotFoundError:
            print(f"❌ HATA: {dosya_yolu} dosyası bulunamadı!")
            return None
        except Exception as e:
            print(f"❌ HATA: {str(e)}")
            return None
    
    def firin_verileri_yukle(self):
        """
        Fırın verilerini yükler ve temizler
        
        Returns:
            pd.DataFrame: Fırın verileri
        """
        print("\n" + "="*50)
        print("FIRIN VERİLERİ YÜKLENİYOR")
        print("="*50 + "\n")
        
        df = self.excel_oku('Fırın Verileri18.xlsx')
        
        if df is None:
            return None
        
        print("\n📋 Sütun İsimleri:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Tarih ve saat sütunlarını datetime'a çevir
        if 'TARİH' in df.columns:
            df['TARİH'] = pd.to_datetime(df['TARİH'], errors='coerce')
            print(f"\n📅 Tarih Aralığı: {df['TARİH'].min()} - {df['TARİH'].max()}")
        
        if 'SAAT' in df.columns:
            # Sadece saat bilgisi var, time formatına çevir
            df['SAAT'] = pd.to_datetime(df['SAAT'], format='%H:%M:%S', errors='coerce').dt.time
        
        print("\n✅ Veri yükleme tamamlandı!")
        
        return df
    
    def veri_bilgisi_goster(self, df, baslik="VERİ BİLGİSİ"):
        """
        DataFrame hakkında detaylı bilgi gösterir
        
        Args:
            df (pd.DataFrame): İncelenecek DataFrame
            baslik (str): Gösterilecek başlık
        """
        print("\n" + "="*50)
        print(baslik)
        print("="*50)
        
        print(f"\n📊 Boyut: {df.shape[0]} satır x {df.shape[1]} sütun")
        print(f"\n📋 Sütunlar ve Veri Tipleri:")
        print(df.dtypes)
        
        print(f"\n🔍 İlk 5 Satır:")
        print(df.head())
        
        # Sadece sayısal sütunlar için istatistik
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print(f"\n📈 Temel İstatistikler (Sayısal Sütunlar):")
            print(df[numeric_cols].describe())
        
        # Eksik değerler
        eksik = df.isnull().sum()
        if eksik.sum() > 0:
            print(f"\n⚠️  Eksik Değerler:")
            print(eksik[eksik > 0])
        else:
            print(f"\n✅ Eksik değer yok!")
    
    def sicaklik_sensoru_bilgisi(self, df):
        """
        Sıcaklık sensörleri hakkında özet bilgi verir
        """
        print("\n" + "="*50)
        print("SICAKLIK SENSÖR ÖZETİ")
        print("="*50)
        
        # Sıcaklık sütunlarını bul (ISI içeren sütunlar)
        sicaklik_sutunlari = [col for col in df.columns if 'ISI' in col.upper() or 'ISITMA' in col.upper()]
        
        print(f"\n🌡️ Toplam Sıcaklık Sensörü: {len(sicaklik_sutunlari)}")
        
        print(f"\n📊 Sıcaklık Sensörleri:")
        for sensor in sicaklik_sutunlari:
            if df[sensor].dtype in ['int64', 'float64']:
                min_val = df[sensor].min()
                max_val = df[sensor].max()
                mean_val = df[sensor].mean()
                print(f"  • {sensor}: {min_val:.0f}°C - {max_val:.0f}°C (Ort: {mean_val:.0f}°C)")


# Test için
if __name__ == "__main__":
    # Veri yükleyiciyi oluştur
    yukleyici = FirinVeriYukleyici()
    
    # Fırın verilerini yükle
    df_firin = yukleyici.firin_verileri_yukle()
    
    if df_firin is not None:
        # Detaylı bilgi göster
        yukleyici.veri_bilgisi_goster(df_firin, "FIRIN VERİLERİ BİLGİSİ")
        
        # Sıcaklık sensör bilgisi
        yukleyici.sicaklik_sensoru_bilgisi(df_firin)