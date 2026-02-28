"""
Real Estate Price Predictor - Complete Demo
Shows the full system in action with predictions and analysis
"""

import pandas as pd
import numpy as np
import joblib
from data_preprocessing import DataPreprocessor
import os

def main():
    print("\n" + "="*80)
    print("REAL ESTATE PRICE PREDICTOR - COMPLETE WORKING DEMO")
    print("="*80)
    
    # Step 1: Load the trained model
    print("\n📦 Step 1: Loading Trained Model...")
    model_path = 'models/best_model_gradient_boosting.pkl'
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(f"✓ Model loaded: {model_path}")
    else:
        print("✗ Model not found. Please run train.py first.")
        return
    
    # Step 2: Load and review the training data
    print("\n📊 Step 2: Loading Training Data...")
    data_path = 'data/real_estate_data.csv'
    df = pd.read_csv(data_path)
    print(f"✓ Data loaded: {len(df)} properties")
    print(f"✓ Average price: ${df['price'].mean():,.0f}")
    print(f"✓ Price range: ${df['price'].min():,.0f} - ${df['price'].max():,.0f}")
    
    # Step 3: Prepare data for predictions
    print("\n🔧 Step 3: Preparing Data for Predictions...")
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(
        data=df,
        target_col='price',
        categorical_cols=['neighborhood', 'market_trend']
    )
    
    # Step 4: Make predictions on test set
    print("\n🎯 Step 4: Making Predictions on Test Set...")
    y_pred = model.predict(X_test)
    
    # Calculate errors
    errors = y_test - y_pred
    abs_errors = np.abs(errors)
    percent_errors = (abs_errors / y_test * 100)
    
    print(f"\n✓ Predictions made for {len(y_test)} test properties")
    print(f"\nPrediction Accuracy Metrics:")
    print(f"  • Mean Absolute Error: ${abs_errors.mean():,.2f}")
    print(f"  • Median Absolute Error: ${np.median(abs_errors):,.2f}")
    print(f"  • Mean Percent Error: {percent_errors.mean():.2f}%")
    print(f"  • Best Prediction Error: ${abs_errors.min():,.2f}")
    print(f"  • Worst Prediction Error: ${abs_errors.max():,.2f}")
    
    # Step 5: Show sample predictions
    print("\n📋 Step 5: Sample Predictions (First 10 Properties)...")
    print("-" * 80)
    print(f"{'Actual Price':<20} {'Predicted':<20} {'Error':<20} {'Accuracy':<15}")
    print("-" * 80)
    
    for i in range(min(10, len(y_test))):
        actual = y_test.iloc[i]
        predicted = y_pred[i]
        error = actual - predicted
        accuracy = (1 - abs(error) / actual) * 100
        
        print(f"${actual:>17,.0f} ${predicted:>17,.0f} ${error:>17,.0f} {accuracy:>13.1f}%")
    
    print("-" * 80)
    
    # Step 6: Make predictions on custom properties
    print("\n🏠 Step 6: Predicting Prices for Custom Properties...")
    print("-" * 80)
    
    custom_properties = [
        {
            'name': 'Luxury Downtown Penthouse',
            'square_feet': 3500,
            'bedrooms': 5,
            'bathrooms': 3.5,
            'age': 5,
            'garage_spaces': 3,
            'lot_size': 10000,
            'location_score': 9.5,
            'neighborhood': 'Downtown',
            'amenities_count': 9,
            'market_trend': 'Rising',
        },
        {
            'name': 'Suburban Family Home',
            'square_feet': 2200,
            'bedrooms': 3,
            'bathrooms': 2.0,
            'age': 20,
            'garage_spaces': 2,
            'lot_size': 7000,
            'location_score': 6.5,
            'neighborhood': 'Suburbs',
            'amenities_count': 4,
            'market_trend': 'Stable',
        },
        {
            'name': 'Rural Cottage',
            'square_feet': 1500,
            'bedrooms': 2,
            'bathrooms': 1.5,
            'age': 35,
            'garage_spaces': 1,
            'lot_size': 8500,
            'location_score': 4.0,
            'neighborhood': 'Rural',
            'amenities_count': 1,
            'market_trend': 'Declining',
        },
        {
            'name': 'Modern Downtown Condo',
            'square_feet': 1800,
            'bedrooms': 2,
            'bathrooms': 2.0,
            'age': 3,
            'garage_spaces': 1,
            'lot_size': 3000,
            'location_score': 8.5,
            'neighborhood': 'Downtown',
            'amenities_count': 7,
            'market_trend': 'Rising',
        },
    ]
    
    for prop in custom_properties:
        name = prop.pop('name')
        
        # Create temp dataframe for single property
        temp_df = df.iloc[:1].copy()  # Get structure
        for key, value in prop.items():
            temp_df[key] = value
        
        # Preprocess the single property
        temp_df_processed = preprocessor.handle_missing_values(temp_df)
        temp_df_processed = preprocessor.encode_categorical_features(temp_df_processed, ['neighborhood', 'market_trend'])
        temp_df_processed = preprocessor.create_features(temp_df_processed)
        
        # Select only the features used in training
        X_features = temp_df_processed[preprocessor.feature_names]
        X_scaled = preprocessor.scaler.transform(X_features)
        
        # Make prediction
        price_prediction = model.predict(X_scaled)[0]
        
        print(f"\n🏘️  {name}")
        print(f"   Bedrooms: {prop['bedrooms']} | Bathrooms: {prop['bathrooms']:.1f} | Size: {prop['square_feet']:,} sqft")
        print(f"   Age: {prop['age']} years | Location Score: {prop['location_score']}/10 | Amenities: {prop['amenities_count']}")
        print(f"   🎯 Predicted Price: ${price_prediction:,.0f}")
    
    # Step 7: Feature importance
    print("\n\n" + "="*80)
    print("📊 Step 7: Feature Importance Analysis")
    print("="*80)
    
    if hasattr(model, 'feature_importances_'):
        feature_importance = model.feature_importances_
        feature_names = preprocessor.feature_names
        
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': feature_importance
        }).sort_values('Importance', ascending=False)
        
        print("\nTop 10 Most Important Features for Price Prediction:\n")
        for idx, (_, row) in enumerate(importance_df.head(10).iterrows(), 1):
            bar = "█" * int(row['Importance'] * 100)
            print(f"{idx:2d}. {row['Feature']:<25} {bar} {row['Importance']:.4f}")
    
    # Step 8: Summary statistics
    print("\n\n" + "="*80)
    print("📈 Step 8: Model Performance Summary")
    print("="*80)
    
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\nModel: Gradient Boosting Regressor")
    print(f"  • R² Score: {r2:.4f} (explains {r2*100:.2f}% of variance)")
    print(f"  • RMSE: ${rmse:,.2f} (root mean squared error)")
    print(f"  • MAE: ${mae:,.2f} (mean absolute error)")
    print(f"  • Test Set Size: {len(y_test)} properties")
    print(f"  • Accuracy: ~{(1 - mae / y_test.mean()) * 100:.1f}% average")
    
    # Step 9: Market Insights
    print("\n" + "="*80)
    print("🔍 Step 9: Market Insights from Sample Data")
    print("="*80)
    
    print(f"\nProperty Statistics:")
    print(f"  • Average Square Footage: {df['square_feet'].mean():,.0f} sqft")
    print(f"  • Average Bedrooms: {df['bedrooms'].mean():.1f}")
    print(f"  • Average Age: {df['age'].mean():.1f} years")
    print(f"  • Average Amenities: {df['amenities_count'].mean():.1f}")
    
    print(f"\nPrice by Neighborhood:")
    for neighborhood in ['Downtown', 'Suburbs', 'Rural']:
        if neighborhood in df['neighborhood'].values:
            avg_price = df[df['neighborhood'] == neighborhood]['price'].mean()
            print(f"  • {neighborhood:<15} ${avg_price:>12,.0f}")
    
    print(f"\nPrice by Market Trend:")
    for trend in ['Rising', 'Stable', 'Declining']:
        if trend in df['market_trend'].values:
            avg_price = df[df['market_trend'] == trend]['price'].mean()
            print(f"  • {trend:<15} ${avg_price:>12,.0f}")
    
    # Final summary
    print("\n" + "="*80)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("="*80)
    print(f"\n📁 Generated Files:")
    print(f"  • Trained Model: models/best_model_gradient_boosting.pkl")
    print(f"  • Sample Data: data/real_estate_data.csv")
    print(f"  • Visualizations: visualizations/predictions_plot.png")
    print(f"  • Visualizations: visualizations/feature_importance.png")
    print(f"\n📚 Next Steps:")
    print(f"  • View visualizations in VS Code")
    print(f"  • Run examples.py for more demonstrations")
    print(f"  • Open Jupyter notebook for interactive learning")
    print(f"  • Read README.md for complete documentation")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
