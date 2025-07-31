import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load the dataset
df = pd.read_csv('swiggy.csv')

print("=" * 60)
print("SWIGGY DATASET ANALYSIS")
print("=" * 60)

# ============================================================================
# EASY QUESTIONS
# ============================================================================

print("\n" + "=" * 20 + " EASY QUESTIONS " + "=" * 20)

# 1. Count Restaurants
restaurant_count = len(df)
print(f"1. Total number of restaurants: {restaurant_count:,}")

# 2. Find Maximum Price
max_price = df['Price'].max()
print(f"2. Highest price of a restaurant: ₹{max_price:,.0f}")

# 3. Average Ratings
avg_rating = df['Avg ratings'].mean()
print(f"3. Average rating of all restaurants: {avg_rating:.2f}")

# 4. Total Ratings
total_ratings = df['Total ratings'].sum()
print(f"4. Total ratings across all restaurants: {total_ratings:,}")

# 5. Food Type Count
# Split food types and count unique ones
all_food_types = []
for food_types in df['Food type'].dropna():
    types = [ft.strip() for ft in food_types.split(',')]
    all_food_types.extend(types)
unique_food_types = set(all_food_types)
print(f"5. Number of different food types: {len(unique_food_types)}")

# ============================================================================
# MEDIUM QUESTIONS
# ============================================================================

print("\n" + "=" * 20 + " MEDIUM QUESTIONS " + "=" * 20)

# 1. City Analysis
city_counts = df['City'].value_counts()
print("1. Top three cities by number of restaurants:")
for i, (city, count) in enumerate(city_counts.head(3).items(), 1):
    print(f"   {i}. {city}: {count:,} restaurants")

# 2. Price Comparison by Food Type
# Create a function to get the first food type for each restaurant
def get_primary_food_type(food_types):
    if pd.isna(food_types):
        return 'Unknown'
    return food_types.split(',')[0].strip()

df['Primary_food_type'] = df['Food type'].apply(get_primary_food_type)
price_by_food = df.groupby('Primary_food_type')['Price'].mean().sort_values(ascending=False)

print("\n2. Average price by food type (top 10):")
for food_type, avg_price in price_by_food.head(10).items():
    print(f"   {food_type}: ₹{avg_price:.0f}")

# 3. Visualization: Bar chart of average price by food type
plt.figure(figsize=(12, 8))
top_10_food_types = price_by_food.head(10)
plt.bar(range(len(top_10_food_types)), top_10_food_types.values, color='skyblue')
plt.xlabel('Food Type')
plt.ylabel('Average Price (₹)')
plt.title('Average Price by Food Type (Top 10)')
plt.xticks(range(len(top_10_food_types)), top_10_food_types.index, rotation=45, ha='right')
plt.tight_layout()
plt.savefig('avg_price_by_food_type.png', dpi=300, bbox_inches='tight')
plt.show()

