import warnings
warnings.filterwarnings('ignore')

import sys
import joblib
import os
from utils.pipeline import CompletePipeline

# Register CompletePipeline in __main__ so pickle can find it
sys.modules['__main__'].CompletePipeline = CompletePipeline

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

PIPELINE_PATH = os.path.join(MODELS_DIR, 'failsafe_complete_pipeline.pkl')
MODEL_PATH = os.path.join(MODELS_DIR, 'failsafe_xgboost_model.pkl')
THRESHOLD_PATH = os.path.join(MODELS_DIR, 'failsafe_threshold.pkl')
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, 'failsafe_feature_names.pkl')

def load_model():
    """Load the complete pipeline and its components."""
    
    # Load complete pipeline
    pipeline = joblib.load(PIPELINE_PATH)
    print(f"✅ Pipeline loaded!")
    
    # Load model separately for SHAP
    model = joblib.load(MODEL_PATH)
    print(f"✅ XGBoost model loaded for SHAP")
    
    # Load threshold
    threshold = joblib.load(THRESHOLD_PATH)
    print(f"✅ Threshold loaded: {threshold}")
    
    # Load feature names
    feature_names = joblib.load(FEATURE_NAMES_PATH)
    print(f"✅ Feature names loaded: {len(feature_names)} features")
    
    return {
        'pipeline': pipeline,
        'model': model,
        'threshold': threshold,
        'feature_names': feature_names
    }

# Load once when app starts
model_bundle = load_model()
pipeline = model_bundle['pipeline']
model = model_bundle['model']
threshold = model_bundle['threshold']
feature_names = model_bundle['feature_names']