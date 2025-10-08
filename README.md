# 🏭 Fabrika Üretim Hattı Veri Analiz Sistemi

O&O Technology fabrikasının üretim hattındaki makinelerin operasyonel verilerini analiz eden kapsamlı veri analiz platformu.

**🎯 Proje Durumu:** ✅ Tamamlandı

**📊 Toplam Analiz Edilen Veri:** 41,422 kayıt

**🔬 Analiz Edilen Makine:** 2 adet (Enjeksiyon Presi + Endüstriyel Fırın)

**📅 Toplam Analiz Süresi:** 67 gün

---

## 📦 İçindekiler

### 1. 🔧 [Enjeksiyon Presi Analizi](enjeksiyon-presi/)

**520 Ton Enjeksiyon Presi** makinasının veri analizi ve anomali tespiti.

- **📊 Veri:** 2,630 üretim kaydı (7 gün)
- **⚠️ Anomali:** 248 adet tespit edildi (%9.4)
- **🎯 Kalite Oranı:** %92.9
- **⚙️ Makine Sağlık Skoru:** 67.6/100 (ORTA 🟠)
- **📈 Grafik:** 5 adet profesyonel görselleştirme

**Kritik Bulgular:**
- ⚠️ Piston basıncı anomalisi: 155 adet
- ⚠️ Valf sistemi acil kontrol gerekli
- ✅ Çevrim süresi hedefe yakın (1.58s)

**[📄 Detaylı README](enjeksiyon-presi/README.md)**

---

### 2. 🔥 [Fırın Verileri Analizi](firin-verileri/)

**3 Bölmeli Endüstriyel Fırın** sıcaklık kontrolü ve performans analizi.

- **📊 Veri:** 38,792 sıcaklık kaydı (60 gün)
- **🌡️ Sensör:** 30 sıcaklık sensörü, 18 güç ölçüm noktası
- **⚡ Genel Performans:** 88.4/100 (İYİ ✅)
- **🎯 Sıcaklık Kontrol Başarısı:** %81.5
- **❄️ Soğutma Etkinliği:** %100 (OPTIMAL)
- **📈 Grafik:** 8 adet detaylı görselleştirme

**Kritik Bulgular:**
- ⚠️ Ceh dengesizliği: 138.2°C fark (acil müdahale)
- ⚠️ Ön ısıtma kontrol sorunu: %38.2 başarı
- ✅ Enerji verimliliği iyi: 92.1/100
- ✅ Soğutma sistemi optimal çalışıyor

**[📄 Detaylı README](firin-verileri/README.md)**

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- pandas, numpy, matplotlib, seaborn
- openpyxl (Excel okuma)

