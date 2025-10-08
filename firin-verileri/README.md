# 🔥 Endüstriyel Fırın Veri Analizi ve Anlamlandırma Projesi

Bu proje, **Endüstriyel Fırın** sisteminin operasyonel verilerini analiz ederek veri odaklı kararlar almayı sağlamak, üretim sürecini optimize etmek ve potansiyel arızaları önceden tespit etmek amacıyla geliştirilmiştir.

**🎯 Proje Durumu:** ✅ Tamamlandı

**📊 Analiz Edilen Veri:** 38,792 kayıt (60 gün)

**🌡️ İzlenen Sensör:** 30 sıcaklık sensörü, 18 güç ölçüm noktası

**📈 Genel Performans:** 88.4/100 (İYİ ✅)

## 📋 Proje Amaçları

- Çalışmanın amacı, endüstriyel fırının operasyonel verilerini analiz ederek veri odaklı kararlar almayı sağlamak
- Üretim sürecini optimize etmek ve potansiyel arızaları önceden tespit etmek
- Gelen verilerin kalitesini artırarak, üretim hattındaki anomalileri belirlemek
- Fırının sıcaklık kontrol, enerji verimliliği ve soğutma performansını analiz etmek
- Anlık metrikler ve uyarılar ile önleyici bakım sistemleri geliştirmek

## 🎯 Hedefler

1. ✅ Veri kalitesinin artırılması için veri temizleme işlemleri yapılması
2. ✅ Sıcaklık kontrol sisteminin performans analizi
3. ✅ Ceh (bölme) dengesizliklerinin tespiti
4. ✅ Enerji verimliliği optimizasyonu
5. ✅ Soğutma sistemi etkinlik analizi
6. ✅ Fırın performansını izlemek için anlık metrikler ve uyarılar tasarlanması
7. ✅ İstenilen hedeflerin detaylı raporlanması

## 📁 Proje Yapısı

```
firin-verileri/
│
├── data/                          # Veri dosyaları
│   ├── raw/                       # Ham veriler
│   │   └── Fırın Verileri18.xlsx
│   └── processed/                 # İşlenmiş veriler
│       ├── firin_temiz.csv
│       └── anomali_*.csv
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
│   ├── figures/                   # Grafik görselleri
│   │   ├── sicaklik_zaman_serisi.png
│   │   ├── set_gercek_karsilastirma.png
│   │   ├── ceh_dagilim_analizi.png
│   │   ├── guc_amp_analizi.png
│   │   ├── sogutma_etkinligi.png
│   │   ├── anomali_haritasi.png
│   │   ├── heatmap_korelasyon.png
│   │   └── performans_ozet_dashboard.png
│   ├── firin_performans_raporu.json
│   └── firin_ozet_rapor.txt
│
├── main.py                        # Ana çalıştırma dosyası
├── requirements.txt               # Gerekli kütüphaneler
└── README.md                      # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/kullaniciadi/firin-verileri-analizi.git
cd firin-verileri-analizi
```

### 2. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Veri Dosyalarını Yerleştirin
`data/raw/` klasörüne Excel dosyasını koyun:
- `Fırın Verileri18.xlsx`

### 4. Modül Bazında Kullanım

```python
# 1. Veri yükleme
from src.veri_yukleme import FirinVeriYukleyici

yukleyici = FirinVeriYukleyici()
df = yukleyici.firin_verileri_yukle()

# 2. Veri temizleme
from src.veri_temizleme import FirinVeriTemizleyici

temizleyici = FirinVeriTemizleyici(df)
df_temiz = temizleyici.temizle()

# 3. Anomali tespiti
from src.anomali_tespiti import FirinAnomaliBulucu

bulucu = FirinAnomaliBulucu(df_temiz)
anomaliler = bulucu.tam_analiz_yap()

# 4. Performans analizi
from src.performans_analizi import FirinPerformansAnalizci

analizci = FirinPerformansAnalizci(df_temiz)
performans = analizci.tam_performans_analizi()

# 5. Görselleştirme
from src.gorsellestirme import FirinGorselestirici

gorselestirici = FirinGorselestirici(df_temiz)
gorselestirici.tum_grafikleri_olustur()
```

