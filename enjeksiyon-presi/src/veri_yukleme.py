"""
Veri Yükleme Modülü
Bu modül Excel dosyalarını okuyup pandas DataFrame'e dönüştürür.
"""

import pandas as pd
import os
from datetime import datetime

class VeriYukleyici:
    """
    Excel dosyalarını yüklemek ve temel bilgileri göstermek için sınıf
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
    
    def enjeksiyon_presi_yukle(self):
        """
        Enjeksiyon presi verilerini yükler ve temizler
        
        Returns:
            pd.DataFrame: Temizlenmiş enjeksiyon presi verileri
        """
        print("\n" + "="*50)
        print("ENJEKSİYON PRESİ VERİLERİ YÜKLENİYOR")
        print("="*50 + "\n")
        
        df = self.excel_oku('520TonEnjPres.xlsx')
        
        if df is None:
            return None
        
        # İlk iki satır başlık satırı, onları kaldır
        # İlk satırda Türkçe başlıklar, ikinci satırda teknik isimler var
        if len(df) > 2:
            # İkinci satırdaki başlıkları kullan (teknik isimler)
            yeni_basliklar = df.iloc[1].tolist()
            df = df[2:].reset_index(drop=True)
            df.columns = yeni_basliklar
        
        # Sütun isimlerini düzelt (boşlukları kaldır)
        df.columns = df.columns.str.strip()
        
        print("\n📋 Sütun İsimleri:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Tarih sütununu datetime'a çevir
        if 'tarih' in df.columns:
            df['tarih'] = pd.to_datetime(df['tarih'])
            print(f"\n📅 Tarih Aralığı: {df['tarih'].min()} - {df['tarih'].max()}")
        
        # Sayısal sütunları kontrol et ve dönüştür
        numeric_columns = df.columns[3:]  # İlk 3 sütun kategorik
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        print("\n✅ Veri yükleme tamamlandı!")
        
        return df
    
    def firin_verileri_yukle(self):
        """
        Fırın verilerini yükler
        
        Returns:
            pd.DataFrame: Fırın verileri
        """
        print("\n" + "="*50)
        print("FIRIN VERİLERİ YÜKLENİYOR")
        print("="*50 + "\n")
        
        df = self.excel_oku('Fırın Verileri18.xlsx')
        
        if df is None:
            return None
        
        # Tarih ve saat sütunlarını datetime'a çevir
        if 'TARİH' in df.columns:
            df['TARİH'] = pd.to_datetime(df['TARİH'])
        
        if 'SAAT' in df.columns:
            df['SAAT'] = pd.to_datetime(df['SAAT'], format='%H:%M:%S', errors='coerce')
        
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
        
        print(f"\n📈 Temel İstatistikler:")
        print(df.describe())
        
        # Eksik değerler
        eksik = df.isnull().sum()
        if eksik.sum() > 0:
            print(f"\n⚠️  Eksik Değerler:")
            print(eksik[eksik > 0])
        else:
            print(f"\n✅ Eksik değer yok!")


# Test için
if __name__ == "__main__":
    # Veri yükleyiciyi oluştur
    yukleyici = VeriYukleyici()
    
    # Enjeksiyon presi verilerini yükle
    df_enj = yukleyici.enjeksiyon_presi_yukle()
    
    if df_enj is not None:
        yukleyici.veri_bilgisi_goster(df_enj, "ENJEKSİYON PRESİ VERİ BİLGİSİ")