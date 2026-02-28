"""
Configuration File - Real Estate Price Predictor
Centralized settings for the project
"""

# ==================== DATA CONFIGURATION ====================

DATA_CONFIG = {
    'data_path': 'data/real_estate_data.csv',
    'generate_sample_data': True,
    'sample_size': 500,
    'test_size': 0.2,
    'random_state': 42,
}

# Columns configuration
COLUMN_CONFIG = {
    'target_column': 'price',
    'categorical_columns': ['neighborhood', 'market_trend'],
    'numeric_columns': [
        'square_feet', 'bedrooms', 'bathrooms', 'age',
        'garage_spaces', 'lot_size', 'location_score', 'amenities_count'
    ],
    'columns_to_drop': [],
}

# Feature engineering configuration
FEATURE_ENGINEERING = {
    'create_price_per_sqft': True,
    'create_bed_bath_ratio': True,
    'create_age_squared': True,
    'create_total_rooms': True,
    'create_luxury_score': True,
}

# ==================== PREPROCESSING CONFIGURATION ====================

PREPROCESSING_CONFIG = {
    'handle_missing_values': True,
    'missing_value_strategy': 'mean',  # 'mean', 'median', 'drop'
    'remove_outliers': True,
    'outlier_method': 'iqr',  # 'iqr' or 'zscore'
    'outlier_threshold': 1.5,
    'scale_features': True,
    'scaling_method': 'standardscaler',  # StandardScaler normalization
}

# ==================== MODEL CONFIGURATION ====================

MODELS_TO_TRAIN = [
    'linear',
    'ridge',
    'lasso',
    'random_forest',
    'gradient_boosting'
]

MODEL_HYPERPARAMETERS = {
    'linear': {},
    
    'ridge': {
        'alpha': 1.0,
    },
    
    'lasso': {
        'alpha': 1.0,
    },
    
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 20,
        'min_samples_split': 5,
        'random_state': 42,
        'n_jobs': -1,
    },
    
    'gradient_boosting': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 5,
        'random_state': 42,
    },
}

# ==================== EVALUATION CONFIGURATION ====================

EVALUATION_CONFIG = {
    'metrics': ['r2', 'rmse', 'mae', 'mape'],
    'display_results': True,
    'save_results': True,
}

# Performance targets
PERFORMANCE_TARGETS = {
    'r2_score': 0.85,  # At least 85% variance explained
    'rmse_max': 80000,  # Max $80K error
    'mae_max': 60000,  # Max $60K average error
}

# ==================== VISUALIZATION CONFIGURATION ====================

VISUALIZATION_CONFIG = {
    'save_plots': True,
    'output_directory': 'visualizations',
    'plot_dpi': 300,
    'figure_style': 'seaborn',
}

PLOT_CONFIG = {
    'predictions_plot': {
        'figsize': (12, 5),
        'show': True,
        'save': True,
        'filename': 'predictions_plot.png',
    },
    'feature_importance': {
        'figsize': (10, 6),
        'top_n': 15,
        'show': True,
        'save': True,
        'filename': 'feature_importance.png',
    },
    'model_comparison': {
        'figsize': (14, 10),
        'show': True,
        'save': True,
        'filename': 'model_comparison.png',
    },
}

# ==================== OUTPUT CONFIGURATION ====================

OUTPUT_CONFIG = {
    'models_directory': 'models',
    'save_best_model': True,
    'save_scaler': False,
    'save_preprocessor': False,
    'create_timestamp': True,
}

# ==================== LOGGING CONFIGURATION ====================

LOGGING_CONFIG = {
    'enable_logging': True,
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'log_file': 'logs/training.log',
}

# ==================== PREDICTION CONFIGURATION ====================

PREDICTION_CONFIG = {
    'batch_size': 1000,
    'round_predictions': True,
    'round_decimals': 0,  # Round to nearest dollar
    'min_price': 50000,
    'max_price': 5000000,
}

# ==================== PRICE GENERATION CONFIGURATION ====================
# Used for synthetic data generation

PRICE_GENERATION = {
    'base_price': 100000,
    'square_feet_multiplier': 100,
    'bedroom_multiplier': 50000,
    'bathroom_multiplier': 30000,
    'location_multiplier': 20000,
    'amenities_multiplier': 5000,
    'age_multiplier': 1000,
    'garage_multiplier': 15000,
    'lot_size_multiplier': 2,
    'market_noise': 50000,  # Gaussian noise std dev
}

# Market and neighborhood factors
MARKET_FACTORS = {
    'trend': {
        'Rising': 1.1,
        'Stable': 1.0,
        'Declining': 0.9,
    },
    'neighborhood': {
        'Downtown': 1.2,
        'Suburbs': 1.0,
        'Rural': 0.8,
        'Waterfront': 1.5,
    },
}

# ==================== HELPER FUNCTIONS ====================

def get_model_type(model_name):
    """Get full model type string"""
    models = {
        'linear': 'Linear Regression',
        'ridge': 'Ridge Regression',
        'lasso': 'Lasso Regression',
        'random_forest': 'Random Forest',
        'gradient_boosting': 'Gradient Boosting',
    }
    return models.get(model_name, model_name)


def get_model_hyperparameters(model_type):
    """Get hyperparameters for a specific model"""
    return MODEL_HYPERPARAMETERS.get(model_type, {})


def validate_config():
    """Validate configuration settings"""
    issues = []
    
    if DATA_CONFIG['test_size'] <= 0 or DATA_CONFIG['test_size'] >= 1:
        issues.append("test_size must be between 0 and 1")
    
    if DATA_CONFIG['sample_size'] < 50:
        issues.append("sample_size should be at least 50")
    
    if PREPROCESSING_CONFIG['outlier_threshold'] <= 0:
        issues.append("outlier_threshold must be positive")
    
    return issues


def print_config():
    """Print current configuration"""
    print("\n" + "="*60)
    print("CONFIGURATION SETTINGS")
    print("="*60)
    
    print("\nDATA:")
    for key, value in DATA_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nPREPROCESSING:")
    for key, value in PREPROCESSING_CONFIG.items():
        print(f"  {key}: {value}")
    
    print("\nMODELS TO TRAIN:")
    for model in MODELS_TO_TRAIN:
        print(f"  - {get_model_type(model)}")
    
    print("\nPERFORMANCE TARGETS:")
    for key, value in PERFORMANCE_TARGETS.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60 + "\n")


# ==================== USAGE EXAMPLES ====================

if __name__ == "__main__":
    # Validate configuration
    issues = validate_config()
    if issues:
        print("Configuration Issues Found:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
    else:
        print("✓ Configuration is valid")
    
    # Print current configuration
    print_config()
    
    # Example: Accessing specific settings
    print(f"Target column: {COLUMN_CONFIG['target_column']}")
    print(f"Models to train: {MODELS_TO_TRAIN}")
    print(f"Random Forest params: {get_model_hyperparameters('random_forest')}")