# 4. Rating Distribution Histogram
plt.figure(figsize=(10, 6))
plt.hist(df['Avg ratings'], bins=30, alpha=0.7, color='lightgreen', edgecolor='black')
plt.xlabel('Average Rating')
plt.ylabel('Number of Restaurants')
plt.title('Distribution of Restaurant Ratings')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('rating_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. Delivery Time Analysis for high-rated restaurants
high_rated = df[df['Avg ratings'] > 4]
avg_delivery_high_rated = high_rated['Delivery time'].mean()
print(f"\n5. Average delivery time for restaurants with rating > 4: {avg_delivery_high_rated:.1f} minutes")

# 6. Top Rated Restaurants
top_restaurants = df.nlargest(5, 'Avg ratings')[['Restaurant', 'Avg ratings', 'Food type', 'City']]
print("\n6. Top 5 restaurants by average rating:")
for idx, row in top_restaurants.iterrows():
    print(f"   {row['Restaurant']} - Rating: {row['Avg ratings']:.1f}, Food: {row['Food type']}, City: {row['City']}")

# ============================================================================
# HARD QUESTIONS
# ============================================================================

print("\n" + "=" * 20 + " HARD QUESTIONS " + "=" * 20)

# 1. Correlation Analysis
correlation = df['Price'].corr(df['Avg ratings'])
print(f"1. Correlation between price and ratings: {correlation:.3f}")

# Scatter plot for correlation
plt.figure(figsize=(10, 6))
plt.scatter(df['Price'], df['Avg ratings'], alpha=0.6, color='purple')
plt.xlabel('Price (₹)')
plt.ylabel('Average Rating')
plt.title(f'Correlation between Price and Ratings (r = {correlation:.3f})')
plt.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(df['Price'], df['Avg ratings'], 1)
p = np.poly1d(z)
plt.plot(df['Price'], p(df['Price']), "r--", alpha=0.8)

plt.tight_layout()
plt.savefig('price_rating_correlation.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Delivery Time Outliers
plt.figure(figsize=(10, 6))
plt.boxplot(df['Delivery time'], vert=True)
plt.ylabel('Delivery Time (minutes)')
plt.title('Delivery Time Distribution with Outliers')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('delivery_time_outliers.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate outliers
Q1 = df['Delivery time'].quantile(0.25)
Q3 = df['Delivery time'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['Delivery time'] < lower_bound) | (df['Delivery time'] > upper_bound)]

print(f"\n2. Delivery Time Outliers Analysis:")
print(f"   Q1: {Q1:.1f} minutes")
print(f"   Q3: {Q3:.1f} minutes")
print(f"   IQR: {IQR:.1f} minutes")
print(f"   Lower bound: {lower_bound:.1f} minutes")
print(f"   Upper bound: {upper_bound:.1f} minutes")
print(f"   Number of outliers: {len(outliers)}")
print(f"   Outliers percentage: {(len(outliers)/len(df)*100):.1f}%")

# 3. Price and Ratings Box Plot
# Create rating categories
def categorize_rating(rating):
    if rating < 3:
        return 'Below 3'
    elif rating <= 4:
        return '3-4'
    else:
        return 'Above 4'

df['Rating_category'] = df['Avg ratings'].apply(categorize_rating)

plt.figure(figsize=(10, 6))
df.boxplot(column='Price', by='Rating_category', figsize=(10, 6))
plt.xlabel('Rating Category')
plt.ylabel('Price (₹)')
plt.title('Price Distribution by Rating Category')
plt.suptitle('')  # Remove default suptitle
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('price_by_rating_category.png', dpi=300, bbox_inches='tight')
plt.show()

# 4. Grouped Analysis by City
city_analysis = df.groupby('City').agg({
    'Price': 'mean',
    'Avg ratings': 'mean'
}).round(2)

print(f"\n4. Grouped Analysis by City:")
print(city_analysis)

# Grouped bar chart
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Average Price by City
city_analysis['Price'].plot(kind='bar', ax=ax1, color='lightcoral')
ax1.set_title('Average Price by City')
ax1.set_ylabel('Average Price (₹)')
ax1.tick_params(axis='x', rotation=45)

# Average Rating by City
city_analysis['Avg ratings'].plot(kind='bar', ax=ax2, color='lightblue')
ax2.set_title('Average Rating by City')
ax2.set_ylabel('Average Rating')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('city_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================================
# ADDITIONAL INSIGHTS
# ============================================================================

print("\n" + "=" * 20 + " ADDITIONAL INSIGHTS " + "=" * 20)

# Price range analysis
print(f"Price Statistics:")
print(f"   Minimum price: ₹{df['Price'].min():,.0f}")
print(f"   Maximum price: ₹{df['Price'].max():,.0f}")
print(f"   Median price: ₹{df['Price'].median():,.0f}")
print(f"   Standard deviation: ₹{df['Price'].std():,.0f}")

# Rating statistics
print(f"\nRating Statistics:")
print(f"   Minimum rating: {df['Avg ratings'].min():.1f}")
print(f"   Maximum rating: {df['Avg ratings'].max():.1f}")
print(f"   Median rating: {df['Avg ratings'].median():.1f}")
print(f"   Standard deviation: {df['Avg ratings'].std():.2f}")

# Delivery time statistics
print(f"\nDelivery Time Statistics:")
print(f"   Minimum delivery time: {df['Delivery time'].min():.0f} minutes")
print(f"   Maximum delivery time: {df['Delivery time'].max():.0f} minutes")
print(f"   Average delivery time: {df['Delivery time'].mean():.1f} minutes")
print(f"   Median delivery time: {df['Delivery time'].median():.0f} minutes")

# Most common food types
print(f"\nMost Common Food Types:")
food_type_counts = pd.Series(all_food_types).value_counts().head(10)
for food_type, count in food_type_counts.items():
    print(f"   {food_type}: {count} restaurants")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE - All visualizations saved as PNG files")
print("=" * 60)

