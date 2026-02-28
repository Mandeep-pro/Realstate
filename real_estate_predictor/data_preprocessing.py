"""
Data preprocessing module for Real Estate Price Predictor
Handles data cleaning, feature engineering, and transformation
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    """
    Handles all data preprocessing operations for real estate data
    """
    
    def __init__(self, test_size=0.2, random_state=42):
        """
        Initialize the preprocessor
        
        Parameters:
        -----------
        test_size : float
            Proportion of data to use for testing
        random_state : int
            Random state for reproducibility
        """
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        
    def load_data(self, filepath):
        """
        Load data from CSV file
        
        Parameters:
        -----------
        filepath : str
            Path to CSV file
            
        Returns:
        --------
        pd.DataFrame
            Loaded data
        """
        try:
            data = pd.read_csv(filepath)
            print(f"Data loaded successfully. Shape: {data.shape}")
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def handle_missing_values(self, data, strategy='mean'):
        """
        Handle missing values in the dataset
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
        strategy : str
            Strategy for handling missing values ('mean', 'median', 'drop')
            
        Returns:
        --------
        pd.DataFrame
            Data with missing values handled
        """
        print(f"Missing values before handling:\n{data.isnull().sum()}\n")
        
        if strategy == 'mean':
            data = data.fillna(data.mean(numeric_only=True))
        elif strategy == 'median':
            data = data.fillna(data.median(numeric_only=True))
        elif strategy == 'drop':
            data = data.dropna()
        
        print(f"Missing values after handling:\n{data.isnull().sum()}\n")
        return data
    
    def encode_categorical_features(self, data, categorical_cols):
        """
        Encode categorical features
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
        categorical_cols : list
            List of categorical column names
            
        Returns:
        --------
        pd.DataFrame
            Data with encoded categorical features
        """
        data_copy = data.copy()
        
        for col in categorical_cols:
            if col in data_copy.columns:
                le = LabelEncoder()
                data_copy[col] = le.fit_transform(data_copy[col].astype(str))
                self.label_encoders[col] = le
                print(f"Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
        
        return data_copy
    
    def create_features(self, data):
        """
        Create derived features from existing features
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
            
        Returns:
        --------
        pd.DataFrame
            Data with new features
        """
        data_copy = data.copy()
        
        # Example feature engineering (adjust based on your data)
        if 'square_feet' in data_copy.columns and 'price' in data_copy.columns:
            data_copy['price_per_sqft'] = data_copy['price'] / data_copy['square_feet']
        
        if 'bedrooms' in data_copy.columns and 'bathrooms' in data_copy.columns:
            data_copy['bed_bath_ratio'] = data_copy['bedrooms'] / (data_copy['bathrooms'] + 1)
        
        if 'age' in data_copy.columns:
            data_copy['age_squared'] = data_copy['age'] ** 2
        
        return data_copy
    
    def remove_outliers(self, data, columns=None, method='iqr', threshold=1.5):
        """
        Remove outliers from the dataset
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
        columns : list
            Columns to check for outliers
        method : str
            Method to use ('iqr' or 'zscore')
        threshold : float
            Threshold for outlier detection
            
        Returns:
        --------
        pd.DataFrame
            Data with outliers removed
        """
        data_copy = data.copy()
        
        if columns is None:
            columns = data_copy.select_dtypes(include=[np.number]).columns.tolist()
        
        initial_rows = len(data_copy)
        
        if method == 'iqr':
            for col in columns:
                Q1 = data_copy[col].quantile(0.25)
                Q3 = data_copy[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                data_copy = data_copy[(data_copy[col] >= lower_bound) & (data_copy[col] <= upper_bound)]
        
        elif method == 'zscore':
            for col in columns:
                mean = data_copy[col].mean()
                std = data_copy[col].std()
                data_copy = data_copy[np.abs((data_copy[col] - mean) / std) < threshold]
        
        removed_rows = initial_rows - len(data_copy)
        print(f"Removed {removed_rows} outliers using {method} method")
        
        return data_copy
    
    def prepare_data(self, data, target_col, categorical_cols=None, 
                     drop_cols=None, test_size=None):
        """
        Complete preprocessing pipeline
        
        Parameters:
        -----------
        data : pd.DataFrame
            Input data
        target_col : str
            Name of target column
        categorical_cols : list
            List of categorical column names
        drop_cols : list
            Columns to drop
        test_size : float
            Test size for train-test split
            
        Returns:
        --------
        tuple
            (X_train, X_test, y_train, y_test)
        """
        # Handle missing values
        data = self.handle_missing_values(data)
        
        # Drop unnecessary columns
        if drop_cols:
            data = data.drop(columns=drop_cols, errors='ignore')
        
        # Encode categorical features
        if categorical_cols:
            data = self.encode_categorical_features(data, categorical_cols)
        
        # Create new features
        data = self.create_features(data)
        
        # Remove outliers
        data = self.remove_outliers(data)
        
        # Separate features and target
        X = data.drop(columns=[target_col])
        y = data[target_col]
        
        self.feature_names = X.columns.tolist()
        
        # Train-test split
        if test_size is None:
            test_size = self.test_size
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state
        )
        
        # Scale features
        X_train = pd.DataFrame(
            self.scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )
        
        X_test = pd.DataFrame(
            self.scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )
        
        print(f"\nData preparation complete!")
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
