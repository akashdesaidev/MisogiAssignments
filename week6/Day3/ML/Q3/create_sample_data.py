import pandas as pd
import numpy as np
import os

def create_sample_dataset():
    """Create a sample dataset that matches the ICRISAT structure"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define sample data parameters
    states = ['Uttar Pradesh', 'Maharashtra', 'Madhya Pradesh', 'Rajasthan', 'Karnataka', 
              'Gujarat', 'West Bengal', 'Bihar', 'Andhra Pradesh', 'Tamil Nadu']
    
    crops = ['Rice', 'Wheat', 'Maize', 'Sorghum', 'Chickpea', 'Pigeon Pea', 'Lentil', 
             'Mung Bean', 'Urad', 'Tomato', 'Onion', 'Potato', 'Brinjal', 'Cabbage', 'Cauliflower']
    
    years = list(range(2010, 2021))
    
    # Generate sample data
    data = []
    
    for year in years:
        for state in states:
            for crop in crops:
                # Generate realistic values based on crop type
                if crop in ['Rice', 'Wheat']:
                    area = np.random.uniform(500, 2000)
                    production = area * np.random.uniform(2.5, 4.0)
                elif crop in ['Maize', 'Sorghum']:
                    area = np.random.uniform(200, 800)
                    production = area * np.random.uniform(2.0, 3.5)
                elif crop in ['Chickpea', 'Pigeon Pea', 'Lentil']:
                    area = np.random.uniform(100, 500)
                    production = area * np.random.uniform(0.8, 1.5)
                else:  # Vegetables
                    area = np.random.uniform(50, 300)
                    production = area * np.random.uniform(15, 25)
                
                # Add some yearly variation
                year_factor = 1 + 0.1 * np.sin((year - 2010) * 0.5)
                area *= year_factor
                production *= year_factor
                
                # Calculate yield
                yield_val = production / area if area > 0 else 0
                
                data.append({
                    'State': state,
                    'Crop': crop,
                    'Year': year,
                    'Area': round(area, 2),
                    'Production': round(production, 2),
                    'Yield': round(yield_val, 3)
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv('indian_agriculture_dataset.csv', index=False)
    
    print("Sample dataset created successfully!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst few rows:")
    print(df.head())
    
    print(f"\nDataset saved as 'indian_agriculture_dataset.csv'")
    
    return df

if __name__ == "__main__":
    create_sample_dataset() 