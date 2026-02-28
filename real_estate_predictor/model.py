
"""
Model training and evaluation module for Real Estate Price Predictor
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class RealEstatePricePredictor:
    """
    Real estate price prediction model with multiple regression algorithms
    """
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize the predictor with selected model type
        
        Parameters:
        -----------
        model_type : str
            Type of model ('linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting')
        """
        self.model_type = model_type
        self.model = None
        self.metrics = {}
        self.feature_importance = None
        self._build_model()
    
    def _build_model(self):
        """Build the selected model"""
        models = {
            'linear': LinearRegression(),
            'ridge': Ridge(alpha=1.0),
            'lasso': Lasso(alpha=1.0),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        }
        
        if self.model_type in models:
            self.model = models[self.model_type]
            print(f"Model initialized: {self.model_type}")
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X_train, y_train):
        """
        Train the model
        
        Parameters:
        -----------
        X_train : pd.DataFrame or np.ndarray
            Training features
        y_train : pd.Series or np.ndarray
            Training target values
        """
        print(f"\nTraining {self.model_type} model...")
        self.model.fit(X_train, y_train)
        print("Model training completed!")
        
        # Store feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = self.model.feature_importances_
    
    def predict(self, X):
        """
        Make predictions on new data
        
        Parameters:
        -----------
        X : pd.DataFrame or np.ndarray
            Features for prediction
            
        Returns:
        --------
        np.ndarray
            Predicted prices
        """
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Parameters:
        -----------
        X_test : pd.DataFrame or np.ndarray
            Test features
        y_test : pd.Series or np.ndarray
            Test target values
            
        Returns:
        --------
        dict
            Dictionary containing evaluation metrics
        """
        y_pred = self.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        
        self.metrics = {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'MAPE': mape
        }
        
        print("\n" + "="*50)
        print(f"Model Evaluation Metrics ({self.model_type})")
        print("="*50)
        print(f"R² Score:                 {r2:.4f}")
        print(f"Mean Absolute Error:      ${mae:,.2f}")
        print(f"Root Mean Squared Error:  ${rmse:,.2f}")
        print(f"Mean Absolute % Error:    {mape:.4f}")
        print("="*50 + "\n")
        
        return self.metrics
    
    def save_model(self, filepath):
        """
        Save the trained model to file
        
        Parameters:
        -----------
        filepath : str
            Path to save the model
        """
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model from file
        
        Parameters:
        -----------
        filepath : str
            Path to the saved model
        """
        self.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
    
    def plot_predictions(self, y_test, y_pred, figsize=(12, 5)):
        """
        Plot actual vs predicted values
        
        Parameters:
        -----------
        y_test : pd.Series or np.ndarray
            Actual test values
        y_pred : np.ndarray
            Predicted values
        figsize : tuple
            Figure size
        """
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Scatter plot
        axes[0].scatter(y_test, y_pred, alpha=0.6)
        axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[0].set_xlabel('Actual Price')
        axes[0].set_ylabel('Predicted Price')
        axes[0].set_title(f'Actual vs Predicted Prices ({self.model_type})')
        axes[0].grid(True, alpha=0.3)
        
        # Residuals plot
        residuals = y_test - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.6)
        axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Predicted Price')
        axes[1].set_ylabel('Residuals')
        axes[1].set_title('Residuals Plot')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_feature_importance(self, feature_names, figsize=(10, 6), top_n=15):
        """
        Plot feature importance (for tree-based models)
        
        Parameters:
        -----------
        feature_names : list
            Names of features
        figsize : tuple
            Figure size
        top_n : int
            Number of top features to display
        """
        if self.feature_importance is None:
            print("Feature importance not available for this model type")
            return None
        
        # Create dataframe for plotting
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False).head(top_n)
        
        fig, ax = plt.subplots(figsize=figsize)
        sns.barplot(data=importance_df, x='importance', y='feature', ax=ax)
        ax.set_title(f'Top {top_n} Feature Importance ({self.model_type})')
        ax.set_xlabel('Importance')
        
        plt.tight_layout()
        return fig
    
    def get_metrics_summary(self):
        """Get a summary of evaluation metrics"""
        return self.metrics


def compare_models(X_train, X_test, y_train, y_test, models_to_train=None):
    """
    Train and compare multiple models
    
    Parameters:
    -----------
    X_train, X_test, y_train, y_test : data
        Training and test data
    models_to_train : list
        List of model types to train
        
    Returns:
    --------
    dict
        Dictionary containing all models and their metrics
    """
    if models_to_train is None:
        models_to_train = ['linear', 'ridge', 'lasso', 'random_forest', 'gradient_boosting']
    
    results = {}
    
    for model_type in models_to_train:
        print(f"\n{'='*50}")
        print(f"Training {model_type.upper()}")
        print('='*50)
        
        predictor = RealEstatePricePredictor(model_type=model_type)
        predictor.train(X_train, y_train)
        metrics = predictor.evaluate(X_test, y_test)
        
        results[model_type] = {
            'model': predictor,
            'metrics': metrics
        }
    
    # Compare models
    print("\n" + "="*50)
    print("MODEL COMPARISON")
    print("="*50)
    
    comparison_df = pd.DataFrame({
        model_name: model_data['metrics'] 
        for model_name, model_data in results.items()
    }).T
    
    print(comparison_df.to_string())
    print("="*50 + "\n")
    
    return results
