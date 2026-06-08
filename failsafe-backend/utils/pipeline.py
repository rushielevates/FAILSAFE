import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

class CompletePipeline:
    def __init__(self):
        self.label_encoders = {}
        self.feature_columns = None
        self.model = None
        self.threshold = 0.55

    def fit_encoders(self, df):
        """Learn encodings from training data"""
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            le.fit(df[col])
            self.label_encoders[col] = le
        self.feature_columns = df.columns.tolist()
        return self

    def preprocess(self, df):
        """Apply preprocessing to new data"""
        df_processed = df.copy()

        for col, le in self.label_encoders.items():
            if col in df_processed.columns:
                df_processed[col] = df_processed[col].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else 0
                )
            else:
                df_processed[col] = 0

        for col in self.feature_columns:
            if col not in df_processed.columns:
                df_processed[col] = 0

        df_processed = df_processed[self.feature_columns]
        return df_processed

    def predict_proba(self, df):
        """Get prediction probabilities"""
        df_processed = self.preprocess(df)
        return self.model.predict_proba(df_processed)

    def predict(self, df):
        """Get predictions"""
        df_processed = self.preprocess(df)
        proba = self.model.predict_proba(df_processed)[:, 0]
        return (proba >= self.threshold).astype(int)