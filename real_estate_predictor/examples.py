"""
Example Usage and Demo Script
Shows how to use the Real Estate Price Predictor project
"""

import sys
import os
import pandas as pd
import numpy as np

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_preprocessing import DataPreprocessor
from model import RealEstatePricePredictor, compare_models


def example_1_basic_training():
    """
    Example 1: Basic model training with sample data
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Model Training")
    print("="*70)
    
    # Generate sample data
    np.random.seed(42)
    n_samples = 300
    
    df = pd.DataFrame({
        'square_feet': np.random.randint(1500, 4000, n_samples),
        'bedrooms': np.random.randint(2, 6, n_samples),
        'bathrooms': np.random.uniform(1.5, 3.5, n_samples).round(1),
        'age': np.random.randint(0, 40, n_samples),
        'garage_spaces': np.random.randint(0, 3, n_samples),
        'lot_size': np.random.randint(3000, 15000, n_samples),
        'location_score': np.random.uniform(2, 9, n_samples).round(1),
        'neighborhood': np.random.choice(['Downtown', 'Suburbs', 'Rural'], n_samples),
        'amenities_count': np.random.randint(1, 8, n_samples),
        'market_trend': np.random.choice(['Rising', 'Stable', 'Declining'], n_samples),
    })
    
    # Generate prices
    df['price'] = (100000 + df['square_feet']*80 + df['bedrooms']*40000 + 
                   np.random.normal(0, 40000, n_samples)).astype(int)
    
    print(f"Generated {len(df)} sample properties\n")
    
    # Preprocess data
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(
        data=df,
        target_col='price',
        categorical_cols=['neighborhood', 'market_trend']
    )
    
    # Train single model
    print("\nTraining Random Forest model...")
    predictor = RealEstatePricePredictor(model_type='random_forest')
    predictor.train(X_train, y_train)
    metrics = predictor.evaluate(X_test, y_test)
    
    print("\n✓ Example 1 completed!")


def example_2_compare_models():
    """
    Example 2: Compare multiple models
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Comparing Multiple Models")
    print("="*70)
    
    # Generate sample data
    np.random.seed(123)
    n_samples = 400
    
    df = pd.DataFrame({
        'square_feet': np.random.randint(1200, 4500, n_samples),
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.uniform(1, 4, n_samples).round(1),
        'age': np.random.randint(0, 50, n_samples),
        'garage_spaces': np.random.randint(0, 4, n_samples),
        'lot_size': np.random.randint(2000, 18000, n_samples),
        'location_score': np.random.uniform(1, 10, n_samples).round(1),
        'neighborhood': np.random.choice(['Downtown', 'Suburbs', 'Rural', 'Waterfront'], n_samples),
        'amenities_count': np.random.randint(0, 10, n_samples),
        'market_trend': np.random.choice(['Rising', 'Stable', 'Declining'], n_samples),
    })
    
    # Generate prices with more variance
    df['price'] = (120000 + df['square_feet']*120 + df['bedrooms']*60000 + 
                   df['location_score']*15000 + np.random.normal(0, 60000, n_samples)).astype(int)
    
    # Preprocess
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(
        data=df,
        target_col='price',
        categorical_cols=['neighborhood', 'market_trend']
    )
    
    # Compare all models
    models_to_compare = ['linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting']
    results = compare_models(X_train, X_test, y_train, y_test, models_to_compare)
    
    # Find best model
    best_model_name = max(results.items(), key=lambda x: x[1]['metrics']['R2'])[0]
    print(f"\n🏆 Best Model: {best_model_name}")
    
    print("\n✓ Example 2 completed!")


