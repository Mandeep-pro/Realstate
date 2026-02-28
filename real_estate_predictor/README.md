# Real Estate Price Predictor 🏠

A comprehensive machine learning project to predict real estate prices based on property features, location, amenities, and market trends.

## 📋 Project Overview

This project builds regression models to predict home prices using:
- **Property Features**: Square footage, bedrooms, bathrooms, age, garage spaces
- **Location Data**: Neighborhood, location score
- **Market Data**: Market trends, amenities count
- **Derived Features**: Price per sqft, bed-bath ratio, luxury scores

## 🎯 Features

- Multiple regression algorithms (Linear, Ridge, Lasso, Random Forest, Gradient Boosting)
- Comprehensive data preprocessing and feature engineering
- Outlier detection and removal
- Model comparison and evaluation
- Feature importance analysis
- Interactive Jupyter notebook for exploration
- Command-line training script
- Prediction utilities for new properties

## 📊 Models Included

1. **Linear Regression** - Baseline model for simple relationships
2. **Ridge Regression** - Linear model with L2 regularization
3. **Lasso Regression** - Linear model with L1 regularization
4. **Random Forest** - Ensemble method for non-linear patterns
5. **Gradient Boosting** - Sequential ensemble for high accuracy

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Setup

1. **Clone/Download the project**
   ```bash
   cd real_estate_predictor
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
real_estate_predictor/
├── data/
│   ├── real_estate_data.csv          # Sample dataset
│   └── README.md                     # Data documentation
├── models/
│   └── best_model_*.pkl              # Saved trained models
├── notebooks/
│   └── real_estate_analysis.ipynb    # Interactive Jupyter notebook
├── visualizations/
│   ├── predictions_plot.png          # Actual vs Predicted
│   └── feature_importance.png        # Feature importance chart
├── data_preprocessing.py              # Data preprocessing class
├── model.py                          # Model training and evaluation
├── predict.py                        # Prediction utilities
├── train.py                          # Main training script
├── requirements.txt                  # Project dependencies
└── README.md                         # This file
```

## 🚀 Quick Start

### Option 1: Run Training Script

```bash
python train.py
```

This will:
- Generate sample real estate data
- Preprocess and engineer features
- Train all models
- Select the best performing model
- Save the model
- Generate visualizations

### Option 2: Interactive Jupyter Notebook

```bash
jupyter notebook notebooks/real_estate_analysis.ipynb
```

Run through the cells to:
- Load and explore data
- Visualize distributions
- Engineer features
- Train models
- Evaluate performance
- Make predictions

### Option 3: Use Pre-trained Model

```python
from predict import RealEstatePricePredictor

# Load trained model
predictor = RealEstatePricePredictor('models/best_model_random_forest.pkl')

# Make prediction
property_data = {
    'square_feet': 2500,
    'bedrooms': 4,
    'bathrooms': 2.5,
    'age': 15,
    'garage_spaces': 2,
    'lot_size': 8000,
    'location_score': 8.5,
    'neighborhood': 'Downtown',
    'amenities_count': 6,
    'market_trend': 'Rising'
}

price = predictor.predict_single(property_data)
print(f"Predicted Price: ${price:,.0f}")
```

## 📊 Evaluation Metrics

The project uses multiple metrics to evaluate model performance:

- **R² Score**: Coefficient of determination (higher is better, max 1.0)
- **RMSE**: Root Mean Squared Error in dollars
- **MAE**: Mean Absolute Error in dollars
- **MAPE**: Mean Absolute Percentage Error

### Expected Performance

Based on synthetic data:
- **Best Model**: Usually Random Forest or Gradient Boosting
- **R² Score**: Typically 0.90+
- **RMSE**: Varies with price range (e.g., $50,000-100,000)

## 🎓 Model Comparison

The project trains and compares 5 different regression models. You can view the performance comparison in:
- Console output during training
- `visualizations/` folder (model performance charts)
- Jupyter notebook cells

## 🔧 Configuration

### Data Preprocessing Options

Edit preprocessing parameters in `train.py`:

```python
categorical_cols = ['neighborhood', 'market_trend']  # Columns to encode
drop_cols = []                                         # Columns to drop
test_size = 0.2                                       # Train/test split ratio
```

### Model Hyperparameters

Edit model parameters in `model.py`:

```python
'random_forest': RandomForestRegressor(
    n_estimators=100,      # Number of trees
    max_depth=20,          # Maximum tree depth
    min_samples_split=5,   # Min samples to split
    random_state=42,
    n_jobs=-1
)
```

## 📈 Feature Engineering

The project creates derived features:
- **price_per_sqft**: Price divided by square footage
- **bed_bath_ratio**: Bedrooms to bathrooms ratio
- **age_squared**: Age raised to power of 2
- **total_rooms**: Sum of bedrooms and bathrooms
- **luxury_score**: Combined location and amenities score

## 🎯 Use Cases

1. **Real Estate Valuation** - Estimate property values
2. **Investment Analysis** - Identify investment opportunities
3. **Market Research** - Analyze pricing trends
4. **Automated Appraisals** - Quick property valuations
5. **Comparative Market Analysis** - CMA reports
6. **Price Prediction** - List price optimization

## 💡 Tips for Production Use

1. **Use Real Data**: Replace sample data with actual market data
2. **Update Regularly**: Retrain model monthly or quarterly
3. **Monitor Performance**: Track prediction accuracy over time
4. **Feature Updates**: Add new relevant features as they become available
5. **Data Quality**: Ensure data cleaning and validation
6. **Version Control**: Track model versions and performance
7. **A/B Testing**: Compare model versions before deployment

## 🐛 Troubleshooting

### Issue: Module not found error
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Memory error with large datasets
**Solution**: Use data sampling or increase system memory
```python
df = df.sample(n=50000, random_state=42)  # Sample 50k rows
```

### Issue: Model accuracy is low
**Solution**: 
- Collect more quality data
- Engineer better features
- Tune hyperparameters
- Try different models

## 📚 Learning Resources

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [ML Performance Metrics](https://en.wikipedia.org/wiki/Machine_learning)

## 🤝 Contributing

To improve this project:
1. Add new features or models
2. Improve data preprocessing
3. Enhance visualizations
4. Fix bugs or optimize code
5. Add documentation

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Real Estate Price Predictor - Machine Learning Project

---

**Happy Predicting! 🚀**

For questions or issues, feel free to reach out or create an issue in the repository.
