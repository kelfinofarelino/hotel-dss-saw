import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    # 1. Read data
    df = pd.read_csv(file_path, sep=',', encoding='utf-8-sig', on_bad_lines='skip')
    
    if len(df.columns) == 1:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
        
    # 2. AUTOMATIC COLUMN DETECTION
    col_title = 'Title'
    col_price = 'Price Starts From'
    col_rating = 'Rating'
    col_review = 'Review Count'
    col_star = 'Star Hotel/Villa/Resort'
    
    criteria_columns = [col_title, col_price, col_rating, col_review, col_star]
    
    # 3. Filter initial criteria data
    df = df.dropna(subset=criteria_columns).copy()
    
    # ==========================================
    # ADDITIONAL PREPROCESSING: DUPLICATE HANDLING
    # ==========================================
    # Remove trailing/leading spaces in hotel names to ensure accurate deduplication
    df[col_title] = df[col_title].astype(str).str.strip()
    
    # Drop duplicates based on the hotel name
    df = df.drop_duplicates(subset=[col_title], keep='first')
    
    # Take the top 300 data entries after duplicate removal
    df = df.head(300).copy()
    df['Alternative (Hotel)'] = df[col_title]
    
# 4. Process the Facilities column into numeric counts (Proxy based on string length)
    col_fac = [c for c in df.columns if 'Facilit' in c]
    if col_fac:
        # Menghitung panjang string karakter, bukan split koma
        df['Facility Count'] = df[col_fac[0]].apply(lambda x: len(str(x)) if pd.notnull(x) else 0)
    else:
        df['Facility Count'] = 1
        
    columns_to_keep = [
        'Alternative (Hotel)', 
        col_price, 
        col_rating, 
        col_star, 
        col_review,
        'Facility Count'
    ]
    
    df_raw = df[columns_to_keep].copy()
    
    # 5. FORCE RENAME COLUMNS FOR CONSISTENCY
    df_matrix = df_raw.copy()
    df_matrix.columns = [
        'Alternative (Hotel)', 
        'C1 (Price)', 
        'C2 (Rating)', 
        'C3 (Star)', 
        'C4 (Reviews)', 
        'C5 (Facilities)'
    ]
    
    # 6. NUMERIC CLEANSING
    # Extract only digits for Price
    df_matrix['C1 (Price)'] = df_matrix['C1 (Price)'].astype(str).replace(r'[^\d]', '', regex=True)
    
    # Replace commas with dots for float conversion in Rating, Star, and Reviews
    for col in ['C2 (Rating)', 'C3 (Star)', 'C4 (Reviews)']:
        df_matrix[col] = df_matrix[col].astype(str).str.replace(',', '.')
        
    # Convert all criteria columns to numeric (float)
    for col in df_matrix.columns:
        if col != 'Alternative (Hotel)':
            df_matrix[col] = pd.to_numeric(df_matrix[col], errors='coerce')
            
    df_matrix = df_matrix.dropna()
    df_matrix.set_index('Alternative (Hotel)', inplace=True)
    return df_raw, df_matrix

def calculate_normalization(df_matrix, attributes):
    df_norm = df_matrix.copy().astype(float)
    for i, col in enumerate(df_matrix.columns):
        if attributes[i] == 0:  # Cost Attribute
            min_val = df_matrix[col].min()
            df_norm[col] = min_val / df_matrix[col]
        else:  # Benefit Attribute
            max_val = df_matrix[col].max()
            df_norm[col] = df_matrix[col] / max_val
    return df_norm

def calculate_final_score(df_matrix, df_norm, weights):
    W = np.array(weights)
    scores = df_norm.values.dot(W) 
    
    df_final = df_matrix.copy()
    df_final['Final Score'] = scores
    df_final = df_final.reset_index()
    df_final = df_final.sort_values(by='Final Score', ascending=False).reset_index(drop=True)
    return df_final