def example_3_single_prediction():
    """
    Example 3: Make predictions on individual properties
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Single Property Predictions")
    print("="*70)
    
    # Create and train model
    np.random.seed(42)
    n_samples = 350
    
    df = pd.DataFrame({
        'square_feet': np.random.randint(1500, 4000, n_samples),
        'bedrooms': np.random.randint(2, 5, n_samples),
        'bathrooms': np.random.uniform(1.5, 3.5, n_samples).round(1),
        'age': np.random.randint(0, 40, n_samples),
        'garage_spaces': np.random.randint(0, 3, n_samples),
        'lot_size': np.random.randint(4000, 12000, n_samples),
        'location_score': np.random.uniform(4, 9, n_samples).round(1),
        'neighborhood': np.random.choice(['Downtown', 'Suburbs', 'Rural'], n_samples),
        'amenities_count': np.random.randint(2, 8, n_samples),
        'market_trend': np.random.choice(['Rising', 'Stable'], n_samples),
    })
    
    df['price'] = (100000 + df['square_feet']*100 + df['bedrooms']*50000 + 
                   np.random.normal(0, 50000, n_samples)).astype(int)
    
    # Train model
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(
        data=df,
        target_col='price',
        categorical_cols=['neighborhood', 'market_trend']
    )
    
    predictor = RealEstatePricePredictor(model_type='random_forest')
    predictor.train(X_train, y_train)
    
    # Make predictions for example properties
    print("\nExample Properties:")
    print("-" * 70)
    
    examples = [
        {
            'name': 'Luxury Downtown Home',
            'features': {
                'square_feet': 3500,
                'bedrooms': 5,
                'bathrooms': 3.5,
                'age': 5,
                'garage_spaces': 3,
                'lot_size': 10000,
                'location_score': 9.0,
                'neighborhood_encoded': 0,  # Downtown
                'amenities_count': 8,
                'market_trend_encoded': 0,  # Rising
                'price_per_sqft': 0,
                'bed_bath_ratio': 5/(3.5+1),
                'age_squared': 25,
                'total_rooms': 5+3.5,
                'luxury_score': 8.4
            }
        },
        {
            'name': 'Suburban Family Home',
            'features': {
                'square_feet': 2200,
                'bedrooms': 3,
                'bathrooms': 2.0,
                'age': 20,
                'garage_spaces': 2,
                'lot_size': 7000,
                'location_score': 6.5,
                'neighborhood_encoded': 1,  # Suburbs
                'amenities_count': 4,
                'market_trend_encoded': 1,  # Stable
                'price_per_sqft': 0,
                'bed_bath_ratio': 3/(2+1),
                'age_squared': 400,
                'total_rooms': 3+2,
                'luxury_score': 5.2
            }
        },
        {
            'name': 'Rural Budget Property',
            'features': {
                'square_feet': 1600,
                'bedrooms': 2,
                'bathrooms': 1.5,
                'age': 35,
                'garage_spaces': 1,
                'lot_size': 8500,
                'location_score': 4.0,
                'neighborhood_encoded': 2,  # Rural
                'amenities_count': 1,
                'market_trend_encoded': 2,  # Declining
                'price_per_sqft': 0,
                'bed_bath_ratio': 2/(1.5+1),
                'age_squared': 1225,
                'total_rooms': 2+1.5,
                'luxury_score': 2.5
            }
        }
    ]
    
    for example in examples:
        features_df = pd.DataFrame([example['features']])
        
        # Scale features (using fitted scaler)
        features_scaled = preprocessor.scaler.transform(features_df)
        features_scaled = pd.DataFrame(features_scaled, columns=features_df.columns)
        
        prediction = predictor.predict(features_scaled)[0]
        
        print(f"\n{example['name']}")
        print(f"  Square Feet: {example['features']['square_feet']:,}")
        print(f"  Bedrooms: {example['features']['bedrooms']}")
        print(f"  Bathrooms: {example['features']['bathrooms']}")
        print(f"  Age: {example['features']['age']} years")
        print(f"  Location Score: {example['features']['location_score']}/10")
        print(f"  Predicted Price: ${prediction:,.0f}")
    
    print("\n✓ Example 3 completed!")


def example_4_feature_analysis():
    """
    Example 4: Analyze feature importance
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Feature Importance Analysis")
    print("="*70)
    
    # Generate data
    np.random.seed(42)
    n_samples = 500
    
    df = pd.DataFrame({
        'square_feet': np.random.randint(1000, 5000, n_samples),
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.uniform(1, 4, n_samples).round(1),
        'age': np.random.randint(0, 50, n_samples),
        'garage_spaces': np.random.randint(0, 4, n_samples),
        'lot_size': np.random.randint(2000, 20000, n_samples),
        'location_score': np.random.uniform(1, 10, n_samples).round(1),
        'neighborhood': np.random.choice(['Downtown', 'Suburbs', 'Rural'], n_samples),
        'amenities_count': np.random.randint(0, 10, n_samples),
        'market_trend': np.random.choice(['Rising', 'Stable', 'Declining'], n_samples),
    })
    
    df['price'] = (100000 + df['square_feet']*100 + df['bedrooms']*50000 + 
                   np.random.normal(0, 50000, n_samples)).astype(int)
    
    # Preprocess
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(
        data=df,
        target_col='price',
        categorical_cols=['neighborhood', 'market_trend']
    )
    
    # Train Random Forest
    predictor = RealEstatePricePredictor(model_type='random_forest')
    predictor.train(X_train, y_train)
    predictor.evaluate(X_test, y_test)
    
    # Show feature importance
    if predictor.feature_importance is not None:
        importance_df = pd.DataFrame({
            'Feature': preprocessor.feature_names,
            'Importance': predictor.feature_importance
        }).sort_values('Importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print("-" * 70)
        for idx, row in importance_df.head(10).iterrows():
            print(f"{row['Feature']:<30} {row['Importance']:.4f}")
    
    print("\n✓ Example 4 completed!")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "REAL ESTATE PRICE PREDICTOR EXAMPLES" + " "*16 + "║")
    print("╚" + "="*68 + "╝")
    
    examples = [
        ("Basic Training", example_1_basic_training),
        ("Compare Models", example_2_compare_models),
        ("Single Predictions", example_3_single_prediction),
        ("Feature Analysis", example_4_feature_analysis),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED!")
    print("="*70)
    print("\nNext Steps:")
    print("1. Review the README.md for detailed documentation")
    print("2. Run train.py to train on your own data")
    print("3. Use predict.py to make predictions")
    print("4. Check notebooks/real_estate_analysis.ipynb for interactive exploration")
    print("\n")


if __name__ == "__main__":
    main()
