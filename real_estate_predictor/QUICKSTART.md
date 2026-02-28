# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Training Script
```bash
python train.py
```
This generates sample data, trains all models, and saves the best one.

### Step 3: View Results
Check the `visualizations/` folder for:
- `predictions_plot.png` - Actual vs Predicted prices
- `feature_importance.png` - Most important features

### Step 4: Make Predictions
Use the trained model to predict prices for new properties

---

## 📖 Learning Path

### Beginner
1. **Run examples.py** - See all features in action
   ```bash
   python examples.py
   ```

2. **Open Jupyter notebook** - Interactive learning
   ```bash
   jupyter notebook notebooks/real_estate_analysis.ipynb
   ```

### Intermediate
1. **Understand preprocessing** - Check `data_preprocessing.py`
2. **Explore model training** - Check `model.py`
3. **Modify parameters** - Experiment with different settings in `train.py`

### Advanced
1. **Use your own data** - Replace sample data with real market data
2. **Add new features** - Extend feature engineering in `data_preprocessing.py`
3. **Tune hyperparameters** - Optimize model performance in `model.py`
4. **Deploy model** - Save and load models for production use

---

## 🎯 Common Tasks

### Load and Explore Data
```python
import pandas as pd
from data_preprocessing import DataPreprocessor

df = pd.read_csv('data/real_estate_data.csv')
print(df.head())
print(df.describe())
```

### Train a Specific Model
```python
from model import RealEstatePricePredictor
from data_preprocessing import DataPreprocessor

# Prepare data
preprocessor = DataPreprocessor()
X_train, X_test, y_train, y_test = preprocessor.prepare_data(
    data=df,
    target_col='price',
    categorical_cols=['neighborhood', 'market_trend']
)

# Train model
predictor = RealEstatePricePredictor(model_type='gradient_boosting')
predictor.train(X_train, y_train)
predictor.evaluate(X_test, y_test)
```

### Make Predictions
```python
new_property = {
    'square_feet': 2500,
    'bedrooms': 4,
    'bathrooms': 2.5,
    'age': 10,
    'garage_spaces': 2,
    'lot_size': 8000,
    'location_score': 8.0,
    'neighborhood_encoded': 0,
    'amenities_count': 6,
    'market_trend_encoded': 0,
    # ... derived features ...
}

df_new = pd.DataFrame([new_property])
df_new_scaled = preprocessor.scaler.transform(df_new)
prediction = predictor.predict(df_new_scaled)
print(f"Predicted Price: ${prediction[0]:,.0f}")
```

### Compare Models
```python
from model import compare_models

results = compare_models(X_train, X_test, y_train, y_test)
# Results show R², RMSE, MAE, MAPE for each model
```

### Save and Load Model
```python
# Save
predictor.save_model('models/my_model.pkl')

# Load
new_predictor = RealEstatePricePredictor(model_type='random_forest')
new_predictor.load_model('models/my_model.pkl')
```

---

## 🔧 Configuration Tips

### Adjust Train/Test Split
In `train.py`:
```python
preprocessor = DataPreprocessor(test_size=0.15)  # 15% for testing
```

### Use Different Model
In `train.py`:
```python
predictor = RealEstatePricePredictor(model_type='gradient_boosting')
```

### Change Categorical Columns
In `train.py`:
```python
categorical_cols = ['neighborhood', 'market_trend', 'property_type']
```

### Adjust Outlier Removal
In `data_preprocessing.py`:
```python
data = self.remove_outliers(data, method='iqr', threshold=2.0)
```

---

## 📊 Performance Expectations

### With Synthetic Data
- **R² Score**: 0.90-0.95
- **RMSE**: $40,000-60,000
- **MAE**: $30,000-50,000

### With Real Market Data
- **R² Score**: 0.70-0.85 (varies by market)
- **RMSE**: 10-15% of average price
- **MAE**: 8-12% of average price

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Model accuracy is low | Add more features, collect quality data, tune hyperparameters |
| Memory error | Sample data, increase RAM, use batch processing |
| Features don't match | Ensure derived features are calculated for new data |
| Model won't load | Check file path and ensure joblib is installed |

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `train.py` | Main training pipeline |
| `data_preprocessing.py` | Data cleaning and feature engineering |
| `model.py` | Model training and evaluation |
| `predict.py` | Making predictions |
| `examples.py` | Usage examples |
| `notebooks/real_estate_analysis.ipynb` | Interactive Jupyter notebook |

---

## 🎓 Next Steps

1. ✅ Run examples to understand the workflow
2. ✅ Explore the Jupyter notebook for interactive learning
3. ✅ Prepare your own real estate data
4. ✅ Train models on your local market
5. ✅ Deploy the model for predictions
6. ✅ Monitor and update regularly

---

**Happy Learning! 🏠📈**
