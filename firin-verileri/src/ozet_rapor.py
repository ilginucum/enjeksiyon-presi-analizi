"""
Fırın Analizi - Özet Rapor Oluşturucu
Bu modül tüm analiz sonuçlarını özetleyen bir TXT raporu oluşturur.
"""

import pandas as pd
import json
from datetime import datetime
import os

def ozet_rapor_olustur():
    """
    Fırın analizi için özet TXT raporu oluşturur
    """
    
    # Performans raporunu yükle
    with open('reports/firin_performans_raporu.json', 'r', encoding='utf-8') as f:
        performans = json.load(f)
    
    # Temizlenmiş veriyi yükle
    df = pd.read_csv('data/processed/firin_temiz.csv')
    df['TARİH'] = pd.to_datetime(df['TARİH'])
    
    # Rapor metni
    rapor = []
    
    # Başlık
    rapor.append("=" * 80)
    rapor.append(" " * 25 + "FIRIN ANALİZ RAPORU")
    rapor.append(" " * 30 + "O&O Technology")
    rapor.append("=" * 80)
    rapor.append(f"Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    rapor.append("=" * 80)
    
    # 1. VERİ ÖZETİ
    rapor.append("\n1. VERİ ÖZETİ")
    rapor.append("-" * 80)
    rapor.append(f"   Ham Veri Satırı: {len(df):,}")
    rapor.append(f"   Temizlenmiş Veri Satırı: {len(df):,}")
    rapor.append(f"   Sütun Sayısı: {len(df.columns)}")
    rapor.append(f"   Tarih Aralığı: {df['TARİH'].min().date()} - {df['TARİH'].max().date()}")
    rapor.append(f"   Analiz Dönemi: {(df['TARİH'].max() - df['TARİH'].min()).days + 1} gün")
    rapor.append(f"   Toplam Sıcaklık Sensörü: 30 adet")
    rapor.append(f"   Toplam Güç Ölçüm Noktası: 18 adet")
    
    # 2. SICAKLIK KONTROL PERFORMANSI
    rapor.append("\n2. SICAKLIK KONTROL PERFORMANSI")
    rapor.append("-" * 80)
    rapor.append(f"   Genel Kontrol Başarısı: {performans['sicaklik_kontrolu']['ortalama_basari']:.1f}%")
    rapor.append(f"   Kontrol Edilen Bölge: 12 adet")
    rapor.append("")
    rapor.append("   En İyi Performans Gösteren Bölgeler:")
    
    # En iyi 3 bölgeyi bul
    bolge_detaylari = performans['sicaklik_kontrolu']['bolge_detaylari']
    en_iyiler = sorted(bolge_detaylari.items(), 
                      key=lambda x: x[1]['basari_orani'], 
                      reverse=True)[:3]
    
    for i, (bolge, veri) in enumerate(en_iyiler, 1):
        rapor.append(f"      {i}. {bolge}: {veri['basari_orani']:.1f}%")
    
    rapor.append("")
    rapor.append("   İyileştirme Gereken Bölgeler:")
    
    # En kötü 3 bölgeyi bul
    en_kotular = sorted(bolge_detaylari.items(), 
                       key=lambda x: x[1]['basari_orani'])[:3]
    
    for i, (bolge, veri) in enumerate(en_kotular, 1):
        rapor.append(f"      {i}. {bolge}: {veri['basari_orani']:.1f}% (Ort. Fark: {veri['ortalama_fark']:.1f}°C)")
    
    # 3. CEH ANALİZİ
    rapor.append("\n3. CEH (BÖLME) ANALİZİ")
    rapor.append("-" * 80)
    rapor.append(f"   CEH.1 Ortalama Sıcaklık: {performans['ceh_dengesizlik']['ceh1_ortalama']:.1f}°C")
    rapor.append(f"   CEH.2 Ortalama Sıcaklık: {performans['ceh_dengesizlik']['ceh2_ortalama']:.1f}°C")
    rapor.append(f"   CEH.3 Ortalama Sıcaklık: {performans['ceh_dengesizlik']['ceh3_ortalama']:.1f}°C")
    rapor.append(f"   Maksimum Fark: {performans['ceh_dengesizlik']['max_fark']:.1f}°C")
    rapor.append(f"   Denge Skoru: {performans['ceh_dengesizlik']['denge_skoru']:.1f}/100")
    
    if performans['ceh_dengesizlik']['max_fark'] > 100:
        rapor.append("   ⚠️  UYARI: Ceh'ler arası yüksek sıcaklık farkı tespit edildi!")
    else:
        rapor.append("   ✅ Ceh dengesizliği kabul edilebilir seviyede")
    
    # 4. ENERJİ VERİMLİLİĞİ
    rapor.append("\n4. ENERJİ VERİMLİLİĞİ")
    rapor.append("-" * 80)
    rapor.append(f"   Ortalama Güç Kullanımı: {performans['enerji_verimliligi']['ortalama_guc']:.1f}%")
    rapor.append(f"   Enerji Verimlilik Skoru: {performans['enerji_verimliligi']['verimlilik_skoru']:.1f}/100")
    
    ortalama_guc = performans['enerji_verimliligi']['ortalama_guc']
    if 50 <= ortalama_guc <= 70:
        rapor.append("   ✅ Optimal güç kullanımı aralığında")
    elif ortalama_guc < 50:
        rapor.append("   ⚠️  Düşük kapasite kullanımı - Üretim artırılabilir")
    else:
        rapor.append("   ⚠️  Yüksek enerji tüketimi - Optimizasyon gerekli")
    
    # 5. SOĞUTMA SİSTEMİ
    rapor.append("\n5. SOĞUTMA SİSTEMİ PERFORMANSI")
    rapor.append("-" * 80)
    
    # Ortalama sıcaklıkları hesapla
    sogutma1 = df['SOĞUTMA1 ISI'].mean()
    sogutma2 = df['SOĞUTMA2 ISI'].mean()
    sogutma3 = df['SOĞUTMA3 ISI'].mean()
    
    rapor.append(f"   Soğutma 1: {sogutma1:.1f}°C")
    rapor.append(f"   Soğutma 2: {sogutma2:.1f}°C")
    rapor.append(f"   Soğutma 3: {sogutma3:.1f}°C")
    rapor.append(f"   Toplam Soğutma: {performans['sogutma_etkinligi']['toplam_sogutma']:.1f}°C")
    rapor.append(f"   Soğutma Etkinliği: {performans['sogutma_etkinligi']['etkinlik_skoru']:.1f}%")
    
    fark1_2 = performans['sogutma_etkinligi']['asamali_sogutma']['fark1_2']
    fark2_3 = performans['sogutma_etkinligi']['asamali_sogutma']['fark2_3']
    
    rapor.append(f"   Aşamalı Soğutma:")
    rapor.append(f"      • 1→2: {fark1_2:.1f}°C")
    rapor.append(f"      • 2→3: {fark2_3:.1f}°C")
    
    if abs(fark1_2 - fark2_3) < 50:
        rapor.append("   ✅ Dengeli soğutma sağlanıyor")
    else:
        rapor.append("   ⚠️  Dengesiz soğutma - Kontrol gerekli")
    
    # 6. GENEL PERFORMANS
    rapor.append("\n6. GENEL PERFORMANS SKORU")
    rapor.append("-" * 80)
    rapor.append(f"   Sıcaklık Kontrolü: {performans['genel_skor']['sicaklik']:.1f}/50")
    rapor.append(f"   Enerji Verimliliği: {performans['genel_skor']['enerji']:.1f}/30")
    rapor.append(f"   Soğutma Etkinliği: {performans['genel_skor']['sogutma']:.1f}/20")
    rapor.append("   " + "-" * 50)
    rapor.append(f"   TOPLAM SKOR: {performans['genel_skor']['toplam']:.1f}/100")
    rapor.append(f"   Fırın Durumu: {performans['genel_skor']['durum']}")
    
    # 7. ANOMALİ TESPİTLERİ
    rapor.append("\n7. ANOMALİ TESPİT SONUÇLARI")
    rapor.append("-" * 80)
    
    # Anomali sayılarını hesapla
    toplam_anomali = 0
    anomali_kategorileri = {}
    
    # Sıcaklık kontrol anomalileri
    for bolge, veri in bolge_detaylari.items():
        basarisiz = len(df) * (100 - veri['basari_orani']) / 100
        if basarisiz > 0:
            anomali_kategorileri[f"Sıcaklık - {bolge}"] = int(basarisiz)
            toplam_anomali += basarisiz
    
    rapor.append(f"   Toplam Anomali: {int(toplam_anomali):,} ({int(toplam_anomali)/len(df)*100:.1f}%)")
    rapor.append(f"   Kategori Sayısı: {len(anomali_kategorileri)} adet")
    rapor.append("")
    rapor.append("   En Kritik Anomali Kategorileri:")
    
    # En yüksek 5 anomaliyi göster
    en_kritikar = sorted(anomali_kategorileri.items(), 
                         key=lambda x: x[1], 
                         reverse=True)[:5]
    
    for i, (kategori, sayi) in enumerate(en_kritikar, 1):
        rapor.append(f"      {i}. {kategori}: {sayi:,} adet")
    
    # 8. ÖNLEYİCİ BAKIM ÖNERİLERİ
    rapor.append("\n8. ÖNLEYİCİ BAKIM ÖNERİLERİ")
    rapor.append("-" * 80)
    
    oneriler = performans['bakim_onerileri']
    
    if oneriler:
        yuksek = sum(1 for o in oneriler if o['oncelik'] == 'YÜKSEK')
        orta = sum(1 for o in oneriler if o['oncelik'] == 'ORTA')
        dusuk = sum(1 for o in oneriler if o['oncelik'] == 'DÜŞÜK')
        
        rapor.append(f"   Toplam Öneri: {len(oneriler)} adet")
        rapor.append(f"   Yüksek Öncelikli: {yuksek}")
        rapor.append(f"   Orta Öncelikli: {orta}")
        rapor.append(f"   Düşük Öncelikli: {dusuk}")
        rapor.append("")
        
        for i, oneri in enumerate(oneriler, 1):
            rapor.append(f"   {i}. [{oneri['oncelik']}] {oneri['kategori']}")
            rapor.append(f"      Sorun: {oneri['sorun']}")
            rapor.append(f"      Öneri: {oneri['oneri']}")
            rapor.append(f"      Tahmini Süre: {oneri['sure']}")
            rapor.append("")
    else:
        rapor.append("   ✅ Acil bakım önerisi bulunmamaktadır.")
        rapor.append("   Fırın iyi durumda çalışmaktadır.")
    
    # 9. OPERASYONEL METRİKLER
    rapor.append("\n9. OPERASYONEL METRİKLER")
    rapor.append("-" * 80)
    rapor.append(f"   Toplam Kayıt: {performans['operasyonel_verimlilik']['toplam_kayit']:,}")
    rapor.append(f"   Analiz Dönemi: {performans['operasyonel_verimlilik']['toplam_gun']} gün")
    rapor.append(f"   Günlük Ortalama Kayıt: {performans['operasyonel_verimlilik']['gunluk_ortalama']:.0f}")
    rapor.append(f"   Veri Tutarlılığı: {performans['operasyonel_verimlilik']['tutarlilik_skoru']:.1f}/100")
    
    # 10. SONUÇ VE ÖNERİLER
    rapor.append("\n10. SONUÇ VE DEĞERLENDİRME")
    rapor.append("-" * 80)
    rapor.append("")
    rapor.append("   Bu analiz, endüstriyel fırının operasyonel verilerini inceleyerek")
    rapor.append("   veri odaklı kararlar almayı sağlamaktadır. Analiz sonuçlarına göre:")
    rapor.append("")
    
    # Genel değerlendirme
    genel_skor = performans['genel_skor']['toplam']
    
    if genel_skor >= 90:
        rapor.append("   ✅ Fırın mükemmel performans göstermektedir.")
        rapor.append("   Mevcut bakım programına devam edilmesi önerilir.")
    elif genel_skor >= 75:
        rapor.append("   ✅ Fırın iyi performans göstermektedir.")
        rapor.append("   Küçük iyileştirmeler ile optimal seviyeye ulaşılabilir.")
    elif genel_skor >= 60:
        rapor.append("   ⚠️  Fırın orta seviye performans göstermektedir.")
        rapor.append("   Belirtilen bakım önerilerinin uygulanması gereklidir.")
    else:
        rapor.append("   🔴 Fırın düşük performans göstermektedir.")
        rapor.append("   Acil bakım ve optimizasyon çalışmaları yapılmalıdır.")
    
    rapor.append("")
    rapor.append("   Önemli Bulgular:")
    
    # Kritik bulguları listele
    bulgular = []
    
    if performans['ceh_dengesizlik']['max_fark'] > 100:
        bulgular.append("Ceh bölmeleri arası yüksek sıcaklık farkı")
    
    if performans['sicaklik_kontrolu']['ortalama_basari'] < 75:
        bulgular.append("Sıcaklık kontrol başarısı düşük")
    
    if performans['enerji_verimliligi']['ortalama_guc'] > 80:
        bulgular.append("Yüksek enerji tüketimi")
    
    if yuksek > 0:
        bulgular.append(f"{yuksek} adet yüksek öncelikli bakım önerisi")
    
    if bulgular:
        for bulgu in bulgular:
            rapor.append(f"      • {bulgu}")
    else:
        rapor.append("      • Kritik bulgu tespit edilmedi")
    
    rapor.append("")
    rapor.append("   Teşekkürler!")
    rapor.append("")
    rapor.append("=" * 80)
    
    # Raporu kaydet
    with open('reports/firin_ozet_rapor.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(rapor))
    
    print("✅ Özet rapor 'reports/firin_ozet_rapor.txt' olarak kaydedildi!")
    
    # Konsola da yazdır
    print("\n" + '\n'.join(rapor))


if __name__ == "__main__":
    ozet_rapor_olustur()