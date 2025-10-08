"""
Main - Ana Çalıştırma Dosyası
Tüm analiz sürecini tek komutla çalıştırır.

Kullanım:
    python main.py
"""

import sys
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Modülleri içe aktar
from src.veri_yukleme import VeriYukleyici
from src.veri_temizleme import VeriTemizleyici
from src.anomali_tespiti import AnomaliBulucu
from src.gorsellestirme import Gorselestirici
from src.performans_analizi import PerformansAnalizci

def banner():
    """Başlangıç banner'ı"""
    print("\n" + "="*80)
    print(" " * 20 + "🏭 ENJEKSİYON PRESİ VERİ ANALİZİ 🏭")
    print(" " * 25 + "O&O Technology - 2025")
    print("="*80)
    print(f"\n📅 Analiz Başlangıç Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

def adim_baslik(adim_no, baslik):
    """Adım başlığı yazdırır"""
    print("\n" + "🔷"*40)
    print(f"ADIM {adim_no}: {baslik}")
    print("🔷"*40 + "\n")

def main():
    """Ana çalıştırma fonksiyonu"""
    
    # Banner göster
    banner()
    
    try:
        # ADIM 1: VERİ YÜKLEME
        adim_baslik(1, "VERİ YÜKLEME")
        yukleyici = VeriYukleyici()
        df = yukleyici.enjeksiyon_presi_yukle()
        
        if df is None:
            print("❌ HATA: Veri yüklenemedi! İşlem durduruluyor.")
            sys.exit(1)
        
        yukleyici.veri_bilgisi_goster(df, "ENJEKSİYON PRESİ HAM VERİ")
        
        # ADIM 2: VERİ TEMİZLEME
        adim_baslik(2, "VERİ TEMİZLEME")
        temizleyici = VeriTemizleyici(df)
        df_temiz = temizleyici.temizle()
        
        # Temizlenmiş veriyi kaydet
        df_temiz.to_csv('data/processed/enjeksiyon_temiz.csv', index=False)
        print("\n💾 Temizlenmiş veri 'data/processed/enjeksiyon_temiz.csv' olarak kaydedildi!")
        
        # ADIM 3: ANOMALİ TESPİTİ
        adim_baslik(3, "ANOMALİ TESPİTİ")
        bulucu = AnomaliBulucu(df_temiz)
        anomaliler = bulucu.tam_analiz_yap()
        
        # Anomalileri kaydet
        if anomaliler:
            for param, anomali_df in anomaliler.items():
                dosya_adi = param.replace(' ', '_').replace('.', '').lower()
                anomali_df.to_csv(f'data/processed/anomali_{dosya_adi}.csv', index=False)
            print(f"\n💾 {len(anomaliler)} adet anomali dosyası 'data/processed/' klasörüne kaydedildi!")
        
        # ADIM 4: GÖRSELLEŞTİRME
        adim_baslik(4, "GÖRSELLEŞTİRME")
        gorselestirici = Gorselestirici(df_temiz)
        gorselestirici.tum_grafikleri_olustur()
        
        # ADIM 5: PERFORMANS ANALİZİ
        adim_baslik(5, "PERFORMANS ANALİZİ")
        analizci = PerformansAnalizci(df_temiz)
        performans_raporu = analizci.tam_performans_analizi()
        
        # Performans raporunu kaydet
        import json
        import numpy as np
        
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
        
        performans_serializable = convert_to_serializable(performans_raporu)
        
        with open('reports/performans_raporu.json', 'w', encoding='utf-8') as f:
            json.dump(performans_serializable, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Performans raporu 'reports/performans_raporu.json' olarak kaydedildi!")
        
        # ADIM 6: ÖZET RAPOR
        adim_baslik(6, "ÖZET RAPOR")
        ozet_rapor_olustur(df, df_temiz, anomaliler, performans_raporu)
        
        # BAŞARI MESAJI
        print("\n" + "="*80)
        print(" " * 30 + "✅ ANALİZ TAMAMLANDI! ✅")
        print("="*80)
        
        print("\n📁 Oluşturulan Dosyalar:")
        print("   📊 data/processed/enjeksiyon_temiz.csv")
        print("   📊 data/processed/anomali_*.csv")
        print("   📈 reports/figures/*.png (5 grafik)")
        print("   📋 reports/performans_raporu.json")
        print("   📄 reports/ozet_rapor.txt")
        
        print(f"\n📅 Analiz Bitiş Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ HATA OLUŞTU: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def ozet_rapor_olustur(df_ham, df_temiz, anomaliler, performans):
    """Özet metin raporu oluşturur"""
    
    rapor = []
    rapor.append("="*80)
    rapor.append(" " * 20 + "ENJEKSİYON PRESİ ANALİZ RAPORU")
    rapor.append(" " * 30 + "O&O Technology")
    rapor.append("="*80)
    rapor.append(f"\nRapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    rapor.append("\n" + "="*80)
    
    # VERİ ÖZETİ
    rapor.append("\n1. VERİ ÖZETİ")
    rapor.append("-"*80)
    rapor.append(f"   Ham Veri Satırı: {len(df_ham)}")
    rapor.append(f"   Temizlenmiş Veri Satırı: {len(df_temiz)}")
    rapor.append(f"   Silinen Satır: {len(df_ham) - len(df_temiz)}")
    rapor.append(f"   Sütun Sayısı: {len(df_temiz.columns)}")
    rapor.append(f"   Tarih Aralığı: {df_temiz['TARİH'].min().date()} - {df_temiz['TARİH'].max().date()}")
    
    # ANOMALİ ÖZETİ
    rapor.append("\n2. ANOMALİ TESPİT SONUÇLARI")
    rapor.append("-"*80)
    
    if anomaliler:
        toplam_anomali = sum(len(v) for v in anomaliler.values())
        rapor.append(f"   Toplam Anomali: {toplam_anomali} ({toplam_anomali/len(df_temiz)*100:.1f}%)")
        rapor.append(f"   Anomali Bulunan Parametre: {len(anomaliler)} adet")
        rapor.append("\n   Detay:")
        for param, anomali_df in anomaliler.items():
            rapor.append(f"      • {param}: {len(anomali_df)} adet")
    else:
        rapor.append("   ✅ Hiçbir anomali tespit edilmedi!")
    
    # PERFORMANS ÖZETİ
    rapor.append("\n3. PERFORMANS METRİKLERİ")
    rapor.append("-"*80)
    
    if 'cevrim_suresi' in performans:
        cs = performans['cevrim_suresi']
        rapor.append(f"   Ortalama Çevrim Süresi: {cs['ortalama']:.0f} ms")
        rapor.append(f"   Saatlik Kapasite: {cs['saatlik_kapasite']:.0f} ürün/saat")
    
    if 'verimlilik' in performans:
        v = performans['verimlilik']
        rapor.append(f"   Verimlilik Oranı: {v['verimlilik_orani']:.1f}%")
        rapor.append(f"   Günlük Ortalama Üretim: {v['gunluk_ortalama']:.0f} ürün")
    
    if 'kalite' in performans:
        k = performans['kalite']
        rapor.append(f"   Kalite Oranı: {k['kalite_orani']:.1f}%")
        rapor.append(f"   Kalite Sorunlu Ürün: {k['sorunlu_urun']} adet")
    
    if 'saglik_skoru' in performans:
        s = performans['saglik_skoru']
        rapor.append(f"   Makine Sağlık Skoru: {s['toplam']:.1f}/100 - {s['durum']}")
    
    # BAKIM ÖNERİLERİ
    rapor.append("\n4. ÖNLEYİCİ BAKIM ÖNERİLERİ")
    rapor.append("-"*80)
    
    if 'bakim_onerileri' in performans and performans['bakim_onerileri']:
        for i, oneri in enumerate(performans['bakim_onerileri'], 1):
            rapor.append(f"\n   {i}. [{oneri['oncelik']}] {oneri['kategori']}")
            rapor.append(f"      Sorun: {oneri['sorun']}")
            rapor.append(f"      Öneri: {oneri['oneri']}")
            rapor.append(f"      Tahmini Süre: {oneri['sure']}")
    else:
        rapor.append("   ✅ Acil bakım önerisi yok!")
    
    # SONUÇ
    rapor.append("\n5. SONUÇ VE DEĞERLENDİRME")
    rapor.append("-"*80)
    rapor.append("   Bu analiz, enjeksiyon presi makinasının operasyonel verilerini")
    rapor.append("   inceleyerek veri odaklı kararlar almayı sağlamaktadır.")
    rapor.append("\n   Teşekkürler!")
    rapor.append("\n" + "="*80)
    
    # Dosyaya kaydet
    with open('reports/ozet_rapor.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(rapor))
    
    # Ekrana yazdır
    print('\n'.join(rapor))
    
    print("\n💾 Özet rapor 'reports/ozet_rapor.txt' olarak kaydedildi!")


if __name__ == "__main__":
    basari = main()
    sys.exit(0 if basari else 1)