### 5. Tek Komutla Çalıştırma

Her modülü ayrı ayrı çalıştırabilirsiniz:

```bash
# Veri yükleme ve inceleme
python src/veri_yukleme.py

# Veri temizleme
python src/veri_temizleme.py

# Anomali tespiti
python src/anomali_tespiti.py

# Performans analizi
python src/performans_analizi.py

# Görselleştirme
python src/gorsellestirme.py
```

## 📊 Analiz Sonuçları

### ✅ Başarıyla Tamamlanan Analizler

#### 1. **Veri Temizleme**
   - 38,792 ham satır işlendi
   - 1,779 sensör hatası düzeltildi
   - Veri kalitesi: %100

#### 2. **Sıcaklık Kontrol Performansı**
   - 12 bölge analiz edildi
   - Ortalama kontrol başarısı: %81.5
   - En iyi: CEH.3 ALT1 (%95.9)
   - İyileştirme gereken: ÖN ISITMA (%38.2)

#### 3. **Ceh Dengesizlik Analizi**
   - CEH.1: 700.0°C
   - CEH.2: 837.6°C
   - CEH.3: 838.2°C
   - Maksimum fark: 138.2°C (⚠️ Yüksek)

#### 4. **Enerji Verimliliği**
   - Ortalama güç kullanımı: %36.9
   - Verimlilik skoru: 92.1/100
   - Durum: Düşük kapasite (artırılabilir)

#### 5. **Soğutma Sistemi**
   - Toplam soğutma: 204.2°C
   - Etkinlik: %100 (OPTIMAL)
   - Aşamalı soğutma: Dengeli ✅

#### 6. **Genel Performans**
   - **TOPLAM SKOR: 88.4/100 (İYİ ✅)**
   - Sıcaklık kontrolü: 40.8/50
   - Enerji verimliliği: 27.6/30
   - Soğutma etkinliği: 20.0/20

### 📁 Oluşturulan Dosyalar

```
data/processed/
├── firin_temiz.csv                    # Temizlenmiş veri
└── anomali_*.csv                      # Anomali detayları

reports/
├── figures/
│   ├── sicaklik_zaman_serisi.png     # 3 katmanlı sıcaklık analizi
│   ├── set_gercek_karsilastirma.png  # 4 bölge scatter plot
│   ├── ceh_dagilim_analizi.png       # 3 ceh box plot
│   ├── guc_amp_analizi.png           # Enerji trend ve dağılım
│   ├── sogutma_etkinligi.png         # 4'lü soğutma analizi
│   ├── anomali_haritasi.png          # Bölge bazlı anomaliler
│   ├── heatmap_korelasyon.png        # 8x8 korelasyon matrisi
│   └── performans_ozet_dashboard.png # 6 panel özet dashboard
├── firin_performans_raporu.json      # Detaylı JSON rapor
└── firin_ozet_rapor.txt              # İnsan okuyabilir özet
```

## 🔍 Temel Bulgular

### ⚠️ Kritik Sorunlar

1. **Ceh Dengesizliği** (Yüksek Öncelik)
   - Ceh bölmeleri arası 138.2°C fark
   - **Öneri:** Isıtma elemanları ve sensörler kontrol edilmeli
   - **Süre:** 4-6 saat

2. **Ön Isıtma Kontrol Sorunu** (Yüksek Öncelik)
   - Kontrol başarısı sadece %38.2
   - **Öneri:** Sensör ve ısıtıcı acil kontrolü
   - **Süre:** 4-6 saat

### ✅ Olumlu Bulgular

- Soğutma sistemi optimal çalışıyor (%100)
- Enerji verimliliği iyi (92.1/100)
- CEH.2 ve CEH.3 mükemmel performans
- Veri toplama tutarlı (%80)

