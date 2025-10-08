# 🏭 Enjeksiyon Presi Veri Analizi ve Anlamlandırma Projesi

Bu proje, **520 Ton Enjeksiyon Presi** makinasının operasyonel verilerini analiz ederek veri odaklı kararlar almayı sağlamak, üretim sürecini optimize etmek ve potansiyel arızaları önceden tespit etmek amacıyla geliştirilmiştir.

**🎯 Proje Durumu:** ✅ Tamamlandı

**📊 Analiz Edilen Veri:** 2,630 üretim kaydı (7 gün)

**📈 Tespit Edilen Anomali:** 248 adet (%9.4)

## 📋 Proje Amaçları

- Çalışmanın amacı, enjeksiyon pres makinelerinin operasyonel verilerini analiz ederek veri odaklı kararlar almayı sağlamak
- Üretim sürecini optimize etmek ve potansiyel arızaları önceden tespit etmek
- Gelen verilerin kalitesini artırarak, üretim hattındaki anomalileri belirlemek
- Makinelerin performans analizlerini gerçekleştirmek
- Anlık metrikler ve uyarılar ile önleyici bakım sistemleri geliştirmek

## 🎯 Hedefler

1. ✅ Veri kalitesinin artırılması için veri temizleme işlemleri yapılması
2. ✅ Üretim hattındaki olası anomalilerin belirlenmesi
3. ✅ Makine performans analizlerinin yapılması
4. ✅ Makine performansını izlemek için anlık metrikler ve uyarılar tasarlanması
5. ✅ İstenilen hedeflerin detaylı raporlanması

## 📁 Proje Yapısı

```
enjeksiyon-presi-analizi/
│
├── data/                          # Veri dosyaları
│   ├── raw/                       # Ham veriler
│   └── processed/                 # İşlenmiş veriler
│
├── src/                           # Kaynak kodlar
│   ├── __init__.py               # Python paketi
│   ├── veri_yukleme.py           # Veri yükleme modülü
│   ├── veri_temizleme.py         # Veri temizleme modülü
│   ├── anomali_tespiti.py        # Anomali tespit modülü
│   ├── performans_analizi.py     # Performans analiz modülü
│   └── gorsellestirme.py         # Görselleştirme modülü
│
├── reports/                       # Raporlar ve grafikler
│   └── figures/                   # Grafik görselleri
│
├── main.py                        # Ana çalıştırma dosyası
├── requirements.txt               # Gerekli kütüphaneler
└── README.md                      # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/ilginucum/enjeksiyon-presi-analizi.git
cd enjeksiyon-presi-analizi
```

### 2. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Veri Dosyalarını Yerleştirin
`data/raw/` klasörüne Excel dosyalarını koyun:
- `520TonEnjPres.xlsx`

### 4. Tek Komutla Tüm Analizi Çalıştırın
```bash
python main.py
```

**Bu kadar!** 🎉 Tüm analiz otomatik olarak çalışacak ve sonuçlar oluşturulacak.

### Modül Bazında Kullanım

```python
# Veri yükleme
from src.veri_yukleme import VeriYukleyici

yukleyici = VeriYukleyici()
df = yukleyici.enjeksiyon_presi_yukle()

# Veri temizleme
from src.veri_temizleme import VeriTemizleyici

temizleyici = VeriTemizleyici(df)
df_temiz = temizleyici.temizle()

# Anomali tespiti
from src.anomali_tespiti import AnomaliBulucu

bulucu = AnomaliBulucu(df_temiz)
anomaliler = bulucu.tam_analiz_yap()

# Performans analizi
from src.performans_analizi import PerformansAnalizci

analizci = PerformansAnalizci(df_temiz)
performans = analizci.tam_performans_analizi() 
```

## 📊 Analiz Sonuçları

### ✅ Başarıyla Tamamlanan Analizler

1. **Veri Temizleme**
   - 2,631 ham satırdan 2,630 temiz veri elde edildi
   - Tüm eksik değerler düzeltildi
   - Veri kalitesi %100

2. **Anomali Tespiti**
   - Toplam 248 anomali bulundu (%9.4)
   - En kritik: 155 piston basınç anomalisi
   - 4 farklı parametrede sorun tespit edildi

3. **Performans Metrikleri**
   - Ortalama çevrim süresi: 1.58 saniye
   - Kalite oranı: %92.9
   - Makine sağlık skoru: 67.6/100 (ORTA)
   - Teorik kapasite: 2,273 ürün/saat

4. **Görselleştirme**
   - 5 profesyonel grafik oluşturuldu
   - Zaman serisi, dağılım, anomali haritaları
   - Yüksek çözünürlüklü PNG formatında

### 📁 Oluşturulan Dosyalar

```
data/processed/
├── enjeksiyon_temiz.csv              # Temizlenmiş veri
└── anomali_*.csv                     # Anomali detayları

reports/
├── figures/
│   ├── zaman_serisi.png             # Zaman serisi grafikleri
│   ├── dagilim_grafikleri.png       # Dağılım analizleri
│   ├── anomali_haritasi.png         # Anomali dağılımı
│   ├── iliski_grafikleri.png        # Korelasyon analizleri
│   └── gunluk_anomali.png           # Günlük trend
├── performans_raporu.json           # Detaylı metrikler
└── ozet_rapor.txt                   # Özet rapor
```

## 🔍 Temel Bulgular

### ⚠️ Kritik Sorunlar

1. **Piston Sürtünme Basıncı** (155 anomali - %5.9)
   - Normal aralık: 5-6 bar
   - Anormal: 8-12 bar
   - **Öneri:** Hidrolik sistem bakımı gerekli

2. **Basınç Yükselme Zamanı** (90 sorunlu kayıt)
   - En uzun: 61.8 saniye (normalin 40 katı!)
   - **Öneri:** Valf sistemi acil kontrolü

3. **Kalıp Dolum Zamanı** (31 anomali - %1.2)
   - 19 adet kritik uzun dolum (>1200 ms)
   - **Öneri:** Bu ürünler kalite kontrolünden geçmeli

### ✅ Olumlu Bulgular

- Kalite oranı %92.9 (Hedef: %95)
- Dolum zamanı 7 gün içinde %12 iyileşti
- Çevrim süresi hedefe çok yakın (1.58s vs 1.5s)

## 🛠️ Teknoloji ve Metodoloji

### Kullanılan Kütüphaneler
- **pandas** - Veri manipülasyonu
- **numpy** - Matematiksel işlemler
- **matplotlib & seaborn** - Görselleştirme
- **scikit-learn** - Anomali tespiti
- **openpyxl** - Excel okuma

### Anomali Tespit Yöntemleri
- **IQR (Interquartile Range)** metodu
- **Z-score** analizi
- **İstatistiksel eşik değerleri**
- **Zaman serisi trend analizi**

### Performans Metrikleri
- Çevrim süresi analizi
- Verimlilik oranı hesaplama
- Kalite skorlama
- Makine sağlık skoru (0-100)

## 👤 Geliştirici

**Ilgın Uçum**

- 📧 Email: cilgin.ucum@gmail.com

## 📝 Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.

## 🙏 Teşekkürler

O&O Technology için hazırlanmıştır.

