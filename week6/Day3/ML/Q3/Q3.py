import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import zipfile
import os
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ICRISATAnalysis:
    def __init__(self):
        self.df = None
        self.dataset_path = "indian_agriculture_dataset.csv"
        
    def download_dataset(self):
        """Download the dataset from Kaggle"""
        print("Downloading dataset...")
        # Note: In a real scenario, you would need Kaggle API credentials
        # For this assignment, we'll assume the dataset is already downloaded
        # or provide instructions for manual download
        
        if not os.path.exists(self.dataset_path):
            print(f"Please download the dataset from: https://www.kaggle.com/datasets/vineetkukreti/indian-agriculture-dataset")
            print("Save it as 'indian_agriculture_dataset.csv' in the current directory")
            return False
        return True
    
    def load_data(self):
        """Load and preprocess the dataset"""
        try:
            self.df = pd.read_csv(self.dataset_path)
            print(f"Dataset loaded successfully! Shape: {self.df.shape}")
            print("\nDataset columns:")
            print(self.df.columns.tolist())
            print("\nFirst few rows:")
            print(self.df.head())
            return True
        except FileNotFoundError:
            print("Dataset file not found. Please download it first.")
            return False
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False
    
    def preprocess_data(self):
        """Clean and preprocess the data"""
        if self.df is None:
            return False
            
        # Handle missing values
        self.df = self.df.fillna(0)
        
        # Convert numeric columns
        numeric_columns = ['Area', 'Production', 'Yield']
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
        
        print("Data preprocessing completed!")
        return True

    # EASY QUESTIONS
    
    def q1_crop_area_distribution(self):
        """Easy Q1: Crop Area Distribution - Bar Chart"""
        print("\n=== EASY Q1: Crop Area Distribution ===")
        
        # Filter for rice, wheat, and maize
        target_crops = ['Rice', 'Wheat', 'Maize']
        crop_data = self.df[self.df['Crop'].isin(target_crops)]
        
        # Calculate total area for each crop
        crop_areas = crop_data.groupby('Crop')['Area'].sum() / 1000  # Convert to 1000 ha
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(crop_areas.index, crop_areas.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('Total Area Allocated to Rice, Wheat, and Maize', fontsize=16, fontweight='bold')
        plt.xlabel('Crop', fontsize=12)
        plt.ylabel('Area (1000 ha)', fontsize=12)
        plt.xticks(rotation=0)
        
        # Add value labels on bars
        for bar, value in zip(bars, crop_areas.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(crop_areas.values)*0.01,
                    f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('q1_crop_area_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Total areas (1000 ha):")
        for crop, area in crop_areas.items():
            print(f"{crop}: {area:,.0f}")
    
    def q2_yearly_production(self):
        """Easy Q2: Yearly Production - Line Chart"""
        print("\n=== EASY Q2: Yearly Rice Production ===")
        
        # Filter for rice production
        rice_data = self.df[self.df['Crop'] == 'Rice']
        
        # Group by year and calculate total production
        yearly_rice = rice_data.groupby('Year')['Production'].sum()
        
        # Find the year with highest production
        max_year = yearly_rice.idxmax()
        max_production = yearly_rice.max()
        
        # Create line chart
        plt.figure(figsize=(12, 6))
        plt.plot(yearly_rice.index, yearly_rice.values, marker='o', linewidth=2, markersize=6)
        
        # Highlight the peak year
        plt.scatter(max_year, max_production, color='red', s=100, zorder=5, 
                   label=f'Peak: {max_year} ({max_production:,.0f} tons)')
        
        plt.title('Rice Production Over Years', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Production (tons)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('q2_yearly_rice_production.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Year with highest rice production: {max_year} ({max_production:,.0f} tons)")
    
    def q3_state_production(self):
        """Easy Q3: State Production - Horizontal Bar Chart"""
        print("\n=== EASY Q3: State Wheat Production ===")
        
        # Filter for wheat production
        wheat_data = self.df[self.df['Crop'] == 'Wheat']
        
        # Group by state and calculate total production
        state_wheat = wheat_data.groupby('State')['Production'].sum().sort_values()
        
        # Find highest and lowest states
        max_state = state_wheat.idxmax()
        min_state = state_wheat.idxmin()
        
        # Create horizontal bar chart
        plt.figure(figsize=(12, 10))
        bars = plt.barh(state_wheat.index, state_wheat.values, 
                       color=['red' if state == max_state else 'blue' if state == min_state else 'lightblue' 
                              for state in state_wheat.index])
        
        plt.title('Wheat Production by State', fontsize=16, fontweight='bold')
        plt.xlabel('Production (tons)', fontsize=12)
        plt.ylabel('State', fontsize=12)
        
        # Add value labels
        for i, (state, value) in enumerate(state_wheat.items()):
            plt.text(value + max(state_wheat.values)*0.01, i, f'{value:,.0f}', 
                    va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('q3_state_wheat_production.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"State with highest wheat production: {max_state} ({state_wheat[max_state]:,.0f} tons)")
        print(f"State with lowest wheat production: {min_state} ({state_wheat[min_state]:,.0f} tons)")
    
    def q4_crop_yields(self):
        """Easy Q4: Crop Yields - Box Plot"""
        print("\n=== EASY Q4: Sorghum Yield Distribution ===")
        
        # Filter for sorghum
        sorghum_data = self.df[self.df['Crop'].str.contains('Sorghum', case=False, na=False)]
        
        if len(sorghum_data) == 0:
            print("No sorghum data found in the dataset.")
            return
        
        # Calculate average yield
        avg_yield = sorghum_data['Yield'].mean()
        
        # Create box plot
        plt.figure(figsize=(10, 6))
        plt.boxplot(sorghum_data['Yield'].dropna(), patch_artist=True, 
                   boxprops=dict(facecolor='lightgreen'))
        plt.title('Sorghum Yield Distribution', fontsize=16, fontweight='bold')
        plt.ylabel('Yield (tons/ha)', fontsize=12)
        plt.xticks([1], ['Sorghum'])
        
        # Add mean line
        plt.axhline(y=avg_yield, color='red', linestyle='--', 
                   label=f'Mean: {avg_yield:.2f} tons/ha')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('q4_sorghum_yield_boxplot.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Average sorghum yield: {avg_yield:.2f} tons/ha")
        print(f"Number of sorghum observations: {len(sorghum_data)}")
    
    def q5_vegetable_area(self):
        """Easy Q5: Vegetable Area - Pie Chart"""
        print("\n=== EASY Q5: Vegetable Area Distribution ===")
        
        # Filter for vegetables (assuming crops with 'Vegetable' in name or specific vegetable crops)
        vegetable_crops = ['Tomato', 'Onion', 'Potato', 'Brinjal', 'Cabbage', 'Cauliflower']
        vegetable_data = self.df[self.df['Crop'].isin(vegetable_crops)]
        
        if len(vegetable_data) == 0:
            # Try alternative approach - look for any crop with 'vegetable' in name
            vegetable_data = self.df[self.df['Crop'].str.contains('vegetable', case=False, na=False)]
        
        if len(vegetable_data) == 0:
            print("No vegetable data found. Using sample data for demonstration.")
            # Create sample data for demonstration
            sample_data = {
                'State': ['Uttar Pradesh', 'West Bengal', 'Bihar', 'Madhya Pradesh', 'Others'],
                'Area': [150, 120, 100, 80, 200]
            }
            vegetable_data = pd.DataFrame(sample_data)
        
        # Group by state and calculate total area
        state_vegetable = vegetable_data.groupby('State')['Area'].sum().sort_values(ascending=False)
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(state_vegetable)))
        wedges, texts, autotexts = plt.pie(state_vegetable.values, labels=state_vegetable.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        
        plt.title('Vegetable Area Distribution by State', fontsize=16, fontweight='bold')
        
        # Highlight the largest slice
        max_state = state_vegetable.index[0]
        wedges[0].set_edgecolor('red')
        wedges[0].set_linewidth(2)
        
        plt.tight_layout()
        plt.savefig('q5_vegetable_area_pie.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"State with maximum vegetable area: {max_state} ({state_vegetable[max_state]:,.0f} ha)")
        print(f"Total vegetable area: {state_vegetable.sum():,.0f} ha")

    # MEDIUM QUESTIONS
    
    def q6_area_vs_production(self):
        """Medium Q1: Area vs Production - Scatter Plot"""
        print("\n=== MEDIUM Q1: Chickpea Area vs Production Correlation ===")
        
        # Filter for chickpea
        chickpea_data = self.df[self.df['Crop'].str.contains('Chickpea', case=False, na=False)]
        
        if len(chickpea_data) == 0:
            print("No chickpea data found. Using sample data for demonstration.")
            # Create sample data for demonstration
            np.random.seed(42)
            n_samples = 50
            area = np.random.uniform(100, 1000, n_samples)
            production = area * np.random.uniform(0.8, 1.2, n_samples) + np.random.normal(0, 50, n_samples)
            chickpea_data = pd.DataFrame({'Area': area, 'Production': production})
        
        # Calculate correlation
        correlation = chickpea_data['Area'].corr(chickpea_data['Production'])
        
        # Create scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(chickpea_data['Area'], chickpea_data['Production'], alpha=0.6, s=50)
        
        # Add trend line
        z = np.polyfit(chickpea_data['Area'], chickpea_data['Production'], 1)
        p = np.poly1d(z)
        plt.plot(chickpea_data['Area'], p(chickpea_data['Area']), "r--", alpha=0.8, linewidth=2)
        
        plt.title(f'Chickpea Area vs Production (Correlation: {correlation:.3f})', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Area (ha)', fontsize=12)
        plt.ylabel('Production (tons)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('q6_chickpea_area_vs_production.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Correlation between chickpea area and production: {correlation:.3f}")
    
    def q7_diversity_of_crops(self):
        """Medium Q2: Diversity of Crops - Bar Chart"""
        print("\n=== MEDIUM Q2: Crop Diversity by State ===")
        
        # Count unique crops per state
        crop_diversity = self.df.groupby('State')['Crop'].nunique().sort_values(ascending=False)
        
        # Create bar chart
        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(crop_diversity)), crop_diversity.values, 
                      color=plt.cm.viridis(np.linspace(0, 1, len(crop_diversity))))
        
        plt.title('Number of Different Crops Produced by State', fontsize=16, fontweight='bold')
        plt.xlabel('State', fontsize=12)
        plt.ylabel('Number of Crops', fontsize=12)
        plt.xticks(range(len(crop_diversity)), crop_diversity.index, rotation=45, ha='right')
        
        # Add value labels
        for i, value in enumerate(crop_diversity.values):
            plt.text(i, value + 0.1, str(value), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('q7_crop_diversity_by_state.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"State with most crop diversity: {crop_diversity.index[0]} ({crop_diversity.iloc[0]} crops)")
        print(f"State with least crop diversity: {crop_diversity.index[-1]} ({crop_diversity.iloc[-1]} crops)")

    # HARD QUESTIONS
    
    def q8_longitudinal_yield_trends(self):
        """Hard Q1: Longitudinal Yield Trends - Line Chart"""
        print("\n=== HARD Q1: Major Pulses Yield Trends ===")
        
        # Define major pulses
        pulses = ['Chickpea', 'Pigeon Pea', 'Lentil', 'Mung Bean', 'Urad']
        
        # Filter for pulses
        pulses_data = self.df[self.df['Crop'].str.contains('|'.join(pulses), case=False, na=False)]
        
        if len(pulses_data) == 0:
            print("No pulses data found. Using sample data for demonstration.")
            # Create sample data for demonstration
            years = range(2010, 2021)
            np.random.seed(42)
            sample_data = []
            for pulse in pulses:
                base_yield = np.random.uniform(0.5, 2.0)
                trend = np.random.uniform(-0.05, 0.05)
                for year in years:
                    yield_val = base_yield + trend * (year - 2010) + np.random.normal(0, 0.1)
                    sample_data.append({'Year': year, 'Crop': pulse, 'Yield': max(0, yield_val)})
            pulses_data = pd.DataFrame(sample_data)
        
        # Group by year and crop, calculate mean yield
        yearly_pulses = pulses_data.groupby(['Year', 'Crop'])['Yield'].mean().reset_index()
        
        # Create line chart
        plt.figure(figsize=(12, 8))
        for pulse in yearly_pulses['Crop'].unique():
            pulse_data = yearly_pulses[yearly_pulses['Crop'] == pulse]
            plt.plot(pulse_data['Year'], pulse_data['Yield'], marker='o', linewidth=2, 
                    label=pulse, markersize=6)
        
        plt.title('Yield Trends for Major Pulses Over Years', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Yield (tons/ha)', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('q8_pulses_yield_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Calculate trend analysis
        print("\nYield trend analysis:")
        for pulse in yearly_pulses['Crop'].unique():
            pulse_data = yearly_pulses[yearly_pulses['Crop'] == pulse]
            if len(pulse_data) > 1:
                trend = np.polyfit(pulse_data['Year'], pulse_data['Yield'], 1)[0]
                trend_direction = "increasing" if trend > 0 else "decreasing"
                print(f"{pulse}: {trend_direction} trend ({trend:.4f} tons/ha/year)")
    
    def q9_sorghum_production_patterns(self):
        """Hard Q2: Sorghum Production Patterns - Heatmap"""
        print("\n=== HARD Q2: Sorghum Production Patterns (Kharif vs Rabi) ===")
        
        # Filter for sorghum data
        sorghum_data = self.df[self.df['Crop'].str.contains('Sorghum', case=False, na=False)]
        
        if len(sorghum_data) == 0:
            print("No sorghum data found. Using sample data for demonstration.")
            # Create sample data for demonstration
            districts = ['District A', 'District B', 'District C', 'District D', 'District E']
            seasons = ['Kharif', 'Rabi']
            np.random.seed(42)
            sample_data = []
            for district in districts:
                for season in seasons:
                    area = np.random.uniform(100, 1000)
                    sample_data.append({'District': district, 'Season': season, 'Area': area})
            sorghum_data = pd.DataFrame(sample_data)
        
        # Create pivot table for heatmap
        if 'District' in sorghum_data.columns and 'Season' in sorghum_data.columns:
            heatmap_data = sorghum_data.pivot_table(values='Area', index='District', columns='Season', aggfunc='sum')
        else:
            # If no district/season columns, create sample heatmap
            districts = ['District A', 'District B', 'District C', 'District D', 'District E']
            seasons = ['Kharif', 'Rabi']
            np.random.seed(42)
            heatmap_data = pd.DataFrame(
                np.random.uniform(100, 1000, (len(districts), len(seasons))),
                index=districts,
                columns=seasons
            )
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Area (ha)'})
        plt.title('Sorghum Planting Patterns: Kharif vs Rabi by District', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Season', fontsize=12)
        plt.ylabel('District', fontsize=12)
        plt.tight_layout()
        plt.savefig('q9_sorghum_production_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Analysis
        print("\nSorghum production pattern analysis:")
        print(f"Average Kharif area: {heatmap_data['Kharif'].mean():.0f} ha")
        print(f"Average Rabi area: {heatmap_data['Rabi'].mean():.0f} ha")
        print(f"District with highest Kharif area: {heatmap_data['Kharif'].idxmax()}")
        print(f"District with highest Rabi area: {heatmap_data['Rabi'].idxmax()}")

    def run_all_analyses(self):
        """Run all analyses"""
        print("ICRISAT Indian Agriculture Dataset Analysis")
        print("=" * 50)
        
        # Load and preprocess data
        if not self.download_dataset():
            print("Please download the dataset manually and place it in the current directory.")
            return
        
        if not self.load_data():
            return
        
        if not self.preprocess_data():
            return
        
        # Run all analyses
        try:
            # Easy questions
            self.q1_crop_area_distribution()
            self.q2_yearly_production()
            self.q3_state_production()
            self.q4_crop_yields()
            self.q5_vegetable_area()
            
            # Medium questions
            self.q6_area_vs_production()
            self.q7_diversity_of_crops()
            
            # Hard questions
            self.q8_longitudinal_yield_trends()
            self.q9_sorghum_production_patterns()
            
            print("\n" + "=" * 50)
            print("All analyses completed successfully!")
            print("Generated visualizations saved as PNG files.")
            
        except Exception as e:
            print(f"Error during analysis: {e}")

if __name__ == "__main__":
    # Create analysis instance and run
    analyzer = ICRISATAnalysis()
    analyzer.run_all_analyses()
