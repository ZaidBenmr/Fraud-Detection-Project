import pandas as pd
import numpy as np
import datetime
from model.preprocessing import pipeline
from bdd import import_data_region, migrate_data

def predict_one(df) : 
    df['CONSUMPTION_PERIOD']  = pd.to_datetime(df['CONSUMPTION_PERIOD'], format='%Y-%m-%d')
    
    df = df.sort_values("CONSUMPTION_PERIOD", inplace = False).reset_index(drop=True)
    
    is_ = df['CONSUMPTION_PERIOD'].between('2018-02-01', '2022-11-30').any()
    
    if is_ : 
        l = pipeline.predict(df)[0]
        return l
    
    else : 
        
        return 3



def predict_all () :

    REGION = ['BIR.CHIFAE']

    for i in REGION :
        
        df = import_data_region(i)

        df['CONSUMPTION_PERIOD']  = pd.to_datetime(df['CONSUMPTION_PERIOD'], format='%Y-%m-%d')
        df = df[df["METER_INSTALLATION_DATE_ELEC"].notna()]
        df = df[df["COMMERCIAL_AGENCY"].notna()]
        df = df[df["METER_READING_ROUTE"].notna()]
        df = df[df["METER_POWER_ELEC"].notna()]
        
        unique_values_all = df["NUM_CTA_ABT_BT"].unique()
        print("Done Importation")
        
        all_labels = []
        for j in unique_values_all[:100] :
            
            consumer = df[df["NUM_CTA_ABT_BT"] == j].sort_values("CONSUMPTION_PERIOD", inplace = False).reset_index(drop=True)
            consumer = consumer[consumer["CONSUMPTION_PERIOD"].dt.year != 2020].reset_index(drop=True)
            
            '''is_ = ((consumer['CONSUMPTION_PERIOD'].between('2017-01-01', '2019-12-31').any()) or
                (consumer['CONSUMPTION_PERIOD'].between('2021-01-01', '2022-11-30').any())) and \
                (consumer.shape[0] >= 4) '''
            is_ = (consumer.loc[(consumer['CONSUMPTION_PERIOD'] >= '2017-01-01') & (consumer['CONSUMPTION_PERIOD'] <= '2022-12-31')] \
                    .shape[0] >= 5)
            
            if is_ : 
                print (j)
                l = pipeline.predict_proba(consumer)
                
                if l[0][1] > 0.5 :
                        print(j + " -True")
                        all_labels.append([consumer["DELIVERY_POINT_ID"].iloc[0], consumer["NUM_CTA_ABT_BT"].iloc[0],
                            consumer["NUM_CTA_ABT_EA"].iloc[0], consumer["CONSUMER_BILLING_ID"].iloc[0],
                            consumer["DELIVERY_POINT_ADDRESS"].iloc[0], consumer["SUBSCRIPTION_STATUS_LBL"].iloc[-1],
                            consumer["BILLING_CATEGORY_ELEC"].iloc[0],consumer["TYP_RES"].iloc[0], np.around(l[0][1] * 100, decimals=2),
                            i, datetime.datetime.today().strftime('%Y-%m-%d')])
            else : 
                continue
        #migrate_data(all_labels)
        

    return "Done"

        
