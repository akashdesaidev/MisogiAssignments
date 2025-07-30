# Swiggy Dataset Analysis

This project performs a comprehensive analysis of the Swiggy restaurant dataset, answering easy, medium, and hard questions with detailed visualizations.

## Dataset Overview

The dataset contains information about restaurants from Swiggy, including:

- **8,680 restaurants** across multiple cities
- **Columns**: ID, Area, City, Restaurant, Price, Avg ratings, Total ratings, Food type, Address, Delivery time

## Questions Answered

### Easy Questions

1. **Count Restaurants**: Total number of restaurants in the dataset
2. **Find Maximum Price**: Highest price of a restaurant
3. **Average Ratings**: Average rating of all restaurants
4. **Total Ratings**: Total ratings across all restaurants
5. **Food Type Count**: Number of different food types

### Medium Questions

1. **City Analysis**: Top three cities by number of restaurants
2. **Price Comparison**: Average price by food type
3. **Visualization**: Bar chart of average price by food type
4. **Rating Distribution**: Histogram of restaurant ratings
5. **Delivery Time Analysis**: Average delivery time for high-rated restaurants (>4 stars)
6. **Top Rated Restaurants**: Top 5 restaurants by average rating

### Hard Questions

1. **Correlation Analysis**: Correlation between price and ratings with scatter plot
2. **Delivery Time Outliers**: Box plot analysis of delivery time outliers
3. **Price and Ratings Box Plot**: Price distribution by rating categories
4. **Grouped Analysis**: Average price and rating by city with grouped bar charts

## Visualizations Generated

The script generates the following visualization files:

1. `avg_price_by_food_type.png` - Bar chart showing average price by food type
2. `rating_distribution.png` - Histogram of restaurant ratings distribution
3. `price_rating_correlation.png` - Scatter plot with correlation line
4. `delivery_time_outliers.png` - Box plot of delivery times
5. `price_by_rating_category.png` - Box plot of prices by rating categories
6. `city_analysis.png` - Grouped bar charts for city analysis

## Installation and Usage

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Analysis

```bash
python Q2.py
```

## Key Insights

### Dataset Statistics

- **Total Restaurants**: 8,680
- **Price Range**: ₹150 - ₹1,200
- **Rating Range**: 2.9 - 4.6
- **Delivery Time Range**: 24 - 90 minutes

### Notable Findings

- **Correlation**: Weak correlation between price and ratings
- **Outliers**: Delivery time outliers indicate restaurants with very fast or slow delivery
- **City Distribution**: Bangalore has the most restaurants
- **Food Types**: North Indian and Chinese are the most common cuisines

## Files Structure

```
Q2/
├── Q2.py                 # Main analysis script
├── swiggy.csv           # Dataset file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── *.png               # Generated visualization files
```

## Technical Details

### Libraries Used

- **pandas**: Data manipulation and analysis
- **matplotlib**: Basic plotting
- **seaborn**: Enhanced visualizations
- **numpy**: Numerical computations
- **scipy**: Statistical functions

### Analysis Features

- Comprehensive statistical analysis
- Multiple visualization types (bar charts, histograms, scatter plots, box plots)
- Outlier detection using IQR method
- Correlation analysis
- Grouped analysis by multiple variables

## Output

The script provides:

1. **Console Output**: Detailed answers to all questions with statistics
2. **Visualizations**: High-quality PNG files for each analysis
3. **Additional Insights**: Extended statistics and analysis

## Notes

- All visualizations are saved as high-resolution PNG files (300 DPI)
- The analysis handles missing data appropriately
- Food types are split and analyzed individually where needed
- Rating categories are created for comparative analysis
