"""
Main training script for Real Estate Price Predictor
"""
"Pankaj ne change kiya ha"

import pandas as pd
import numpy as np
import os
from data_preprocessing import DataPreprocessor
from model import RealEstatePricePredictor, compare_models
import matplotlib.pyplot as plt


def generate_sample_data(n_samples=500, filepath='data/real_estate_data.csv'):
    """
    Generate sample real estate data for demonstration
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
    filepath : str
        Path to save the CSV file
    """
    print(f"Generating {n_samples} sample data points...")
    
    np.random.seed(42)
    
    data = {
        'square_feet': np.random.randint(1000, 5000, n_samples),
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.uniform(1, 4, n_samples).round(1),
        'age': np.random.randint(0, 50, n_samples),
        'garage_spaces': np.random.randint(0, 4, n_samples),
        'lot_size': np.random.randint(2000, 20000, n_samples),
        'location_score': np.random.uniform(1, 10, n_samples).round(1),  # 1-10 score
        'neighborhood': np.random.choice(['Downtown', 'Suburbs', 'Rural'], n_samples),
        'amenities_count': np.random.randint(0, 10, n_samples),
        'market_trend': np.random.choice(['Rising', 'Stable', 'Declining'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate realistic prices based on features
    base_price = 100000
    price = (
        base_price +
        (df['square_feet'] * 100) +
        (df['bedrooms'] * 50000) +
        (df['bathrooms'] * 30000) +
        (df['location_score'] * 20000) +
        (df['amenities_count'] * 5000) +
        ((100 - df['age']) * 1000) +
        (df['garage_spaces'] * 15000) +
        (df['lot_size'] * 2) +
        np.random.normal(0, 50000, n_samples)  # Add some noise
    )
    
    # Apply trend and neighborhood factors
    trend_factors = {'Rising': 1.1, 'Stable': 1.0, 'Declining': 0.9}
    neighborhood_factors = {'Downtown': 1.2, 'Suburbs': 1.0, 'Rural': 0.8}
    
    price = price * df['market_trend'].map(trend_factors)
    price = price * df['neighborhood'].map(neighborhood_factors)
    
    # Ensure positive prices
    df['price'] = np.maximum(price, 50000).astype(int)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    print(f"Sample data saved to {filepath}")
    print(f"Data shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nData statistics:\n{df.describe()}")
    
    return df


def main():
    """Main training pipeline"""
    
    print("="*60)
    print("REAL ESTATE PRICE PREDICTOR - TRAINING PIPELINE")
    print("="*60)
    
    # Step 1: Generate or load data
    data_path = 'data/indian_real_estate_data.csv'
    
    if not os.path.exists(data_path):
        print("\nStep 1: Generating sample data...")
        df = generate_sample_data(n_samples=500, filepath=data_path)
    else:
        print("\nStep 1: Loading existing data...")
        df = pd.read_csv(data_path)
        print(f"Data loaded from {data_path}")
        print(f"Data shape: {df.shape}")
    
    # Step 2: Data preprocessing
    print("\n" + "-"*60)
    print("Step 2: Data Preprocessing")
    print("-"*60)
    
    preprocessor = DataPreprocessor()
    
    # Define preprocessing parameters
    categorical_cols = ['state', 'city', 'market_trend']
    drop_cols = []  # Columns to drop if any
    target_col = 'price'
    
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(
        data=df,
        target_col=target_col,
        categorical_cols=categorical_cols,
        drop_cols=drop_cols
    )
    
    # Step 3: Train and compare models
    print("\n" + "-"*60)
    print("Step 3: Training Multiple Models")
    print("-"*60)
    
    models_to_train = ['linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting']
    results = compare_models(X_train, X_test, y_train, y_test, models_to_train)
    
    # Step 4: Select best model
    print("\n" + "-"*60)
    print("Step 4: Selecting Best Model")
    print("-"*60)
    
    best_model_name = max(results.items(), key=lambda x: x[1]['metrics']['R2'])[0]
    best_model = results[best_model_name]['model']
    
    print(f"Best Model: {best_model_name.upper()}")
    print(f"R² Score: {best_model.metrics['R2']:.4f}")
    
    # Step 5: Save best model
    print("\n" + "-"*60)
    print("Step 5: Saving Model")
    print("-"*60)
    
    model_save_path = f'models/best_model_{best_model_name}.pkl'
    os.makedirs('models', exist_ok=True)
    best_model.save_model(model_save_path)
    
    # Step 6: Generate visualizations
    print("\n" + "-"*60)
    print("Step 6: Generating Visualizations")
    print("-"*60)
    
    y_pred = best_model.predict(X_test)
    
    # Plot 1: Predictions
    fig1 = best_model.plot_predictions(y_test.values, y_pred)
    os.makedirs('visualizations', exist_ok=True)
    fig1.savefig('visualizations/predictions_plot.png', dpi=300, bbox_inches='tight')
    print("Saved: visualizations/predictions_plot.png")
    
    # Plot 2: Feature importance (if available)
    if best_model.feature_importance is not None:
        fig2 = best_model.plot_feature_importance(
            preprocessor.feature_names,
            figsize=(10, 6),
            top_n=15
        )
        fig2.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
        print("Saved: visualizations/feature_importance.png")
    
    print("\n" + "="*60)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nModel saved at: {model_save_path}")
    print(f"Visualizations saved in: visualizations/")
    print(f"Training completed with {len(X_train)} training samples and {len(X_test)} test samples")


if __name__ == "__main__":
    main()
