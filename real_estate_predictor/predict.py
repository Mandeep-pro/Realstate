"""
Prediction module for Real Estate Price Predictor
Use trained model to make predictions on new properties
"""

import pandas as pd
import numpy as np
import joblib
from data_preprocessing import DataPreprocessor


class RealEstatePricePredictor:
    """
    Predict real estate prices using a trained model
    """
    
    def __init__(self, model_path, preprocessor_path=None):
        """
        Initialize predictor with saved model
        
        Parameters:
        -----------
        model_path : str
            Path to the saved model file
        preprocessor_path : str
            Path to saved preprocessor (optional)
        """
        self.model = joblib.load(model_path)
        self.preprocessor = None
        if preprocessor_path:
            self.preprocessor = joblib.load(preprocessor_path)
        print(f"Model loaded from: {model_path}")
    
    def predict_single(self, property_data):
        """
        Predict price for a single property
        
        Parameters:
        -----------
        property_data : dict
            Dictionary with property features
            
        Returns:
        --------
        float
            Predicted price
        """
        # Convert to DataFrame
        df = pd.DataFrame([property_data])
        
        # Preprocess (assuming features match training data)
        prediction = self.model.predict(df)[0]
        
        return prediction
    
    def predict_batch(self, properties_df):
        """
        Predict prices for multiple properties
        
        Parameters:
        -----------
        properties_df : pd.DataFrame
            DataFrame with property features
            
        Returns:
        --------
        np.ndarray
            Array of predicted prices
        """
        predictions = self.model.predict(properties_df)
        return predictions


def demo_predictions():
    """
    Demo function showing how to make predictions
    """
    print("="*60)
    print("REAL ESTATE PRICE PREDICTION DEMO")
    print("="*60)
    
    # Example properties
    example_properties = [
        {
            'square_feet': 2500,
            'bedrooms': 4,
            'bathrooms': 2.5,
            'age': 15,
            'garage_spaces': 2,
            'lot_size': 8000,
            'location_score': 8.5,
            'neighborhood': 'Downtown',  # Will be encoded
            'amenities_count': 6,
            'market_trend': 'Rising',  # Will be encoded
            'price_per_sqft': 0,  # Placeholder for derived features
            'bed_bath_ratio': 0,  # Placeholder
            'age_squared': 0  # Placeholder
        },
        {
            'square_feet': 1800,
            'bedrooms': 3,
            'bathrooms': 2.0,
            'age': 5,
            'garage_spaces': 1,
            'lot_size': 6000,
            'location_score': 7.0,
            'neighborhood': 'Suburbs',
            'amenities_count': 5,
            'market_trend': 'Stable',
            'price_per_sqft': 0,
            'bed_bath_ratio': 0,
            'age_squared': 0
        }
    ]
    
    print("\nExample Properties for Prediction:")
    for i, prop in enumerate(example_properties, 1):
        print(f"\nProperty {i}:")
        print(f"  Square Feet: {prop['square_feet']}")
        print(f"  Bedrooms: {prop['bedrooms']}")
        print(f"  Bathrooms: {prop['bathrooms']}")
        print(f"  Age: {prop['age']} years")
        print(f"  Garage Spaces: {prop['garage_spaces']}")
        print(f"  Location Score: {prop['location_score']}/10")
        print(f"  Neighborhood: {prop['neighborhood']}")
        print(f"  Market Trend: {prop['market_trend']}")


if __name__ == "__main__":
    demo_predictions()