### Kurulum

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/ilginucum/fabrika-uretim-analizi.git
cd fabrika-uretim-analizi
```

2. **Gerekli kütüphaneleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Her proje için ayrı ayrı analiz çalıştırın:**

**Enjeksiyon Presi:**
```bash
cd enjeksiyon-presi
python src/veri_yukleme.py
python src/veri_temizleme.py
python src/anomali_tespiti.py
python src/performans_analizi.py
python src/gorsellestirme.py
```

**Fırın Verileri:**
```bash
cd firin-verileri
python src/veri_yukleme.py
python src/veri_temizleme.py
python src/anomali_tespiti.py
python src/performans_analizi.py
python src/gorsellestirme.py
python src/ozet_rapor.py
```

---

## 📊 Proje Yapısı

```
fabrika-uretim-analizi/
│
├── enjeksiyon-presi/              # Enjeksiyon presi analizi
│   ├── data/
│   │   ├── raw/                   # 520TonEnjPres.xlsx
│   │   └── processed/             # Temizlenmiş veriler
│   ├── src/                       # Python modülleri
│   │   ├── veri_yukleme.py
│   │   ├── veri_temizleme.py
│   │   ├── anomali_tespiti.py
│   │   ├── performans_analizi.py
│   │   └── gorsellestirme.py
│   ├── reports/                   # Raporlar ve grafikler
│   │   ├── figures/               # 5 adet grafik
│   │   ├── performans_raporu.json
│   │   └── ozet_rapor.txt
│   └── README.md
│
├── firin-verileri/                # Fırın analizi
│   ├── data/
│   │   ├── raw/                   # Fırın Verileri18.xlsx
│   │   └── processed/             # Temizlenmiş veriler
│   ├── src/                       # Python modülleri
│   │   ├── veri_yukleme.py
│   │   ├── veri_temizleme.py
│   │   ├── anomali_tespiti.py
│   │   ├── performans_analizi.py
│   │   ├── gorsellestirme.py
│   │   └── ozet_rapor.py
│   ├── reports/                   # Raporlar ve grafikler
│   │   ├── figures/               # 8 adet grafik
│   │   ├── firin_performans_raporu.json
│   │   └── firin_ozet_rapor.txt
│   └── README.md
│
├── requirements.txt               # Tüm bağımlılıklar
└── README.md                      # Bu dosya
```

---

## 🔍 Karşılaştırmalı Analiz

| Metrik | Enjeksiyon Presi | Endüstriyel Fırın |
|--------|------------------|-------------------|
| **Veri Miktarı** | 2,630 kayıt | 38,792 kayıt |
| **Analiz Süresi** | 7 gün | 60 gün |
| **Genel Sağlık Skoru** | 67.6/100 (ORTA) | 88.4/100 (İYİ) |
| **Tespit Edilen Anomali** | 248 (%9.4) | ~18,000 (%46.4) |
| **Kritik Öneri** | 2 adet | 2 adet |
| **Grafik Sayısı** | 5 adet | 8 adet |
| **İzlenen Parametre** | 13 sütun | 69 sütun |

---

## 🎯 Ana Bulgular ve Öneriler

### 🔧 Enjeksiyon Presi

**Güçlü Yönler:**
- ✅ Kalite oranı hedefine yakın (%92.9)
- ✅ Çevrim süresi optimal (1.58s)
- ✅ Dolum zamanı iyileşiyor

**İyileştirme Alanları:**
- 🔴 **Acil:** Valf sistemi kontrolü (90 basınç yükselme problemi)
- 🟠 **Orta:** Hidrolik sistem bakımı (155 basınç anomalisi)
- 🟡 **Düşük:** Verimlilik optimizasyonu (%0.7)

### 🔥 Endüstriyel Fırın

**Güçlü Yönler:**
- ✅ Soğutma sistemi mükemmel (%100)
- ✅ Enerji verimliliği yüksek (92.1/100)
- ✅ CEH.2 ve CEH.3 optimal çalışıyor

**İyileştirme Alanları:**
- 🔴 **Acil:** Ceh dengesizliği (138.2°C fark, 4-6 saat bakım)
- 🔴 **Acil:** Ön ısıtma sensör/ısıtıcı kontrolü (4-6 saat)
- 🟡 **Düşük:** Kapasite kullanımı artırılabilir

---

## 🛠️ Teknoloji Stack

### Veri İşleme
- **pandas** - Veri manipülasyonu ve analiz
- **numpy** - Matematiksel işlemler ve array operasyonları
- **openpyxl** - Excel dosyaları okuma

### Görselleştirme
- **matplotlib** - Temel grafikler ve plot'lar
- **seaborn** - İstatistiksel görselleştirme

### Analiz Yöntemleri
- **IQR (Interquartile Range)** - Aykırı değer tespiti
- **Z-score** analizi - Standart sapma bazlı anomali
- **Interpolasyon** - Eksik/hatalı veri düzeltme
- **Zaman serisi analizi** - Trend ve pattern tespiti
- **Korelasyon analizi** - Parametre ilişkileri

---

## 📈 Görselleştirmeler

### Enjeksiyon Presi (5 Grafik)
1. **Zaman Serisi** - Dolum zamanı, basınç ve spesifik basınç trendleri
2. **Dağılım Grafikleri** - Box plot ve histogram (4 parametre)
3. **Anomali Haritası** - Parametre bazlı anomali dağılımı
4. **İlişki Grafikleri** - 4 scatter plot ile korelasyon
5. **Günlük Anomali** - Stacked bar ve trend analizi

### Endüstriyel Fırın (8 Grafik)
1. **Sıcaklık Zaman Serisi** - 3 katmanlı (Giriş, Ceh, Soğutma)
2. **Set vs Gerçek Karşılaştırma** - 4 bölge scatter plot
3. **Ceh Dağılım Analizi** - 3 ceh box plot karşılaştırma
4. **Güç ve Amper Analizi** - Enerji trend ve dağılım
5. **Soğutma Etkinliği** - 4 panel detaylı analiz
6. **Anomali Haritası** - Bölge bazlı horizontal bar
7. **Korelasyon Heatmap** - 8x8 sıcaklık parametresi
8. **Performans Dashboard** - 6 panel özet gösterge

---

## 📊 Çıktı Formatları

### Raporlar
- **JSON** - Makine okuyabilir detaylı metrikler
- **TXT** - İnsan okuyabilir özet raporlar
- **CSV** - Temizlenmiş veri setleri
- **PNG** - Yüksek çözünürlüklü grafikler (300 DPI)

### Veri Akışı
```
Excel Dosyası → Veri Yükleme → Temizleme → Anomali Tespiti
                                              ↓
                  Görselleştirme ← Performans Analizi
                        ↓
              Raporlar (JSON/TXT/PNG)
```

---

## 🎓 Öğrenilen Dersler

### Veri Kalitesi
- Sensör hataları düzenli temizlenmeli (-3276 gibi değerler)
- Zaman serisi tutarlılığı kritik
- Eksik değerler interpolasyon ile düzeltilebilir

### Makine Operasyonu
- Düzenli bakım anomali sayısını azaltır
- Erken uyarı sistemleri maliyet tasarrufu sağlar
- Veri odaklı kararlar üretim kalitesini artırır

### Performans Optimizasyonu
- Parametre izleme gerçek zamanlı olmalı
- Eşik değerler makine tipine göre özelleştirilmeli
- Görselleştirme operatör kararlarını hızlandırır

---

## 🔐 Güvenlik ve Uyarılar

### ⚠️ Kritik Uyarılar

**Enjeksiyon Presi:**
- Basınç yükselme >10 saniye = acil durdurma
- Piston basınç >10 bar = hidrolik risk
- Dolum zamanı >1500 ms = kalite sorunu

**Fırın:**
- Ceh arası >150°C fark = acil müdahale
- Ani sıcaklık değişimi >100°C/dk = tehlike
- Soğutma arızası = ürün kalitesi riski

---

## 👥 Proje Ekibi

**Geliştirici:** Ilgın Uçum
- 📧 Email: cilgin.ucum@gmail.com
- 💼 LinkedIn: [linkedin.com/in/ilginucum](https://linkedin.com/in/ilginucum)

**Proje Sahibi:** O&O Technology

---

## 📝 Lisans

Bu proje eğitim ve portföy amaçlı geliştirilmiştir.

---

## 🙏 Teşekkürler

O&O Technology fabrikasına veri sağladığı ve bu projeye katkıda bulunduğu için teşekkür ederiz.

