"""
Görselleştirme Modülü
Bu modül analiz sonuçlarını grafiklerle görselleştirir.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class Gorselestirici:
    """
    Veri görselleştirme işlemlerini gerçekleştiren sınıf
    """
    
    def __init__(self, df):
        """
        Args:
            df (pd.DataFrame): Görselleştirilecek DataFrame
        """
        self.df = df.copy()
        self.output_dir = 'reports/figures/'
        
        # Renk paleti
        self.colors = {
            'normal': '#2ecc71',      # Yeşil
            'anomali': '#e74c3c',     # Kırmızı
            'uyari': '#f39c12',       # Turuncu
            'bilgi': '#3498db'        # Mavi
        }
        
        # Grafik stili
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def zaman_serisi_grafigi(self):
        """
        Zaman serisi grafiklerini çizer (Dolum Zamanı, Basınç)
        """
        print("\n📈 Zaman Serisi Grafikleri Oluşturuluyor...")
        
        # Günlük ortalamalar
        gunluk = self.df.groupby(self.df['TARİH'].dt.date).agg({
            'KALIP DOLUM ZAMANI': 'mean',
            'PİSTON SÜRTÜNME BASINCI': 'mean',
            'SPESİFİK BASINÇ BAR': 'mean'
        })
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        fig.suptitle('Zaman Serisi Analizi - Günlük Ortalamalar', 
                     fontsize=16, fontweight='bold', y=0.995)
        
        # 1. Kalıp Dolum Zamanı
        axes[0].plot(gunluk.index, gunluk['KALIP DOLUM ZAMANI'], 
                    marker='o', linewidth=2.5, markersize=8,
                    color=self.colors['bilgi'], label='Dolum Zamanı')
        axes[0].axhline(y=gunluk['KALIP DOLUM ZAMANI'].mean(), 
                       color=self.colors['uyari'], linestyle='--', 
                       linewidth=2, label=f"Ortalama: {gunluk['KALIP DOLUM ZAMANI'].mean():.0f} ms")
        axes[0].set_ylabel('Süre (ms)', fontsize=12, fontweight='bold')
        axes[0].set_title('Kalıp Dolum Zamanı Trendi', fontsize=13, fontweight='bold')
        axes[0].legend(loc='best', fontsize=10)
        axes[0].grid(True, alpha=0.3)
        
        # 2. Piston Sürtünme Basıncı
        axes[1].plot(gunluk.index, gunluk['PİSTON SÜRTÜNME BASINCI'], 
                    marker='s', linewidth=2.5, markersize=8,
                    color=self.colors['anomali'], label='Sürtünme Basıncı')
        axes[1].axhline(y=gunluk['PİSTON SÜRTÜNME BASINCI'].mean(), 
                       color=self.colors['uyari'], linestyle='--', 
                       linewidth=2, label=f"Ortalama: {gunluk['PİSTON SÜRTÜNME BASINCI'].mean():.2f} bar")
        axes[1].set_ylabel('Basınç (bar)', fontsize=12, fontweight='bold')
        axes[1].set_title('Piston Sürtünme Basıncı Trendi', fontsize=13, fontweight='bold')
        axes[1].legend(loc='best', fontsize=10)
        axes[1].grid(True, alpha=0.3)
        
        # 3. Spesifik Basınç
        axes[2].plot(gunluk.index, gunluk['SPESİFİK BASINÇ BAR'], 
                    marker='^', linewidth=2.5, markersize=8,
                    color=self.colors['normal'], label='Spesifik Basınç')
        axes[2].axhline(y=gunluk['SPESİFİK BASINÇ BAR'].mean(), 
                       color=self.colors['uyari'], linestyle='--', 
                       linewidth=2, label=f"Ortalama: {gunluk['SPESİFİK BASINÇ BAR'].mean():.0f} bar")
        axes[2].set_xlabel('Tarih', fontsize=12, fontweight='bold')
        axes[2].set_ylabel('Basınç (bar)', fontsize=12, fontweight='bold')
        axes[2].set_title('Spesifik Basınç Trendi', fontsize=13, fontweight='bold')
        axes[2].legend(loc='best', fontsize=10)
        axes[2].grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}zaman_serisi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}zaman_serisi.png")
        plt.close()
    
    def dagilim_grafikleri(self):
        """
        Box plot ve histogram ile dağılım grafikleri
        """
        print("\n📊 Dağılım Grafikleri Oluşturuluyor...")
        
        parametreler = [
            'KALIP DOLUM ZAMANI',
            'PİSTON SÜRTÜNME BASINCI',
            'İKİNCİ FAZ HIZI',
            'SPESİFİK BASINÇ BAR'
        ]
        
        fig, axes = plt.subplots(2, 4, figsize=(18, 10))
        fig.suptitle('Parametre Dağılım Analizi', fontsize=16, fontweight='bold')
        
        for idx, param in enumerate(parametreler):
            # Box Plot
            sns.boxplot(y=self.df[param], ax=axes[0, idx], 
                       color=self.colors['bilgi'], width=0.5)
            axes[0, idx].set_title(f'{param}\nBox Plot', fontsize=11, fontweight='bold')
            axes[0, idx].set_ylabel('Değer', fontsize=10)
            axes[0, idx].grid(True, alpha=0.3, axis='y')
            
            # Histogram
            axes[1, idx].hist(self.df[param], bins=30, 
                            color=self.colors['normal'], alpha=0.7, edgecolor='black')
            axes[1, idx].axvline(self.df[param].mean(), 
                               color=self.colors['anomali'], linestyle='--', 
                               linewidth=2, label=f'Ort: {self.df[param].mean():.1f}')
            axes[1, idx].axvline(self.df[param].median(), 
                               color=self.colors['uyari'], linestyle='--', 
                               linewidth=2, label=f'Med: {self.df[param].median():.1f}')
            axes[1, idx].set_title(f'{param}\nHistogram', fontsize=11, fontweight='bold')
            axes[1, idx].set_xlabel('Değer', fontsize=10)
            axes[1, idx].set_ylabel('Frekans', fontsize=10)
            axes[1, idx].legend(fontsize=8)
            axes[1, idx].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}dagilim_grafikleri.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}dagilim_grafikleri.png")
        plt.close()
    
    def anomali_haritasi(self):
        """
        Anomali sayılarını gösteren bar chart
        """
        print("\n🗺️ Anomali Haritası Oluşturuluyor...")
        
        # Anomali sayılarını hesapla (IQR metodu)
        anomali_sayilari = {}
        
        parametreler = [
            'PİSTON SÜRTÜNME BASINCI',
            'KALIP DOLUM ZAMANI',
            'İKİNCİ FAZ HIZI',
            '3. FAZ BASINC YÜKSELME ZAMANI',
            'SPESİFİK BASINÇ BAR'
        ]
        
        for param in parametreler:
            Q1 = self.df[param].quantile(0.25)
            Q3 = self.df[param].quantile(0.75)
            IQR = Q3 - Q1
            
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            anomaliler = ((self.df[param] < lower) | (self.df[param] > upper)).sum()
            anomali_sayilari[param] = anomaliler
        
        # Grafik
        fig, ax = plt.subplots(figsize=(12, 7))
        
        params = list(anomali_sayilari.keys())
        counts = list(anomali_sayilari.values())
        colors_list = [self.colors['anomali'] if c > 50 else 
                      self.colors['uyari'] if c > 20 else 
                      self.colors['normal'] for c in counts]
        
        bars = ax.barh(params, counts, color=colors_list, edgecolor='black', linewidth=1.5)
        
        # Bar üzerine değer yaz
        for i, (bar, count) in enumerate(zip(bars, counts)):
            width = bar.get_width()
            ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
                   f'{count} adet\n({count/len(self.df)*100:.1f}%)',
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Anomali Sayısı', fontsize=12, fontweight='bold')
        ax.set_title('Parametre Bazlı Anomali Dağılımı', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Renk açıklaması
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['anomali'], label='Kritik (>50)'),
            Patch(facecolor=self.colors['uyari'], label='Orta (20-50)'),
            Patch(facecolor=self.colors['normal'], label='Düşük (<20)')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}anomali_haritasi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}anomali_haritasi.png")
        plt.close()
    
    def scatter_plot_analizi(self):
        """
        Parametreler arası ilişkiyi gösteren scatter plot
        """
        print("\n🔗 İlişki Grafikleri Oluşturuluyor...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle('Parametreler Arası İlişki Analizi', fontsize=16, fontweight='bold')
        
        # 1. Basınç vs Dolum Zamanı
        axes[0, 0].scatter(self.df['PİSTON SÜRTÜNME BASINCI'], 
                          self.df['KALIP DOLUM ZAMANI'],
                          alpha=0.5, s=30, c=self.colors['bilgi'])
        axes[0, 0].set_xlabel('Piston Sürtünme Basıncı (bar)', fontsize=10, fontweight='bold')
        axes[0, 0].set_ylabel('Kalıp Dolum Zamanı (ms)', fontsize=10, fontweight='bold')
        axes[0, 0].set_title('Basınç vs Dolum Zamanı', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Korelasyon hesapla
        corr1 = self.df['PİSTON SÜRTÜNME BASINCI'].corr(self.df['KALIP DOLUM ZAMANI'])
        axes[0, 0].text(0.05, 0.95, f'Korelasyon: {corr1:.3f}', 
                       transform=axes[0, 0].transAxes,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       fontsize=10, verticalalignment='top')
        
        # 2. Hız vs Dolum Zamanı
        axes[0, 1].scatter(self.df['İKİNCİ FAZ HIZI'], 
                          self.df['KALIP DOLUM ZAMANI'],
                          alpha=0.5, s=30, c=self.colors['normal'])
        axes[0, 1].set_xlabel('İkinci Faz Hızı (m/s)', fontsize=10, fontweight='bold')
        axes[0, 1].set_ylabel('Kalıp Dolum Zamanı (ms)', fontsize=10, fontweight='bold')
        axes[0, 1].set_title('Hız vs Dolum Zamanı', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        corr2 = self.df['İKİNCİ FAZ HIZI'].corr(self.df['KALIP DOLUM ZAMANI'])
        axes[0, 1].text(0.05, 0.95, f'Korelasyon: {corr2:.3f}', 
                       transform=axes[0, 1].transAxes,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       fontsize=10, verticalalignment='top')
        
        # 3. Basınç vs Spesifik Basınç
        axes[1, 0].scatter(self.df['PİSTON SÜRTÜNME BASINCI'], 
                          self.df['SPESİFİK BASINÇ BAR'],
                          alpha=0.5, s=30, c=self.colors['anomali'])
        axes[1, 0].set_xlabel('Piston Sürtünme Basıncı (bar)', fontsize=10, fontweight='bold')
        axes[1, 0].set_ylabel('Spesifik Basınç (bar)', fontsize=10, fontweight='bold')
        axes[1, 0].set_title('Sürtünme Basıncı vs Spesifik Basınç', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        corr3 = self.df['PİSTON SÜRTÜNME BASINCI'].corr(self.df['SPESİFİK BASINÇ BAR'])
        axes[1, 0].text(0.05, 0.95, f'Korelasyon: {corr3:.3f}', 
                       transform=axes[1, 0].transAxes,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       fontsize=10, verticalalignment='top')
        
        # 4. Basınç Yükselme vs Dolum Zamanı
        axes[1, 1].scatter(self.df['3. FAZ BASINC YÜKSELME ZAMANI'], 
                          self.df['KALIP DOLUM ZAMANI'],
                          alpha=0.5, s=30, c=self.colors['uyari'])
        axes[1, 1].set_xlabel('3. Faz Basınç Yükselme (ms)', fontsize=10, fontweight='bold')
        axes[1, 1].set_ylabel('Kalıp Dolum Zamanı (ms)', fontsize=10, fontweight='bold')
        axes[1, 1].set_title('Basınç Yükselme vs Dolum Zamanı', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        corr4 = self.df['3. FAZ BASINC YÜKSELME ZAMANI'].corr(self.df['KALIP DOLUM ZAMANI'])
        axes[1, 1].text(0.05, 0.95, f'Korelasyon: {corr4:.3f}', 
                       transform=axes[1, 1].transAxes,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                       fontsize=10, verticalalignment='top')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}iliski_grafikleri.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}iliski_grafikleri.png")
        plt.close()
    
    def gunluk_anomali_analizi(self):
        """
        Günlük anomali sayılarını gösteren grafik
        """
        print("\n📅 Günlük Anomali Analizi Oluşturuluyor...")
        
        # Her gün için anomali sayısını hesapla
        gunluk_anomali = []
        
        for tarih in self.df['TARİH'].dt.date.unique():
            gun_verisi = self.df[self.df['TARİH'].dt.date == tarih]
            
            # Basınç anomalileri
            Q1 = self.df['PİSTON SÜRTÜNME BASINCI'].quantile(0.25)
            Q3 = self.df['PİSTON SÜRTÜNME BASINCI'].quantile(0.75)
            IQR = Q3 - Q1
            basinc_anomali = ((gun_verisi['PİSTON SÜRTÜNME BASINCI'] < Q1 - 1.5*IQR) | 
                             (gun_verisi['PİSTON SÜRTÜNME BASINCI'] > Q3 + 1.5*IQR)).sum()
            
            # Dolum anomalileri
            Q1 = self.df['KALIP DOLUM ZAMANI'].quantile(0.25)
            Q3 = self.df['KALIP DOLUM ZAMANI'].quantile(0.75)
            IQR = Q3 - Q1
            dolum_anomali = ((gun_verisi['KALIP DOLUM ZAMANI'] < Q1 - 1.5*IQR) | 
                            (gun_verisi['KALIP DOLUM ZAMANI'] > Q3 + 1.5*IQR)).sum()
            
            toplam_uretim = len(gun_verisi)
            
            gunluk_anomali.append({
                'Tarih': tarih,
                'Basınç Anomali': basinc_anomali,
                'Dolum Anomali': dolum_anomali,
                'Toplam Üretim': toplam_uretim
            })
        
        gunluk_df = pd.DataFrame(gunluk_anomali)
        
        # Grafik
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle('Günlük Anomali Dağılımı', fontsize=16, fontweight='bold')
        
        # Stacked bar chart
        x = range(len(gunluk_df))
        ax1.bar(x, gunluk_df['Basınç Anomali'], label='Basınç Anomalisi', 
               color=self.colors['anomali'], edgecolor='black')
        ax1.bar(x, gunluk_df['Dolum Anomali'], bottom=gunluk_df['Basınç Anomali'],
               label='Dolum Anomalisi', color=self.colors['uyari'], edgecolor='black')
        ax1.set_ylabel('Anomali Sayısı', fontsize=12, fontweight='bold')
        ax1.set_title('Günlük Anomali Sayıları', fontsize=13, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels([str(t) for t in gunluk_df['Tarih']], rotation=45)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Anomali oranı
        gunluk_df['Anomali Oranı'] = ((gunluk_df['Basınç Anomali'] + gunluk_df['Dolum Anomali']) / 
                                       gunluk_df['Toplam Üretim'] * 100)
        
        ax2.plot(x, gunluk_df['Anomali Oranı'], marker='o', linewidth=2.5, 
                markersize=10, color=self.colors['anomali'])
        ax2.axhline(y=gunluk_df['Anomali Oranı'].mean(), color=self.colors['uyari'], 
                   linestyle='--', linewidth=2, label=f"Ortalama: {gunluk_df['Anomali Oranı'].mean():.1f}%")
        ax2.set_ylabel('Anomali Oranı (%)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Tarih', fontsize=12, fontweight='bold')
        ax2.set_title('Günlük Anomali Oranı Trendi', fontsize=13, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([str(t) for t in gunluk_df['Tarih']], rotation=45)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}gunluk_anomali.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}gunluk_anomali.png")
        plt.close()
    
    def tum_grafikleri_olustur(self):
        """
        Tüm grafikleri sırayla oluşturur
        """
        print("\n" + "🎨"*35)
        print("GÖRSELLEŞTİRME SÜRECİ BAŞLIYOR")
        print("🎨"*35)
        
        self.zaman_serisi_grafigi()
        self.dagilim_grafikleri()
        self.anomali_haritasi()
        self.scatter_plot_analizi()
        self.gunluk_anomali_analizi()
        
        print("\n" + "="*70)
        print("✅ TÜM GRAFİKLER OLUŞTURULDU!")
        print("="*70)
        print(f"\n📁 Grafikler şu klasörde: {self.output_dir}")
        print("\nOluşturulan Grafikler:")
        print("  1. zaman_serisi.png - Zaman serisi trendleri")
        print("  2. dagilim_grafikleri.png - Box plot ve histogramlar")
        print("  3. anomali_haritasi.png - Anomali dağılımı")
        print("  4. iliski_grafikleri.png - Parametreler arası ilişkiler")
        print("  5. gunluk_anomali.png - Günlük anomali analizi")


# Test için
if __name__ == "__main__":
    # Temizlenmiş veriyi yükle
    df = pd.read_csv('data/processed/enjeksiyon_temiz.csv')
    df['TARİH'] = pd.to_datetime(df['TARİH'])
    
    print(f"✅ Temizlenmiş veri yüklendi: {len(df)} satır")
    
    # Görselleştirici oluştur
    gorselestirici = Gorselestirici(df)
    
    # Tüm grafikleri oluştur
    gorselestirici.tum_grafikleri_olustur()