## 🛠️ Teknoloji ve Metodoloji

### Kullanılan Kütüphaneler
- **pandas** - Veri manipülasyonu
- **numpy** - Matematiksel işlemler
- **matplotlib & seaborn** - Görselleştirme
- **openpyxl** - Excel okuma

### Analiz Yöntemleri
- **IQR (Interquartile Range)** - Aykırı değer tespiti
- **Interpolasyon** - Sensör hatalarının düzeltilmesi
- **Zaman serisi analizi** - Trend ve tutarlılık kontrolü
- **Korelasyon analizi** - Parametreler arası ilişkiler
- **Set-Gerçek karşılaştırma** - Kontrol performansı

### Performans Metrikleri
- Sıcaklık kontrol başarı oranı (12 bölge)
- Enerji verimlilik skoru (0-100)
- Soğutma etkinliği (ideal: 150-250°C)
- Ceh denge skoru (0-100)
- Operasyonel tutarlılık skoru (0-100)
- Genel performans skoru (ağırlıklı)

## 📈 Grafik ve Görselleştirmeler

### 1. **Sıcaklık Zaman Serisi** (3 katman)
   - Giriş ve ön ısıtma trendleri
   - Ceh bölmeleri sıcaklık değişimi
   - Soğutma sistemi performansı

### 2. **Set vs Gerçek Karşılaştırma** (4 bölge)
   - Scatter plot ile hedef-gerçek analizi
   - İdeal hat ve sapma gösterimi
   - Renk kodlu fark gösterimi

### 3. **Ceh Dağılım Analizi** (3 ceh)
   - Box plot ile sensör dağılımları
   - Her ceh için 4-5 sensör
   - Min, max, quartile değerleri

### 4. **Güç ve Enerji Analizi**
   - 6 bölge ortalama güç kullanımı
   - Günlük trend analizi
   - Bölge bazlı karşılaştırma

### 5. **Soğutma Etkinliği** (4 panel)
   - Soğutma sıcaklık trendi
   - Soğutma farkı analizi (Soğutma1-3)
   - Box plot dağılımı
   - Etkinlik histogram

### 6. **Anomali Haritası**
   - Bölge bazlı anomali sayıları
   - Yüzdelik dağılım
   - Öncelik bazlı renklendirme

### 7. **Korelasyon Isı Haritası** (8x8)
   - Sıcaklık parametreleri arası ilişki
   - -1 ile +1 arası korelasyon
   - Renk kodlu matris

### 8. **Performans Dashboard** (6 panel)
   - Bölge bazlı ortalama sıcaklıklar
   - Kontrol başarı oranı (pie chart)
   - Ana ceh trendleri
   - Güç kullanımı (box plot)
   - Soğutma etkinliği (histogram)
   - Sistem metrikleri (text)

## 🔧 Önleyici Bakım Sistemi

### Otomatik Öneri Sistemi

Sistem, performans metriklerine göre otomatik bakım önerileri üretir:

#### 🔴 Yüksek Öncelik
- Ceh bölmeleri arası >100°C fark
- Sıcaklık kontrol başarısı <%75
- Kritik sensör hataları

#### 🟠 Orta Öncelik
- Enerji verimliliği <%70
- Soğutma etkinliği <150°C veya >250°C
- Aşamalı soğutma dengesizliği

#### 🟡 Düşük Öncelik
- Kapasite kullanımı optimizasyonu
- Küçük sensör sapmaları
- İstatistiksel optimizasyonlar

### Bakım Takvimine Örnek

```
📅 Haftalık Kontroller:
   • Sensör kalibrasyonu (kritik bölgeler)
   • Veri toplama tutarlılık kontrolü

📅 Aylık Kontroller:
   • Tüm sensör kalibrasyonu
   • Isıtma elemanları kontrolü
   • Enerji tüketimi optimizasyonu

📅 3 Aylık Kontroller:
   • Ceh dengesizlik analizi
   • Soğutma sistemi kapsamlı bakım
   • Performans trend değerlendirmesi
```

