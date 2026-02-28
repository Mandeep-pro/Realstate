# Data Documentation

## Dataset Description

This directory contains real estate pricing data used for model training and validation.

### real_estate_data.csv

#### Dataset Shape
- Rows: 500 (configurable)
- Columns: 10+ features

#### Feature Descriptions

| Feature | Type | Range/Values | Description |
|---------|------|---------|---|
| square_feet | Integer | 1,000 - 5,000 | Total livable square footage |
| bedrooms | Integer | 1 - 5 | Number of bedrooms |
| bathrooms | Float | 1.0 - 4.0 | Number of bathrooms (increments of 0.5) |
| age | Integer | 0 - 50 | Age of property in years |
| garage_spaces | Integer | 0 - 3 | Number of garage parking spaces |
| lot_size | Integer | 2,000 - 20,000 | Total lot size in sq ft |
| location_score | Float | 1.0 - 10.0 | Neighborhood quality score (1-10) |
| neighborhood | Categorical | 'Downtown', 'Suburbs', 'Rural' | Location type |
| amenities_count | Integer | 0 - 9 | Number of amenities (pool, gym, etc) |
| market_trend | Categorical | 'Rising', 'Stable', 'Declining' | Current market condition |
| price | Integer | 50,000+ | Property price in dollars (TARGET) |

#### Target Variable
- **price**: Property price in US dollars

### Data Statistics

#### Numeric Features
```
square_feet:     Mean: ~3,000 sq ft,    StdDev: ~1,100 sq ft
bedrooms:        Mean: ~3,           StdDev: ~1.4
bathrooms:       Mean: ~2.5,         StdDev: ~0.9
age:             Mean: ~25 years,    StdDev: ~14.5 years
garage_spaces:   Mean: ~1.5,         StdDev: ~1.0
lot_size:        Mean: ~11,000 sq ft, StdDev: ~5,200 sq ft
location_score:  Mean: ~5.5/10,      StdDev: ~2.8
amenities_count: Mean: ~4.5,         StdDev: ~2.9
price:           Mean: ~$600,000,    StdDev: ~$250,000
```

#### Categorical Features
```
neighborhood:    Downtown (33%), Suburbs (33%), Rural (33%)
market_trend:    Rising (33%), Stable (33%), Declining (33%)
```

### Data Quality Notes

- **Missing Values**: None in sample data
- **Outliers**: Removed using IQR method during preprocessing
- **Duplicates**: None present
- **Data Type Issues**: All features in correct format

### Data Generation

The sample data is generated using:
1. Random sampling for base features
2. Realistic price calculation using feature relationships
3. Market trend and neighborhood multipliers applied
4. Random noise added for variability

Formula for sample prices:
```
base_price = $100,000
+ (square_feet × $100)
+ (bedrooms × $50,000)
+ (bathrooms × $30,000)
+ (location_score × $20,000)
+ (amenities_count × $5,000)
+ ((100 - age) × $1,000)
+ (garage_spaces × $15,000)
+ (lot_size × $2)
+ (neighborhood_multiplier)
+ (market_trend_multiplier)
+ (random_noise)
```

### Using Your Own Data

To use your own real estate data:

1. **Format**: Create a CSV file with the same columns
2. **Place**: Put file in the `data/` directory
3. **Update**: Modify `train.py` to reference your file
4. **Validate**: Ensure data types match the descriptions

Example CSV structure:
```csv
square_feet,bedrooms,bathrooms,age,garage_spaces,lot_size,location_score,neighborhood,amenities_count,market_trend,price
2500,4,2.5,15,2,8000,8.5,Downtown,6,Rising,650000
1800,3,2.0,5,1,6000,7.0,Suburbs,5,Stable,450000
...
```

### Data Preprocessing Steps

1. **Missing Values**: Filled with mean/median
2. **Feature Engineering**: 
   - price_per_sqft = price / square_feet
   - bed_bath_ratio = bedrooms / (bathrooms + 1)
   - age_squared = age²
   - total_rooms = bedrooms + bathrooms
   - luxury_score = (location_score + amenities_count) / 20

3. **Outlier Removal**: IQR method with threshold 1.5
4. **Categorical Encoding**: Label encoding for categorical features
5. **Feature Scaling**: StandardScaler normalization (mean=0, std=1)

### Data Privacy

- Sample data is synthetic and for demonstration only
- All real data should comply with privacy regulations
- Personally identifiable information should be removed
- Sensitive financial data should be encrypted

### Data Sources

When using real data, consider sources like:
- [Zillow Research](https://www.zillow.com/)
- [Redfin Data](https://www.redfin.com/)
- [Realtor.com](https://www.realtor.com/)
- Local MLS databases
- County property records
- Real estate brokerages

---

**Last Updated**: February 2026
**Data Version**: 1.0 (Synthetic Sample)
