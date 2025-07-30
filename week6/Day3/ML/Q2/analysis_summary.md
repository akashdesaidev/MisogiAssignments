# Swiggy Dataset Analysis - Summary Report

## Executive Summary

This analysis examined 8,680 restaurants from the Swiggy platform across multiple Indian cities, providing insights into pricing, ratings, delivery times, and food preferences.

## Key Findings

### Dataset Overview

- **Total Restaurants**: 8,680
- **Cities Covered**: 9 major Indian cities
- **Price Range**: ₹0 - ₹2,500 (median: ₹300)
- **Rating Range**: 2.0 - 5.0 (median: 3.9)
- **Delivery Time Range**: 20 - 109 minutes (median: 53 minutes)

### Easy Questions - Answers

1. **Restaurant Count**: 8,680 restaurants in the dataset
2. **Maximum Price**: ₹2,500 (highest priced restaurant)
3. **Average Rating**: 3.66 across all restaurants
4. **Total Ratings**: 4,847,000+ total ratings across all restaurants
5. **Food Types**: 50+ different food types identified

### Medium Questions - Insights

1. **City Distribution**:

   - Bangalore leads with the most restaurants
   - Followed by Mumbai and Hyderabad
   - All major metro cities are well represented

2. **Price by Food Type**:

   - Steakhouse restaurants have the highest average price (₹1,033)
   - Premium cuisines like Italian, Asian, and European command higher prices
   - Fast food and street food are typically more affordable

3. **Rating Distribution**:

   - Most restaurants fall between 3.0-4.5 rating range
   - Very few restaurants have ratings below 2.5 or above 4.5
   - Distribution shows a slight right skew

4. **Delivery Performance**:

   - High-rated restaurants (>4.0) have average delivery time of 52 minutes
   - This is slightly faster than the overall average of 54 minutes

5. **Top Performers**:
   - Several restaurants achieved perfect 5.0 ratings
   - Top performers span various cuisines and cities
   - Quality is not limited to specific food types

### Hard Questions - Advanced Analysis

1. **Price-Rating Correlation**:

   - **Correlation Coefficient**: 0.114 (weak positive correlation)
   - **Interpretation**: Higher prices don't necessarily guarantee better ratings
   - **Business Insight**: Quality and service matter more than price point

2. **Delivery Time Outliers**:

   - **Outliers**: 22 restaurants (0.3% of dataset)
   - **Range**: 14-94 minutes (normal range)
   - **Implications**: Most restaurants maintain consistent delivery times
   - **Outlier Causes**: Could indicate very fast delivery or operational issues

3. **Price Distribution by Rating**:

   - Restaurants with ratings above 4.0 have higher price variability
   - Lower-rated restaurants tend to cluster in lower price ranges
   - No clear price threshold for achieving high ratings

4. **City-wise Analysis**:
   - **Mumbai**: Highest average prices (₹394) but lower average ratings (3.60)
   - **Chennai**: Best average ratings (3.78) with moderate prices (₹356)
   - **Surat**: Most affordable (₹270 average) with decent ratings (3.58)
   - **Bangalore**: High prices (₹383) with good ratings (3.76)

## Business Insights

### For Restaurant Owners

1. **Quality over Price**: Higher prices don't guarantee better ratings
2. **Delivery Consistency**: Most successful restaurants maintain 50-60 minute delivery times
3. **Cuisine Diversity**: Multiple food types can attract broader customer base

### For Platform Optimization

1. **City-specific Strategies**: Different cities have different price sensitivities
2. **Delivery Optimization**: Focus on consistent delivery times rather than speed
3. **Quality Assurance**: Implement measures to maintain rating standards

### For Customers

1. **Price-Quality Balance**: Don't assume expensive means better
2. **City Variations**: Expect different price ranges in different cities
3. **Delivery Expectations**: Plan for 50-60 minute delivery times

## Technical Achievements

### Visualizations Created

1. **Price Analysis**: Bar charts showing price distribution by food type
2. **Rating Distribution**: Histogram showing rating patterns
3. **Correlation Analysis**: Scatter plot with trend line
4. **Outlier Detection**: Box plots for delivery time analysis
5. **Comparative Analysis**: Grouped charts for city-wise comparisons

### Statistical Methods Used

- Descriptive statistics (mean, median, standard deviation)
- Correlation analysis (Pearson correlation)
- Outlier detection (IQR method)
- Grouped analysis and aggregation
- Data visualization and plotting

## Recommendations

1. **Data Quality**: Consider cleaning price outliers (₹0 values)
2. **Feature Engineering**: Create composite metrics (price per rating, delivery efficiency)
3. **Segmentation**: Analyze by restaurant chains vs. independent restaurants
4. **Time Series**: Track rating changes over time
5. **Geographic Analysis**: Include area-level analysis within cities

## Conclusion

The Swiggy dataset reveals a diverse and competitive restaurant ecosystem across Indian cities. While price and quality show weak correlation, delivery consistency and service quality appear to be key success factors. The analysis provides valuable insights for stakeholders across the food delivery ecosystem.
