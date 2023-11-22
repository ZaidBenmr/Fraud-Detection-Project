import os
import pandas as pd
import numpy as np
import tqdm.notebook as tqdm
import joblib
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
import scipy.stats as stats
from scipy.fft import fft


def preprocessing_renamecolumns_castint (df) :
    
    df['LIB_ANO_ELEC'] = df['LIB_ANO_ELEC'].replace('INTROUVABLE', 'COMPTEUR INTROUVABLE')
    df['LIB_ANO_ELEC'] = df['LIB_ANO_ELEC'].replace('COMPTEUR MANIPUL�', 'COMPTEUR MANIPULE')
    df['LIB_ANO_ELEC'] = df['LIB_ANO_ELEC'].replace("COMPTEUR A L INTERIEUR", "COMPTEUR A L'INTERIEUR")
    df['LIB_ANO_ELEC'] = df['LIB_ANO_ELEC'].replace("COFFRET BLOQU�", "COFFRET BLOQUE")


    df["DELIVERY_POINT_ID_INT"]   = df["DELIVERY_POINT_ID"].astype('int64')
    #df['CONSUMPTION_PERIOD']  = pd.to_datetime(df['CONSUMPTION_PERIOD'], format='%Y-%m-%d')
    return df


def preprocessing_reformatdate(df) : 
    
    df["day"] = df['CONSUMPTION_PERIOD'].dt.day
    
    #Sum of N_days and consumption in same month
    df = df.groupby([df['CONSUMPTION_PERIOD'].dt.year, df['CONSUMPTION_PERIOD'].dt.month, 'NUM_CTA_ABT_BT'])\
            .agg({'BILLED_VOLUME_ELEC': 'sum', 'NOMBRE_JOUR_ELEC': 'sum',
                  'DELIVERY_POINT_ID': 'last', 'CONSUMER_BILLING_ID' : 'last',
                  'SUBSCRIPTION_STATUS_LBL': 'last', 'DELIVERY_POINT_ADDRESS': 'last',
                  'CONSUMER_TYPE':'last', 'TYP_RES': 'last', 'BILLING_CATEGORY_ELEC': 'last', 'METER_MPID_NUMBER_ELEC': 'last',
                  'METER_INSTALLATION_DATE_ELEC':'last', 'METER_BRAND_LABEL_ELEC':'last', 'METER_MODEL_LABEL_ELEC':'last',
                  'METER_POWER_ELEC': 'last', 'METER_EXISTENCE_ELEC': 'last', 'CONSUMPTION_QUALIFICATION_ELEC': 'last',
                  'METER_READING_ROUTE' : 'last', 'COMMERCIAL_AGENCY' :'last', 'LIB_ANOMALIE_ELEC': 'last', 'LIB_ANO_ELEC': 'last',
                 'DELIVERY_POINT_ID_INT' : 'last', 'day': 'last'})
    
    #Rename the indexes & reset them
    df.index.names = ['year', 'month', 'NUM_CTA_ABT_BT']
    df = df.reset_index()
    
    #Create date column from year and month ( days not important)
    df['date'] = pd.to_datetime({'year': df['year'], 'month': df['month'], 'day': df['day']})
    df = df.drop(["year","month","day"], axis=1)

    df['moyenne_consomation'] = df['BILLED_VOLUME_ELEC'] / df['NOMBRE_JOUR_ELEC']
    if (np.isnan(df['moyenne_consomation'].iloc[0]) ) : 
        df.loc[0, 'moyenne_consomation'] = df['moyenne_consomation'].mean()

    df['moyenne_consomation'] = df['moyenne_consomation'].interpolate(method="pchip")
    
    return df
    
    
def preprocessing_oneechelle (df) : 
    
    index_df = pd.DataFrame(index=pd.MultiIndex.from_product([df['NUM_CTA_ABT_BT'].unique(), \
                                                             pd.date_range(start='2017-01-01', end='2022-12-01', freq='MS').strftime('%Y-%m') \
                                                             .difference(pd.date_range(start='2020-01-01', end='2020-12-01', freq='MS').strftime('%Y-%m'))], \
                                                                 names=['NUM_CTA_ABT_BT', 'date']))
    # Convert date column in original dataframe to only month and year format
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    
    # merge the grouped_df with the index_df
    merged_df = pd.merge(index_df, df, how='left', on=['NUM_CTA_ABT_BT', 'date']).copy()
    
    # Missing values for Consumption data
    merged_df.loc[merged_df["moyenne_consomation"] == np.inf, "moyenne_consomation"] = np.nan

    if (np.isnan(merged_df['moyenne_consomation'].iloc[0]) ) : 
        merged_df.loc[merged_df.index[0], 'moyenne_consomation'] = merged_df['moyenne_consomation'].mean()
        
    merged_df['moyenne_consomation'] = merged_df['moyenne_consomation'].interpolate(method="pchip")
    
    # Missing values for Categorical data
    cols_to_fillna = merged_df.columns.drop(['NUM_CTA_ABT_BT', 'date', 'LIB_ANO_ELEC', 'moyenne_consomation'])
    merged_df[cols_to_fillna] = merged_df[cols_to_fillna].fillna(merged_df[cols_to_fillna].mode().iloc[0])
    
    return merged_df


