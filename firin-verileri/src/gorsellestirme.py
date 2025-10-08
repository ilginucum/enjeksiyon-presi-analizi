"""
Fırın Verileri Görselleştirme Modülü
Bu modül fırın analiz sonuçlarını grafiklerle görselleştirir.
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

class FirinGorselestirici:
    """
    Fırın veri görselleştirme işlemlerini gerçekleştiren sınıf
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
            'bilgi': '#3498db',       # Mavi
            'mor': '#9b59b6',         # Mor
            'turkuaz': '#1abc9c'      # Turkuaz
        }
        
        # Grafik stili
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def sicaklik_zaman_serisi(self):
        """
        Tüm sıcaklık sensörlerinin zaman serisi grafiği
        """
        print("\n🌡️ Sıcaklık Zaman Serisi Grafikleri Oluşturuluyor...")
        
        # Günlük ortalamalar
        gunluk = self.df.groupby(self.df['TARİH'].dt.date).agg({
            'GİRİŞ ISI': 'mean',
            'ÖN ISITMA ISI': 'mean',
            'CEH.1 ÜST1 ISI': 'mean',
            'CEH.2 ÜST1 ISI': 'mean',
            'CEH.3 ÜST1 ISI': 'mean',
            'SOĞUTMA1 ISI': 'mean',
            'SOĞUTMA2 ISI': 'mean',
            'SOĞUTMA3 ISI': 'mean'
        })
        
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))
        fig.suptitle('Fırın Sıcaklık Zaman Serisi Analizi', 
                     fontsize=18, fontweight='bold', y=0.995)
        
        # 1. Giriş ve Ön Isıtma
        axes[0].plot(gunluk.index, gunluk['GİRİŞ ISI'], 
                    marker='o', linewidth=2.5, markersize=8,
                    color=self.colors['bilgi'], label='Giriş Isı')
        axes[0].plot(gunluk.index, gunluk['ÖN ISITMA ISI'], 
                    marker='s', linewidth=2.5, markersize=8,
                    color=self.colors['uyari'], label='Ön Isıtma')
        axes[0].set_ylabel('Sıcaklık (°C)', fontsize=12, fontweight='bold')
        axes[0].set_title('Giriş ve Ön Isıtma Sıcaklıkları', fontsize=14, fontweight='bold')
        axes[0].legend(loc='best', fontsize=11)
        axes[0].grid(True, alpha=0.3)
        
        # 2. Ceh Sıcaklıkları
        axes[1].plot(gunluk.index, gunluk['CEH.1 ÜST1 ISI'], 
                    marker='o', linewidth=2.5, markersize=8,
                    color=self.colors['normal'], label='Ceh.1 Üst')
        axes[1].plot(gunluk.index, gunluk['CEH.2 ÜST1 ISI'], 
                    marker='s', linewidth=2.5, markersize=8,
                    color=self.colors['anomali'], label='Ceh.2 Üst')
        axes[1].plot(gunluk.index, gunluk['CEH.3 ÜST1 ISI'], 
                    marker='^', linewidth=2.5, markersize=8,
                    color=self.colors['mor'], label='Ceh.3 Üst')
        axes[1].axhline(y=gunluk[['CEH.1 ÜST1 ISI', 'CEH.2 ÜST1 ISI', 'CEH.3 ÜST1 ISI']].mean().mean(), 
                       color='black', linestyle='--', linewidth=2, 
                       label=f"Ortalama: {gunluk[['CEH.1 ÜST1 ISI', 'CEH.2 ÜST1 ISI', 'CEH.3 ÜST1 ISI']].mean().mean():.0f}°C")
        axes[1].set_ylabel('Sıcaklık (°C)', fontsize=12, fontweight='bold')
        axes[1].set_title('Ceh Bölmeleri Sıcaklıkları', fontsize=14, fontweight='bold')
        axes[1].legend(loc='best', fontsize=11)
        axes[1].grid(True, alpha=0.3)
        
        # 3. Soğutma Sıcaklıkları
        axes[2].plot(gunluk.index, gunluk['SOĞUTMA1 ISI'], 
                    marker='o', linewidth=2.5, markersize=8,
                    color=self.colors['anomali'], label='Soğutma 1')
        axes[2].plot(gunluk.index, gunluk['SOĞUTMA2 ISI'], 
                    marker='s', linewidth=2.5, markersize=8,
                    color=self.colors['uyari'], label='Soğutma 2')
        axes[2].plot(gunluk.index, gunluk['SOĞUTMA3 ISI'], 
                    marker='^', linewidth=2.5, markersize=8,
                    color=self.colors['turkuaz'], label='Soğutma 3')
        axes[2].set_xlabel('Tarih', fontsize=12, fontweight='bold')
        axes[2].set_ylabel('Sıcaklık (°C)', fontsize=12, fontweight='bold')
        axes[2].set_title('Soğutma Sistemi Sıcaklıkları', fontsize=14, fontweight='bold')
        axes[2].legend(loc='best', fontsize=11)
        axes[2].grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}sicaklik_zaman_serisi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}sicaklik_zaman_serisi.png")
        plt.close()
    
    def set_gercek_karsilastirma(self):
        """
        Set sıcaklık vs Gerçek sıcaklık karşılaştırması
        """
        print("\n🎯 Set vs Gerçek Sıcaklık Karşılaştırması Oluşturuluyor...")
        
        # Önemli bölgeleri seç
        bolumler = [
            ('ÖN ISITMA', 'ÖN ISITMA SET ISI', 'ÖN ISITMA ISI'),
            ('CEH.1 ÜST1', 'CEH.1 ÜST1 SET ISI', 'CEH.1 ÜST1 ISI'),
            ('CEH.2 ÜST1', 'CEH.2 ÜST1 SET ISI', 'CEH.2 ÜST1 ISI'),
            ('CEH.3 ÜST1', 'CEH.3 ÜST1 SET ISI', 'CEH.3 ÜST1 ISI')
        ]
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Set Sıcaklık vs Gerçek Sıcaklık Karşılaştırması', 
                     fontsize=18, fontweight='bold')
        axes = axes.flatten()
        
        for idx, (isim, set_col, gercek_col) in enumerate(bolumler):
            # Fark hesapla
            fark = abs(self.df[set_col] - self.df[gercek_col])
            
            # Scatter plot
            scatter = axes[idx].scatter(self.df[set_col], self.df[gercek_col],
                                       c=fark, cmap='RdYlGn_r', alpha=0.6, s=30)
            
            # İdeal çizgi (45 derece)
            min_val = min(self.df[set_col].min(), self.df[gercek_col].min())
            max_val = max(self.df[set_col].max(), self.df[gercek_col].max())
            axes[idx].plot([min_val, max_val], [min_val, max_val], 
                          'r--', linewidth=2, label='İdeal Hat')
            
            axes[idx].set_xlabel(f'Set Sıcaklık (°C)', fontsize=11, fontweight='bold')
            axes[idx].set_ylabel(f'Gerçek Sıcaklık (°C)', fontsize=11, fontweight='bold')
            axes[idx].set_title(f'{isim}\nOrt. Fark: {fark.mean():.1f}°C', 
                              fontsize=12, fontweight='bold')
            axes[idx].legend(fontsize=9)
            axes[idx].grid(True, alpha=0.3)
            
            # Colorbar
            cbar = plt.colorbar(scatter, ax=axes[idx])
            cbar.set_label('Fark (°C)', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}set_gercek_karsilastirma.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}set_gercek_karsilastirma.png")
        plt.close()
    
    def ceh_dagilim_analizi(self):
        """
        Ceh bölmeleri sıcaklık dağılımı
        """
        print("\n📊 Ceh Dağılım Analizi Oluşturuluyor...")
        
        # 3 Ceh'in tüm sensörleri
        ceh1_cols = [col for col in self.df.columns if 'CEH.1' in col and 'ISI' in col and 'SET' not in col]
        ceh2_cols = [col for col in self.df.columns if 'CEH.2' in col and 'ISI' in col and 'SET' not in col]
        ceh3_cols = [col for col in self.df.columns if 'CEH.3' in col and 'ISI' in col and 'SET' not in col]
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Ceh Bölmeleri Sıcaklık Dağılımı', fontsize=18, fontweight='bold')
        
        # Ceh 1
        data1 = [self.df[col].values for col in ceh1_cols]
        bp1 = axes[0].boxplot(data1, labels=[col.replace('CEH.1 ', '') for col in ceh1_cols],
                             patch_artist=True)
        for patch in bp1['boxes']:
            patch.set_facecolor(self.colors['normal'])
        axes[0].set_title('Ceh 1 Sensörleri', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Sıcaklık (°C)', fontsize=12, fontweight='bold')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Ceh 2
        data2 = [self.df[col].values for col in ceh2_cols]
        bp2 = axes[1].boxplot(data2, labels=[col.replace('CEH.2 ', '') for col in ceh2_cols],
                             patch_artist=True)
        for patch in bp2['boxes']:
            patch.set_facecolor(self.colors['anomali'])
        axes[1].set_title('Ceh 2 Sensörleri', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Sıcaklık (°C)', fontsize=12, fontweight='bold')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(True, alpha=0.3, axis='y')
        
        # Ceh 3
        data3 = [self.df[col].values for col in ceh3_cols]
        bp3 = axes[2].boxplot(data3, labels=[col.replace('CEH.3 ', '') for col in ceh3_cols],
                             patch_artist=True)
        for patch in bp3['boxes']:
            patch.set_facecolor(self.colors['mor'])
        axes[2].set_title('Ceh 3 Sensörleri', fontsize=14, fontweight='bold')
        axes[2].set_ylabel('Sıcaklık (°C)', fontsize=12, fontweight='bold')
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}ceh_dagilim_analizi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}ceh_dagilim_analizi.png")
        plt.close()
    
    def guc_amp_analizi(self):
        """
        Güç yüzdesi ve amper analizi
        """
        print("\n⚡ Güç ve Amper Analizi Oluşturuluyor...")
        
        guc_cols = [col for col in self.df.columns if 'GÜÇ %' in col]
        amp_cols = [col for col in self.df.columns if 'AMP.' in col]
        
        # Günlük ortalamalar
        gunluk = self.df.groupby(self.df['TARİH'].dt.date).agg({
            col: 'mean' for col in guc_cols[:4]
        })
        
        fig, axes = plt.subplots(2, 1, figsize=(16, 10))
        fig.suptitle('Enerji Tüketimi Analizi', fontsize=18, fontweight='bold')
        
        # 1. Güç Yüzdesi Trend
        for idx, col in enumerate(guc_cols[:4]):
            axes[0].plot(gunluk.index, gunluk[col], 
                        marker='o', linewidth=2.5, markersize=8,
                        label=col.replace(' GÜÇ %', ''))
        axes[0].set_ylabel('Güç (%)', fontsize=12, fontweight='bold')
        axes[0].set_title('Bölge Bazlı Güç Kullanımı Trendi', fontsize=14, fontweight='bold')
        axes[0].legend(loc='best', fontsize=10, ncol=2)
        axes[0].grid(True, alpha=0.3)
        
        # 2. Toplam Enerji Dağılımı
        ortalama_guc = [self.df[col].mean() for col in guc_cols[:6]]
        bolge_isimleri = [col.replace(' GÜÇ %', '') for col in guc_cols[:6]]
        
        bars = axes[1].bar(range(len(ortalama_guc)), ortalama_guc, 
                          color=[self.colors['normal'], self.colors['anomali'], 
                                self.colors['mor'], self.colors['bilgi'],
                                self.colors['uyari'], self.colors['turkuaz']])
        axes[1].set_xlabel('Bölge', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Ortalama Güç (%)', fontsize=12, fontweight='bold')
        axes[1].set_title('Bölge Bazlı Ortalama Güç Kullanımı', fontsize=14, fontweight='bold')
        axes[1].set_xticks(range(len(bolge_isimleri)))
        axes[1].set_xticklabels(bolge_isimleri, rotation=45, ha='right')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        # Bar üzerine değer yaz
        for bar, val in zip(bars, ortalama_guc):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{val:.1f}%',
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}guc_amp_analizi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}guc_amp_analizi.png")
        plt.close()
    
    def sogutma_etkinligi(self):
        """
        Soğutma sistemi etkinlik analizi
        """
        print("\n❄️ Soğutma Sistemi Analizi Oluşturuluyor...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Soğutma Sistemi Performans Analizi', fontsize=18, fontweight='bold')
        
        # 1. Soğutma Trendi
        gunluk = self.df.groupby(self.df['TARİH'].dt.date).agg({
            'SOĞUTMA1 ISI': 'mean',
            'SOĞUTMA2 ISI': 'mean',
            'SOĞUTMA3 ISI': 'mean'
        })
        
        axes[0, 0].plot(gunluk.index, gunluk['SOĞUTMA1 ISI'], 
                       marker='o', linewidth=2.5, color=self.colors['anomali'], label='Soğutma 1')
        axes[0, 0].plot(gunluk.index, gunluk['SOĞUTMA2 ISI'], 
                       marker='s', linewidth=2.5, color=self.colors['uyari'], label='Soğutma 2')
        axes[0, 0].plot(gunluk.index, gunluk['SOĞUTMA3 ISI'], 
                       marker='^', linewidth=2.5, color=self.colors['turkuaz'], label='Soğutma 3')
        axes[0, 0].set_ylabel('Sıcaklık (°C)', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Soğutma Sıcaklık Trendi', fontsize=12, fontweight='bold')
        axes[0, 0].legend(fontsize=10)
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Soğutma Farkı
        self.df['SOGUTMA_FARKI'] = self.df['SOĞUTMA1 ISI'] - self.df['SOĞUTMA3 ISI']
        gunluk_fark = self.df.groupby(self.df['TARİH'].dt.date)['SOGUTMA_FARKI'].mean()
        
        axes[0, 1].plot(gunluk_fark.index, gunluk_fark.values, 
                       marker='o', linewidth=2.5, markersize=8, color=self.colors['bilgi'])
        axes[0, 1].axhline(y=gunluk_fark.mean(), color=self.colors['uyari'], 
                          linestyle='--', linewidth=2, 
                          label=f'Ortalama: {gunluk_fark.mean():.1f}°C')
        axes[0, 1].set_ylabel('Sıcaklık Farkı (°C)', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Soğutma Etkinliği (Soğutma1 - Soğutma3)', fontsize=12, fontweight='bold')
        axes[0, 1].legend(fontsize=10)
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Dağılım
        sogutma_data = [self.df['SOĞUTMA1 ISI'], self.df['SOĞUTMA2 ISI'], self.df['SOĞUTMA3 ISI']]
        bp = axes[1, 0].boxplot(sogutma_data, labels=['Soğutma 1', 'Soğutma 2', 'Soğutma 3'],
                               patch_artist=True)
        colors_box = [self.colors['anomali'], self.colors['uyari'], self.colors['turkuaz']]
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
        axes[1, 0].set_ylabel('Sıcaklık (°C)', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Soğutma Sıcaklık Dağılımı', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Histogram
        axes[1, 1].hist(self.df['SOGUTMA_FARKI'], bins=50, 
                       color=self.colors['bilgi'], alpha=0.7, edgecolor='black')
        axes[1, 1].axvline(self.df['SOGUTMA_FARKI'].mean(), 
                          color=self.colors['anomali'], linestyle='--', linewidth=2,
                          label=f'Ortalama: {self.df["SOGUTMA_FARKI"].mean():.1f}°C')
        axes[1, 1].set_xlabel('Sıcaklık Farkı (°C)', fontsize=11, fontweight='bold')
        axes[1, 1].set_ylabel('Frekans', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Soğutma Etkinliği Dağılımı', fontsize=12, fontweight='bold')
        axes[1, 1].legend(fontsize=10)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}sogutma_etkinligi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}sogutma_etkinligi.png")
        plt.close()
    
    def anomali_haritasi(self):
        """
        Tespit edilen anomalilerin görselleştirilmesi
        """
        print("\n🗺️ Anomali Haritası Oluşturuluyor...")
        
        # Anomali tiplerini say
        anomali_tipleri = {}
        
        if 'SICAKLIK_KONTROL_FARK' in self.df.columns:
            for col in self.df.columns:
                if col.startswith('SICAKLIK_KONTROL_'):
                    bolge = col.replace('SICAKLIK_KONTROL_', '')
                    if bolge != 'FARK':
                        anomali_sayisi = self.df[col].sum() if self.df[col].dtype == bool else 0
                        if anomali_sayisi > 0:
                            anomali_tipleri[bolge] = anomali_sayisi
        
        if not anomali_tipleri:
            print("⚠️ Anomali sütunları bulunamadı, manuel hesaplama yapılıyor...")
            # Manuel hesaplama
            set_gercek_pairs = [
                ('ÖN ISITMA', 'ÖN ISITMA SET ISI', 'ÖN ISITMA ISI'),
                ('CEH.1 ÜST1', 'CEH.1 ÜST1 SET ISI', 'CEH.1 ÜST1 ISI'),
                ('CEH.2 ÜST1', 'CEH.2 ÜST1 SET ISI', 'CEH.2 ÜST1 ISI'),
                ('CEH.3 ÜST1', 'CEH.3 ÜST1 SET ISI', 'CEH.3 ÜST1 ISI'),
            ]
            
            for isim, set_col, gercek_col in set_gercek_pairs:
                fark = abs(self.df[set_col] - self.df[gercek_col])
                anomali_sayisi = (fark > 50).sum()
                if anomali_sayisi > 0:
                    anomali_tipleri[isim] = anomali_sayisi
        
        if not anomali_tipleri:
            print("⚠️ Anomali verisi bulunamadı!")
            return
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        bolumler = list(anomali_tipleri.keys())
        sayilar = list(anomali_tipleri.values())
        
        # Renk seç (kritik seviyeye göre)
        colors_list = [self.colors['anomali'] if s > 1000 else 
                      self.colors['uyari'] if s > 500 else 
                      self.colors['normal'] for s in sayilar]
        
        bars = ax.barh(bolumler, sayilar, color=colors_list, edgecolor='black', linewidth=1.5)
        
        # Bar üzerine değer ve yüzde yaz
        for bar, sayi in zip(bars, sayilar):
            width = bar.get_width()
            yuzde = (sayi / len(self.df)) * 100
            ax.text(width + max(sayilar)*0.01, bar.get_y() + bar.get_height()/2,
                   f'{sayi} adet\n({yuzde:.1f}%)',
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Anomali Sayısı', fontsize=12, fontweight='bold')
        ax.set_title('Bölge Bazlı Sıcaklık Kontrol Anomalisi Dağılımı', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Renk açıklaması
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['anomali'], label='Kritik (>1000)'),
            Patch(facecolor=self.colors['uyari'], label='Orta (500-1000)'),
            Patch(facecolor=self.colors['normal'], label='Düşük (<500)')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}anomali_haritasi.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}anomali_haritasi.png")
        plt.close()
    
    def heatmap_korelasyon(self):
        """
        Önemli parametreler arası korelasyon ısı haritası
        """
        print("\n🔥 Korelasyon Isı Haritası Oluşturuluyor...")
        
        # Önemli sıcaklık parametrelerini seç
        onemli_cols = [
            'GİRİŞ ISI',
            'ÖN ISITMA ISI',
            'CEH.1 ÜST1 ISI',
            'CEH.2 ÜST1 ISI',
            'CEH.3 ÜST1 ISI',
            'SOĞUTMA1 ISI',
            'SOĞUTMA2 ISI',
            'SOĞUTMA3 ISI'
        ]
        
        # Korelasyon matrisi
        corr_matrix = self.df[onemli_cols].corr()
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn',
                   center=0, square=True, linewidths=1,
                   cbar_kws={"shrink": 0.8}, ax=ax,
                   vmin=-1, vmax=1)
        
        ax.set_title('Sıcaklık Parametreleri Korelasyon Matrisi', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Sütun isimlerini kısalt
        kisaltilmis = [col.replace(' ISI', '').replace('CEH.', 'C') 
                      for col in onemli_cols]
        ax.set_xticklabels(kisaltilmis, rotation=45, ha='right')
        ax.set_yticklabels(kisaltilmis, rotation=0)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}heatmap_korelasyon.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}heatmap_korelasyon.png")
        plt.close()
    
    def performans_ozet_dashboard(self):
        """
        Genel performans özeti dashboard
        """
        print("\n📊 Performans Özet Dashboard Oluşturuluyor...")
        
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        fig.suptitle('Fırın Performans Özet Dashboard', fontsize=20, fontweight='bold')
        
        # 1. Ortalama Sıcaklıklar (Bar)
        ax1 = fig.add_subplot(gs[0, :2])
        ortalama_sicakliklar = {
            'Giriş': self.df['GİRİŞ ISI'].mean(),
            'Ön Isıtma': self.df['ÖN ISITMA ISI'].mean(),
            'Ceh 1': self.df['CEH.1 ÜST1 ISI'].mean(),
            'Ceh 2': self.df['CEH.2 ÜST1 ISI'].mean(),
            'Ceh 3': self.df['CEH.3 ÜST1 ISI'].mean(),
            'Soğutma 1': self.df['SOĞUTMA1 ISI'].mean(),
            'Soğutma 2': self.df['SOĞUTMA2 ISI'].mean(),
            'Soğutma 3': self.df['SOĞUTMA3 ISI'].mean()
        }
        bars = ax1.bar(ortalama_sicakliklar.keys(), ortalama_sicakliklar.values(),
                      color=[self.colors['bilgi'], self.colors['uyari'], 
                            self.colors['normal'], self.colors['anomali'], self.colors['mor'],
                            self.colors['turkuaz'], self.colors['uyari'], self.colors['normal']],
                      edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Ortalama Sıcaklık (°C)', fontsize=11, fontweight='bold')
        ax1.set_title('Bölge Bazlı Ortalama Sıcaklıklar', fontsize=13, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}°C',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 2. Kontrol Başarı Oranları (Pie)
        ax2 = fig.add_subplot(gs[0, 2])
        
        # Örnek: Ön Isıtma kontrol başarısı
        on_isitma_fark = abs(self.df['ÖN ISITMA SET ISI'] - self.df['ÖN ISITMA ISI'])
        basarili = (on_isitma_fark <= 50).sum()
        basarisiz = (on_isitma_fark > 50).sum()
        
        ax2.pie([basarili, basarisiz], labels=['Başarılı', 'Başarısız'],
               autopct='%1.1f%%', colors=[self.colors['normal'], self.colors['anomali']],
               startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax2.set_title('Ön Isıtma Kontrol\nBaşarısı', fontsize=12, fontweight='bold')
        
        # 3. Günlük Trend (Line)
        ax3 = fig.add_subplot(gs[1, :])
        gunluk_ort = self.df.groupby(self.df['TARİH'].dt.date).agg({
            'CEH.2 ÜST1 ISI': 'mean',
            'CEH.3 ÜST1 ISI': 'mean'
        })
        ax3.plot(gunluk_ort.index, gunluk_ort['CEH.2 ÜST1 ISI'], 
                marker='o', linewidth=2.5, label='Ceh 2', color=self.colors['anomali'])
        ax3.plot(gunluk_ort.index, gunluk_ort['CEH.3 ÜST1 ISI'], 
                marker='s', linewidth=2.5, label='Ceh 3', color=self.colors['mor'])
        ax3.set_ylabel('Sıcaklık (°C)', fontsize=11, fontweight='bold')
        ax3.set_title('Ana Ceh Sıcaklık Trendi (Günlük Ortalama)', fontsize=13, fontweight='bold')
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Güç Kullanımı (Box)
        ax4 = fig.add_subplot(gs[2, 0])
        guc_cols = [col for col in self.df.columns if 'GÜÇ %' in col][:4]
        guc_data = [self.df[col] for col in guc_cols]
        bp = ax4.boxplot(guc_data, labels=[col.replace(' GÜÇ %', '').replace('CEH.', 'C') 
                                           for col in guc_cols],
                        patch_artist=True)
        for patch, color in zip(bp['boxes'], [self.colors['normal'], self.colors['anomali'], 
                                              self.colors['mor'], self.colors['bilgi']]):
            patch.set_facecolor(color)
        ax4.set_ylabel('Güç (%)', fontsize=11, fontweight='bold')
        ax4.set_title('Güç Kullanımı Dağılımı', fontsize=12, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Soğutma Etkinliği (Histogram)
        ax5 = fig.add_subplot(gs[2, 1])
        sogutma_fark = self.df['SOĞUTMA1 ISI'] - self.df['SOĞUTMA3 ISI']
        ax5.hist(sogutma_fark, bins=40, color=self.colors['turkuaz'], 
                alpha=0.7, edgecolor='black')
        ax5.axvline(sogutma_fark.mean(), color=self.colors['anomali'], 
                   linestyle='--', linewidth=2, label=f'Ort: {sogutma_fark.mean():.1f}°C')
        ax5.set_xlabel('Sıcaklık Farkı (°C)', fontsize=11, fontweight='bold')
        ax5.set_ylabel('Frekans', fontsize=11, fontweight='bold')
        ax5.set_title('Soğutma Etkinliği', fontsize=12, fontweight='bold')
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3, axis='y')
        
        # 6. Sistem Metrikleri (Text)
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.axis('off')
        
        # Metrik hesapla
        toplam_kayit = len(self.df)
        gun_sayisi = (self.df['TARİH'].max() - self.df['TARİH'].min()).days + 1
        
        metin = f"""
        📊 SİSTEM METRİKLERİ
        {'='*25}
        
        📅 Analiz Dönemi: {gun_sayisi} gün
        📝 Toplam Kayıt: {toplam_kayit:,}
        
        🌡️ Ortalama Sıcaklıklar:
        • Ceh 2: {self.df['CEH.2 ÜST1 ISI'].mean():.0f}°C
        • Ceh 3: {self.df['CEH.3 ÜST1 ISI'].mean():.0f}°C
        
        ⚡ Ortalama Güç: {self.df['ÖN ISITMA GÜÇ %'].mean():.1f}%
        
        ❄️ Soğutma Farkı: {sogutma_fark.mean():.0f}°C
        
        ✅ Veri Kalitesi: {((1 - on_isitma_fark[on_isitma_fark > 200].count()/len(self.df))*100):.1f}%
        """
        
        ax6.text(0.1, 0.5, metin, fontsize=10, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))
        
        plt.savefig(f'{self.output_dir}performans_ozet_dashboard.png', dpi=300, bbox_inches='tight')
        print(f"✅ Kaydedildi: {self.output_dir}performans_ozet_dashboard.png")
        plt.close()
    
    def tum_grafikleri_olustur(self):
        """
        Tüm grafikleri sırayla oluşturur
        """
        print("\n" + "🎨"*40)
        print("FIRIN GÖRSELLEŞTİRME SÜRECİ BAŞLIYOR")
        print("🎨"*40)
        
        self.sicaklik_zaman_serisi()
        self.set_gercek_karsilastirma()
        self.ceh_dagilim_analizi()
        self.guc_amp_analizi()
        self.sogutma_etkinligi()
        self.anomali_haritasi()
        self.heatmap_korelasyon()
        self.performans_ozet_dashboard()
        
        print("\n" + "="*70)
        print("✅ TÜM GRAFİKLER BAŞARIYLA OLUŞTURULDU!")
        print("="*70)
        print(f"\n📁 Grafikler şu klasörde: {self.output_dir}")
        print("\n📊 Oluşturulan Grafikler:")
        print("  1. sicaklik_zaman_serisi.png - Sıcaklık trendleri")
        print("  2. set_gercek_karsilastirma.png - Hedef vs gerçek sıcaklık")
        print("  3. ceh_dagilim_analizi.png - Ceh bölmeleri dağılımı")
        print("  4. guc_amp_analizi.png - Enerji tüketimi analizi")
        print("  5. sogutma_etkinligi.png - Soğutma sistemi performansı")
        print("  6. anomali_haritasi.png - Anomali dağılımı")
        print("  7. heatmap_korelasyon.png - Korelasyon matrisi")
        print("  8. performans_ozet_dashboard.png - Genel özet dashboard")


# Test için
if __name__ == "__main__":
    # Temizlenmiş veriyi yükle
    print("\n📂 Temizlenmiş fırın verisi yükleniyor...")
    df = pd.read_csv('data/processed/firin_temiz.csv')
    df['TARİH'] = pd.to_datetime(df['TARİH'])
    
    print(f"✅ Veri yüklendi: {len(df)} satır, {len(df.columns)} sütun")
    print(f"📅 Tarih aralığı: {df['TARİH'].min()} - {df['TARİH'].max()}")
    
    # Görselleştirici oluştur
    gorselestirici = FirinGorselestirici(df)
    
    # Tüm grafikleri oluştur
    gorselestirici.tum_grafikleri_olustur()
    
    print("\n✨ Görselleştirme işlemi tamamlandı!")
    print("💡 Grafikleri 'reports/figures/' klasöründe inceleyebilirsiniz.")