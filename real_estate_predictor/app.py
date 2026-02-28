"""
Flask Web Application for Real Estate Price Predictor
Displays the model and predictions in a web browser
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from data_preprocessing import DataPreprocessor
import os
import json

app = Flask(__name__)

# Load model and data globally
# Ensure paths are resolved relative to this script's directory
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'models', 'best_model_gradient_boosting.pkl')
data_path = os.path.join(base_dir, 'data', 'indian_real_estate_data.csv')

model = joblib.load(model_path)
df = pd.read_csv(data_path)
preprocessor = DataPreprocessor()

# Prepare data once
X_train, X_test, y_train, y_test = preprocessor.prepare_data(
    data=df,
    target_col='price',
    categorical_cols=['state', 'city', 'market_trend']
)

# Make predictions
y_pred = model.predict(X_test)

@app.route('/')
def index():
    """Home page with overview"""
    # Calculate metrics
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    # Market insights (neighborhood prices if available)
    neighborhood_prices = {}
    if 'neighborhood' in df.columns:
        neighborhoods = df['neighborhood'].unique().tolist()
        for neighborhood in neighborhoods:
            avg_price = df[df['neighborhood'] == neighborhood]['price'].mean()
            neighborhood_prices[neighborhood] = f"₹{avg_price:,.0f}"
    
    return render_template('index.html',
                         r2_score=f"{r2:.4f}",
                         rmse=f"₹{rmse:,.0f}",
                         mae=f"₹{mae:,.0f}",
                         accuracy=f"{(1 - mae / y_test.mean()) * 100:.1f}%",
                         test_count=len(y_test),
                         avg_price=f"₹{df['price'].mean():,.0f}",
                         min_price=f"₹{df['price'].min():,.0f}",
                         max_price=f"₹{df['price'].max():,.0f}",
                         neighborhoods=neighborhood_prices)

@app.route('/predict', methods=['POST'])
def predict():
    """Make price predictions"""
    try:
        data = request.json
        
        # Create property dataframe
        prop = {
            'square_feet': int(data['square_feet']),
            'bedrooms': int(data['bedrooms']),
            'bathrooms': float(data['bathrooms']),
            'age': int(data['age']),
            'garage_spaces': int(data['garage_spaces']),
            'lot_size': int(data['lot_size']),
            'location_score': float(data['location_score']),
            'state': data['state'],
            'city': data['city'],
            'amenities_count': int(data['amenities_count']),
            'market_trend': data['market_trend'],
        }
        
        # Process single property
        temp_df = df.iloc[:1].copy()
        for key, value in prop.items():
            temp_df[key] = value
        
        temp_df_processed = preprocessor.handle_missing_values(temp_df)
        temp_df_processed = preprocessor.encode_categorical_features(temp_df_processed, ['state', 'city', 'market_trend'])
        temp_df_processed = preprocessor.create_features(temp_df_processed)
        
        X_features = temp_df_processed[preprocessor.feature_names]
        X_scaled = preprocessor.scaler.transform(X_features)
        
        price = model.predict(X_scaled)[0]
        
        return jsonify({
            'success': True,
            'price': f"₹{price:,.0f}",
            'price_raw': float(price)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/predictions')
def predictions_page():
    """Show test predictions"""
    errors = y_test.values - y_pred
    abs_errors = np.abs(errors)
    percent_errors = (abs_errors / y_test.values * 100)
    
    predictions_list = []
    for i in range(min(20, len(y_test))):
        predictions_list.append({
            'actual': f"₹{y_test.iloc[i]:,.0f}",
            'predicted': f"₹{y_pred[i]:,.0f}",
            'error': f"₹{errors[i]:,.0f}",
            'accuracy': f"{(1 - abs_errors[i] / y_test.iloc[i]) * 100:.1f}%"
        })
    
    return render_template('predictions.html', predictions=predictions_list)

@app.route('/features')
def features_page():
    """Show feature importance"""
    if hasattr(model, 'feature_importances_'):
        feature_importance = model.feature_importances_
        feature_names = preprocessor.feature_names
        
        importance_list = []
        for i, (name, imp) in enumerate(zip(feature_names, feature_importance)):
            importance_list.append({
                'rank': i + 1,
                'feature': name,
                'importance': f"{imp:.4f}",
                'percentage': f"{imp * 100:.2f}%",
                'bar_width': int(imp * 100)
            })
        
        importance_list.sort(key=lambda x: float(x['importance']), reverse=True)
        importance_list = importance_list[:15]  # Top 15
        
        return render_template('features.html', features=importance_list)
    
    return render_template('features.html', features=[])

@app.route('/insights')
def insights_page():
    """Market insights"""
    # Neighborhood analysis
    states = df['state'].unique().tolist()
    state_data = []
    for state in states:
        subset = df[df['state'] == state]
        state_data.append({
            'name': state,
            'avg_price': f"₹{subset['price'].mean():,.0f}",
            'count': len(subset),
            'avg_sqft': f"{subset['square_feet'].mean():,.0f}"
        })
    
    # Market trend analysis
    trends = df['market_trend'].unique().tolist()
    trend_data = []
    for trend in trends:
        subset = df[df['market_trend'] == trend]
        trend_data.append({
            'name': trend,
            'avg_price': f"₹{subset['price'].mean():,.0f}",
            'count': len(subset),
            'pct_change': '+10%' if trend == 'Rising' else ('+0%' if trend == 'Stable' else '-10%')
        })
    
    return render_template('insights.html', 
                         neighborhoods=state_data,
                         trends=trend_data)

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🌐 REAL ESTATE PRICE PREDICTOR - WEB SERVER")
    print("="*80)
    print("\n✅ Starting Flask server...")
    print("📊 Open Chrome and go to: http://127.0.0.1:5000")
    print("="*80 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000)
