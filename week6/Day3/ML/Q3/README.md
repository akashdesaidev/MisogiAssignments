# ICRISAT Indian Agriculture Dataset Analysis

This project provides a comprehensive analysis of the Indian Agriculture Dataset from ICRISAT, covering easy, medium, and hard-level questions with various visualizations.

## Dataset Information

**Dataset Link**: [Indian Agriculture Dataset on Kaggle](https://www.kaggle.com/datasets/vineetkukreti/indian-agriculture-dataset)

**Description**: This dataset contains information about agricultural production across different states in India, including crop areas, production volumes, and yields.

## Setup Instructions

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Download the Dataset**:

   - Visit the Kaggle dataset link above
   - Download the CSV file
   - Save it as `indian_agriculture_dataset.csv` in the current directory

3. **Run the Analysis**:
   ```bash
   python Q3.py
   ```

## Analysis Overview

### Easy Questions

1. **Crop Area Distribution** (Bar Chart)

   - **Analysis**: Calculate total area allocated to rice, wheat, and maize
   - **Visualization**: Bar chart showing areas in 1000 ha
   - **Output**: `q1_crop_area_distribution.png`

2. **Yearly Production** (Line Chart)

   - **Analysis**: Identify year with highest rice production
   - **Visualization**: Line chart with highlighted peak year
   - **Output**: `q2_yearly_rice_production.png`

3. **State Production** (Horizontal Bar Chart)

   - **Analysis**: Find states with highest and lowest wheat production
   - **Visualization**: Horizontal bar chart by state
   - **Output**: `q3_state_wheat_production.png`

4. **Crop Yields** (Box Plot)

   - **Analysis**: Calculate average yield for sorghum
   - **Visualization**: Box plot showing yield distribution
   - **Output**: `q4_sorghum_yield_boxplot.png`

5. **Vegetable Area** (Pie Chart)
   - **Analysis**: Calculate total vegetable area and find state with maximum area
   - **Visualization**: Pie chart showing proportion by state
   - **Output**: `q5_vegetable_area_pie.png`

### Medium Questions

1. **Area vs. Production** (Scatter Plot)

   - **Analysis**: Calculate correlation between chickpea area and production
   - **Visualization**: Scatter plot with trend line
   - **Output**: `q6_chickpea_area_vs_production.png`

2. **Diversity of Crops** (Bar Chart)
   - **Analysis**: Count number of different crops produced in each state
   - **Visualization**: Bar chart showing crop diversity by state
   - **Output**: `q7_crop_diversity_by_state.png`

### Hard Questions

1. **Longitudinal Yield Trends** (Line Chart)

   - **Analysis**: Analyze yield changes for major pulses over years
   - **Visualization**: Multi-line chart for different pulse crops
   - **Output**: `q8_pulses_yield_trends.png`

2. **Sorghum Production Patterns** (Heatmap)
   - **Analysis**: Identify planting patterns for kharif and rabi sorghum
   - **Visualization**: Heatmap showing area by district and season
   - **Output**: `q9_sorghum_production_heatmap.png`

## Features

- **Robust Data Handling**: Automatically handles missing data and data type conversions
- **Fallback Mechanisms**: Uses sample data for demonstration when actual data is not available
- **High-Quality Visualizations**: Professional-looking charts with proper styling
- **Comprehensive Analysis**: Covers all required questions with detailed insights
- **Error Handling**: Graceful error handling for missing datasets or data issues

## Output Files

The script generates the following output files:

- 9 PNG visualization files (one for each question)
- Console output with detailed analysis results

## Code Structure

- `ICRISATAnalysis` class: Main analysis class
- Individual methods for each question (q1*\*, q2*\*, etc.)
- Data preprocessing and validation
- Visualization generation with proper styling
- Statistical analysis and insights

## Notes

- If the actual dataset is not available, the script will use sample data for demonstration purposes
- All visualizations are saved as high-resolution PNG files (300 DPI)
- The script includes comprehensive error handling and informative console output
- Analysis results include both visual and numerical insights

## Requirements

- Python 3.7+
- pandas, numpy, matplotlib, seaborn, requests
- Internet connection for dataset download (if using Kaggle API)
