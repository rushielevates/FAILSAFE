import warnings
warnings.filterwarnings('ignore')
import traceback
import sys
from fastapi import APIRouter, HTTPException, UploadFile, File
import pandas as pd
import io
import shap
import numpy as np
from utils.model_loader import pipeline, model, threshold, feature_names
from utils.preprocessing import preprocess_new_data
from fastapi import Depends
from database.connection import get_db
from database.models import Prediction, StudentData
from utils.intervention import generate_intervention, generate_class_summary

router = APIRouter()

# SHAP explainer - use the XGBoost inside Stacking for explanations
# Stacking final_estimator_ is the XGBoost meta-learner
# Replace the explainer section
try:
    explainer = shap.TreeExplainer(model)  # No .final_estimator_ needed!
    print("✅ SHAP explainer initialized")
except Exception as e:
    explainer = None
    print(f"⚠️ SHAP not available: {e}")

@router.post("/predict")
async def predict(file: UploadFile = File(...), db = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        contents = await file.read()
        sample = contents[:200].decode('utf-8', errors='ignore')
        sep = ';' if ';' in sample else ','
        raw_df = pd.read_csv(io.BytesIO(contents), sep=sep)
        
        # Preprocess
        processed_df = pipeline.preprocess(raw_df)
        
        # Predict
        proba = pipeline.model.predict_proba(processed_df)
        prob_fail = proba[:, 0]
        predictions = (prob_fail >= threshold).astype(int)
        
        results = []
        for i in range(len(raw_df)):
            # SHAP explanation
            risk_factors = []
            if explainer is not None:
                try:
                    shap_values = explainer.shap_values(processed_df.iloc[[i]])
                    for fname, sval in zip(feature_names, shap_values[0]):
                        risk_factors.append({
                            "feature": fname,
                            "impact": round(float(sval), 4),
                            "direction": "protective" if sval > 0 else "risk"
                        })
                    risk_factors.sort(key=lambda x: abs(x['impact']), reverse=True)
                    risk_factors = risk_factors[:5]
                except:
                    pass
            
            pred = "AT-RISK" if predictions[i] == 1 else "SAFE"
            prob = round(float(prob_fail[i]) * 100, 1)
            
            # Save to DB
            try:
                db_prediction = Prediction(
                    student_id=str(i),
                    risk_probability=prob,
                    prediction=pred,
                    risk_factors=risk_factors,
                    uploaded_by="faculty@failsafe.com"
                )
                db.add(db_prediction)
            except:
                pass
            
            # Interventions
            interventions = generate_intervention(risk_factors, prob)
            
            results.append({
                "student_id": i,
                "risk_probability": prob,
                "prediction": pred,
                "risk_factors": risk_factors,
                "interventions": interventions
            })
        
        try:
            db.commit()
        except:
            pass
        
        total = len(raw_df)
        at_risk = sum(1 for r in results if r['prediction'] == "AT-RISK")
        class_recommendations = generate_class_summary(results)
        
        return {
            "summary": {
                "total_students": total,
                "at_risk_count": at_risk,
                "at_risk_percentage": round(at_risk/total*100, 1) if total > 0 else 0,
                "saved_to_db": True
            },
            "class_recommendations": class_recommendations,
            "students": results
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict/single")
async def predict_single(student_data: dict):
    try:
        raw_df = pd.DataFrame([student_data])
        
        print(f"\n🔍 PREDICT DEBUG:")
        print(f"   Raw columns: {len(raw_df.columns)}")
        print(f"   Raw shape: {raw_df.shape}")
        
        processed_df = preprocess_new_data(raw_df, pipeline)
        
        print(f"   Processed shape: {processed_df.shape}")
        print(f"   Expected features: {len(feature_names)}")
        
        prob_fail = pipeline.predict_proba(processed_df)[:, 0]
        prediction =  (prob_fail >= threshold).astype(int)
        
        risk_factors = []
        if explainer is not None:
            shap_values = explainer.shap_values(processed_df)
            for fname, sval in zip(feature_names, shap_values[0]):
                risk_factors.append({
                    "feature": fname,
                    "impact": round(float(sval), 4),
                    "direction": "protective" if sval > 0 else "risk"
                })
            risk_factors.sort(key=lambda x: abs(x['impact']), reverse=True)
            risk_factors = risk_factors[:5]
        interventions = generate_intervention(risk_factors, round(float(prob_fail) * 100, 1))
        return {
            "risk_probability": round(float(prob_fail) * 100, 1),
            "prediction": "AT-RISK" if prediction == 0 else "SAFE",
            "risk_factors": risk_factors,
            "interventions": interventions
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/debug/features")
async def debug_features(student_data: dict):
    """Debug endpoint - check feature counts."""
    raw_df = pd.DataFrame([student_data])
    
    print(f"\n🔍 DEBUG:")
    print(f"   Raw columns: {len(raw_df.columns)}")
    print(f"   Raw columns list: {list(raw_df.columns)}")
    
    processed_df = preprocess_new_data(
        raw_df,
        feature_names,
        preprocessing_config['binary_mappings'],
        preprocessing_config['multi_cols']
    )
    
    print(f"   Processed columns: {len(processed_df.columns)}")
    print(f"   Expected columns: {len(feature_names)}")
    
    # Find extra columns
    extra = set(processed_df.columns) - set(feature_names)
    missing = set(feature_names) - set(processed_df.columns)
    
    print(f"   Extra columns: {extra}")
    print(f"   Missing columns: {missing}")
    
    return {
        "raw_count": len(raw_df.columns),
        "processed_count": len(processed_df.columns),
        "expected_count": len(feature_names),
        "extra_columns": list(extra),
        "missing_columns": list(missing)
    }

@router.get("/debug/model-info")
async def model_info():
    """Check what the model actually expects."""
    # Get the model's internal feature count
    if hasattr(model, 'n_features_in_'):
        model_features = model.n_features_in_
    elif hasattr(model, 'final_estimator_') and hasattr(model.final_estimator_, 'n_features_in_'):
        model_features = model.final_estimator_.n_features_in_
    else:
        model_features = "Unknown"
    
    return {
        "bundle_feature_names_count": len(feature_names),
        "bundle_feature_names": feature_names,
        "model_expected_features": model_features,
        "preprocessing_config_keys": list(preprocessing_config.keys())
    }

@router.get("/history")
async def get_history(db = Depends(get_db)):
    """Get all past predictions."""
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(50).all()
    
    return {
        "total": len(predictions),
        "predictions": [
            {
                "id": p.id,
                "student_id": p.student_id,
                "risk_probability": p.risk_probability,
                "prediction": p.prediction,
                "created_at": str(p.created_at)
            }
            for p in predictions
        ]
    }