possible_cat_features = ['SBSTATUS_CS', 'SBSTATUS_RS', 'SBSTATUS_SE', 'MTR_BR_REPRISE',
                         'MTR_MD_ACTARIS M2XS4', 'MTR_MD_REPRISE APT BT',
                         'CSO_QF_FORF ABO ABSENT/CPT INNA', 'CSO_QF_INDEX RELEVE INTERMED',
                         'CSO_QF_INDEX RELEVE NORMALE', 'CSO_QF_INDX DEPART RECTIF ERREUR',
                         'LIBANO_COMPTEUR INTROUVABLE', 'LIBANO_COMPTEUR MANIPULE',
                         'LIBANO_PT NUMERIQUE ILLISIBLE', 'LIBANOMALIE_COMPTEUR INACCESSIBLE',
                         'LIBANOMALIE_COMPTEUR NON LU', 'LIBANOMALIE_CONSOMMATION FORTE',
                         'LIBANOMALIE_CONSOMMATION NULLE', 'LIBANOMALIE_NON SIGNIFICATIF',
                         'LIBANOMALIE_RELEVE NORMAL']

def one_hot_encoding(df) : 
    
    df.drop(["TYP_RES","METER_MPID_NUMBER_ELEC"], axis=1, inplace= True)
    
    # One hot the existing columns
    cols_to_encode = {
        "SUBSCRIPTION_STATUS_LBL": "SBSTATUS",
        "CONSUMER_TYPE": "CSTYPE",
        "BILLING_CATEGORY_ELEC": "BCE",
        "METER_BRAND_LABEL_ELEC": "MTR_BR",
        "METER_MODEL_LABEL_ELEC": "MTR_MD",
        "METER_EXISTENCE_ELEC": "MTR_EX",
        "CONSUMPTION_QUALIFICATION_ELEC": "CSO_QF",
        "LIB_ANO_ELEC": "LIBANO",
        "LIB_ANOMALIE_ELEC": "LIBANOMALIE"
    }

    for col, prefix in cols_to_encode.items():
        df = pd.get_dummies(df, prefix=prefix, columns=[col])
    
    #Adding the other columns
    list3 = [x for x in possible_cat_features if x not in df.columns[13:].tolist()]
    for col in list3 :
        df[col] = 0
        
    # Date encoding
    df['METER_INSTALLATION_DATE_ELEC'] = pd.to_datetime(df['METER_INSTALLATION_DATE_ELEC'], format='%Y-%m-%d')
    df['METER_INSTALLATION_DATE_ELEC'] = df['METER_INSTALLATION_DATE_ELEC'].apply(lambda x: x.timestamp())
        
    return df

TIME_DOMAIN_FEATURES = ['MIN', 'MAX', 'MEAN', 'STD', 'P2P', 'SKEW','MAD', 'ETROPY', 'KURTOSIS', 'MAX_f', 'SUM_f', 
                        'MEAN_f', 'VAR_f','SKEW_f', 'KURTOSIS_f', 'N_releve_null']

def time_domain_features(X): 
    
    ## TIME DOMAIN ##
    values = X.values
    N_releve_null = (X == 0.0).sum()
    
    Min = np.min(X)
    Max = np.max(X)
    Mean = np.mean(X)
    Std = np.std(X)
    P2p = np.ptp(X)
    Skew = stats.skew(X)
    mad = np.median(np.abs(X - np.median(X)))
    value_counts = X.value_counts(normalize=True)
    entropy = stats.entropy(value_counts)
    Kurtosis = stats.kurtosis(X)
    
    # Frequency domain features
    ft = fft(values)
    S = np.abs(ft)
    Max_f = np.max(S)
    Sum_f = np.sum(S)
    Mean_f = np.mean(S)
    Var_f = np.var(S)
    
    sampling_rate = 1  # set the sampling rate to 1 Hz
    frequencies_hz = np.fft.fftfreq(X.size, 1/sampling_rate)
    
    Peak_f = frequencies_hz[np.argmax(S)]
    Skew_f = stats.skew(X)
    Kurtosis_f = stats.kurtosis(X)
    
    df_features = [Min,Max,Mean,Std,P2p,Skew,mad,entropy,Kurtosis,Max_f,Sum_f,Mean_f,Var_f,Skew_f,Kurtosis_f,N_releve_null]
    
    return df_features

def feature_extractor(df):
    vector = []
    # Feature of categorical values
    for i in possible_cat_features : 
        vector.append(df[i].sum())
        
    # Feature of non-categorical values
    for j in ['DELIVERY_POINT_ID_INT', 'METER_INSTALLATION_DATE_ELEC', 'METER_POWER_ELEC', 
              'METER_READING_ROUTE', 'COMMERCIAL_AGENCY'] :
        column_values = df[j].unique()
        if len(column_values) == 1:
            vector.append(df[j].iloc[0])
        else : 
            print("Error at index " + df["NUM_CTA_ABT_BT"].unique())
            
    # Time-domain features
    vector = vector + time_domain_features(df["moyenne_consomation"])
            
    #return vector
    return np.array(vector).reshape(1, 40)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(BASE_DIR, 'model') # we are now in src/model

# Importing Min-Max Scaler
path_scaler = path = os.path.join(MODELS, "scaler_v2.joblib")
scaler = joblib.load(path_scaler)

# Importing Random Forest Model
path_rf = path = os.path.join(MODELS, "model_rf_v2.joblib")
rf = joblib.load(path_rf)


pipeline = Pipeline(steps=[
    ('Rename columns / Cast to int', FunctionTransformer(preprocessing_renamecolumns_castint)),
    ('Reformating dates', FunctionTransformer(preprocessing_reformatdate)),
    ('One Echelle', FunctionTransformer(preprocessing_oneechelle)),
    ('One hot encoding', FunctionTransformer(one_hot_encoding)),
    ('Feature extractor', FunctionTransformer(feature_extractor)),
    ('Standarization', scaler),
    ('Classifier', rf)
])