## 📊 Veri Yapısı

### Ham Veri Formatı
- **Satır sayısı:** 38,792 kayıt
- **Sütun sayısı:** 58 (ham) → 69 (işlenmiş)
- **Tarih aralığı:** 60 gün
- **Kayıt sıklığı:** ~3-4 dakikada bir

### Sütun Kategorileri

#### 🌡️ Sıcaklık Sensörleri (30 adet)
```
• Giriş: GİRİŞ ISI
• Ön Isıtma: ÖN ISITMA SET ISI, ÖN ISITMA ISI
• Ceh 1: ÜST1, ÜST2, ALT1 (SET + ISI)
• Ceh 2: ÜST1, ÜST2, ALT1, ALT2 (SET + ISI)
• Ceh 3: ÜST1, ÜST2, ALT1, ALT2 (SET + ISI)
• Soğutma: SOĞUTMA1, SOĞUTMA2, SOĞUTMA3
```

#### ⚡ Güç ve Amper (18 adet)
```
• Her bölge için: GÜÇ %, AMP.
• Ön Isıtma: 1 çift
• Ceh 1: 3 çift
• Ceh 2: 4 çift
• Ceh 3: 4 çift
```

#### 🔄 Operasyonel
```
• PRG: Program numarası
• RULO FREKANS Hz
• GİRİŞ PER.FAN Hz
• ÇIKIŞ PER.FAN Hz
```

## 🎓 Öğrenilen Dersler

### Veri Kalitesi
- Sensör hataları (-3276 gibi) düzenli temizlenmeli
- Zaman serisi tutarlılığı kritik önemde
- Eksik değerler interpolasyon ile düzeltilebilir

### Fırın Operasyonu
- Ceh dengesi ürün kalitesi için kritik
- Ön ısıtma fazı en problemli alan
- Soğutma sistemi genelde stabil çalışıyor

### Enerji Optimizasyonu
- %50-70 güç kullanımı optimal
- Düşük kullanım = kapasite artırma fırsatı
- Yüksek kullanım = verimlilik sorunu

## 🔐 Güvenlik ve Uyarılar

⚠️ **Kritik Uyarılar:**
- Ceh arası >150°C fark acil müdahale gerektirir
- Ani sıcaklık değişimleri (>100°C/dakika) tehlikelidir
- Soğutma sistemi arızası ürün kalitesini etkiler

⚡ **Enerji Güvenliği:**
- Sürekli >90% güç kullanımı aşırı yüke işaret eder
- Tüm bölgelerin aynı anda yüksek güç çekmesi anormaldir

🔥 **Yangın Riski:**
- Set sıcaklıktan >100°C sapma risk oluşturur
- Ön ısıtma bölgesi düzenli kontrol edilmeli

## 👥 Proje Ekibi ve Katkılar

**Geliştirici:** Ilgın Uçum

**Proje Sahibi:** O&O Technology


## 📞 İletişim

- 📧 Email: cilgin.ucum@gmail.com
- 🔗 LinkedIn: [linkedin.com/in/ilginucum](https://linkedin.com/in/ilginucum)
- 💼 Şirket: O&O Technology

## 📝 Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.

## 🙏 Teşekkürler

O&O Technology için hazırlanmıştır.

---

## 📚 Ek Kaynaklar

### Dokümantasyon
- `/reports/firin_ozet_rapor.txt` - İnsan okuyabilir özet rapor
- `/reports/firin_performans_raporu.json` - Makine okuyabilir detaylı rapor

### Referans Projeler
- [Enjeksiyon Presi Analizi](https://github.com/ilginucum/enjeksiyon-presi-analizi) - Benzer metodoloji

### Faydalı Linkler
- [Endüstriyel Fırın Proses Akışı](docs/firin_proses_akisi.pdf)
- [Sıcaklık Kontrol Sistemleri](docs/sicaklik_kontrol.pdf)

