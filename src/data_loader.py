"""
Data loading and preprocessing utilities for COMPAS dataset.
"""

import pandas as pd
import numpy as np
from aif360.datasets import StandardDataset

def load_compas_data(file_path='data/compas.csv'):
    """
    Load and preprocess COMPAS dataset for fairness analysis.
    
    Args:
        file_path (str): Path to COMPAS CSV file
        
    Returns:
        tuple: (raw_dataframe, aif360_dataset)
    """
    try:
        # Load the dataset
        df = pd.read_csv(file_path)
        print(f"Loaded COMPAS dataset with {len(df)} rows and {len(df.columns)} columns")
        
        # Basic preprocessing
        df = preprocess_compas_data(df)
        
        # Convert to AIF360 dataset
        aif360_data = create_aif360_dataset(df)
        
        return df, aif360_data
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None, None

def preprocess_compas_data(df):
    """
    Preprocess COMPAS data for fairness analysis.
    """
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Handle missing values
    df_clean = df_clean.dropna()
    
    # Convert relevant columns to appropriate data types
    if 'is_recid' in df_clean.columns:
        df_clean['is_recid'] = df_clean['is_recid'].astype(int)
    
    print("Data preprocessing completed")
    return df_clean

def create_aif360_dataset(df):
    """
    Convert pandas DataFrame to AIF360 StandardDataset.
    """
    # Define protected attribute and labels
    protected_attribute = 'race' if 'race' in df.columns else None
    label_name = 'two_year_recid' if 'two_year_recid' in df.columns else 'is_recid'
    
    if protected_attribute and label_name in df.columns:
        dataset = StandardDataset(
            df=df,
            label_name=label_name,
            favorable_classes=[0],  # Assuming 0 is favorable (no recidivism)
            protected_attribute_names=[protected_attribute],
            privileged_classes=[['Caucasian']]  # Assuming Caucasian is privileged group
        )
        print("AIF360 dataset created successfully")
        return dataset
    else:
        print("Required columns not found in dataset")
        return None

if __name__ == "__main__":
    # Test the data loader
    df, aif_data = load_compas_data()
    if df is not None:
        print("Data columns:", df.columns.tolist())
        print("Dataset shape:", df.shape)