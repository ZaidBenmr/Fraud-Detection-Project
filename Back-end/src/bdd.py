import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pyodbc
import datetime
import locale
from io import BytesIO

# Define the connection parameters to the SQL Server
server_name = 'DESKTOP-OKBTQGT'
database_name = 'Fraudseeker'
user_name = 'sa'
password = '123456'

# Define the connection string to connect to the database
connection_string = f"Driver=ODBC Driver 17 for SQL Server;Server={server_name};Database={database_name};UID={user_name};PWD={password}"

def import_data_one(num) : 

    # Define the name of the table in the database
    table_name = 'CSO'

    # Define the SQL query with the filters
    sql_query = f"""
    SELECT * FROM {table_name}
    WHERE TYP_RES = 'BT'
    AND NUM_CTA_ABT_BT = '{num}'

    """

    # Create a connection to the database
    conn = pyodbc.connect(connection_string)

    # Execute the query and load the results into a pandas DataFrame
    df = pd.read_sql(sql_query, conn, parse_dates=["METER_INSTALLATION_DATE_EAU", "METER_INSTALLATION_DATE_ELEC", "CONSUMPTION_PERIOD"])

    # Close the database connection
    conn.close()

    return df

def import_data_region(region) : 

    # Define the name of the table in the database
    table_name = 'CSO'

    # Define the SQL query with the filters
    sql_query = f"""
    SELECT * FROM {table_name}
    WHERE TYP_RES = 'BT'
    AND REGION = '{region}'
    """

    # Create a connection to the database
    conn = pyodbc.connect(connection_string)

    # Execute the query and load the results into a pandas DataFrame
    df = pd.read_sql(sql_query, conn, parse_dates=["METER_INSTALLATION_DATE_EAU", "METER_INSTALLATION_DATE_ELEC", "CONSUMPTION_PERIOD"])

    # Close the database connection
    conn.close()

    return df

def migrate_data (listFraud) :

    '''listFraud_flat = np.array(listFraud, dtype=object)
    df = pd.DataFrame(data=listFraud_flat, columns=["DELIVERY_POINT_ID", "NUM_CTA_ABT_BT", "NUM_CTA_ABT_EA", "CONSUMER_BILLING_ID",
                                                    "DELIVERY_POINT_ADDRESS", "SUBSCRIPTION_STATUS_LBL", "BILLING_CATEGORY_ELEC", 
                                                    "METIER", "PROBABILITE", "REGION", "DATE_ANALYSE"])
    
    # Define the engine and connection string to connect to the database
    engine = create_engine(f"mssql+pyodbc://{user_name}:{password}@{server_name}/{database_name}?driver=ODBC Driver 17 for SQL Server")

    # Define the name of the table in the database
    table_name = 'ResultsFraud'

    # Write the Pandas DataFrame to the database table
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    # Close the database connection
    engine.dispose()'''
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()

    for row in listFraud:
        query = "EXEC sp_InsertNewFraudData '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, '{9}', '{10}'".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        cursor.execute(query)

    conn.commit()

def cards () :
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)

    table_name = 'ResultsFraud'
    cursor = conn.cursor()

    # Execute the query and fetch the results
    cursor.execute(f"""
                SELECT COUNT(*) as total_rows, COUNT(CASE WHEN CONFIRMATION = 1 THEN 1 END) as ConfirmedRows
                FROM {table_name}
                """)
    n_fraud = cursor.fetchall()

    cursor.execute(f"""
                SELECT MAX(DATE_ANALYSE) as Dernier_data_analyse, COUNT(*) as TotalRows
                FROM {table_name}
                WHERE DATE_ANALYSE = (SELECT MAX(DATE_ANALYSE) FROM {table_name})
                """)
    last_date_info = cursor.fetchall()

    # set the locale to French
    locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')

    # Cards Informations
    total_frauds            = n_fraud[0][0]
    total_confirme          = n_fraud[0][1]
    last_date_str           = last_date_info[0][0].strftime('%d, %B, %Y').replace(',','').title()
    next_date_str           = (last_date_info[0][0] + datetime.timedelta(days=7)).strftime('%d, %B, %Y').replace(',','').title()
    total_frauds_last_date  = last_date_info[0][1]
    
    # Close the database connection
    conn.close()

    return {"total"             : total_frauds,
            "confirme"          : total_confirme,
            "last_date"         : last_date_str,
            "next_date"         : next_date_str,
            "total_last_date"   : total_frauds_last_date
            }

def fraud_detectd_confrmed () : 
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)
    table_name = "ResultsFraud"
    
    # Execute the query and fetch the results
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT 
        REGION, 
        COUNT(*) as TotalRows, 
        COUNT(CASE WHEN CONFIRMATION = 1 THEN 1 END) as ConfirmedRows
    FROM 
        {table_name}
    GROUP BY 
        REGION

    ''')
    n_fraud_conf_region = cursor.fetchall()

    # Close the database connection
    conn.close()
    labels = []
    x3 = []
    y3 = []
    for i, j, k in n_fraud_conf_region:
        labels.append(i)
        x3.append(j)
        y3.append(k)
    x_sorted3, y_sorted3, labels_sorted3  = zip(*sorted(zip(x3, y3, labels), key=lambda pair: pair[1], reverse=True))

    return {
        "x"         : x_sorted3,
        "y"         : y_sorted3,
        "labels"    : labels_sorted3
    }

def fraud_par_region () :
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)

    table_name = 'ResultsFraud'
    cursor = conn.cursor()

    cursor.execute(f"""
                SELECT REGION, COUNT(*) as TotalRows
                FROM {table_name}
                GROUP BY REGION
                """)
    
    n_fraud_region = cursor.fetchall()
    x = []
    y = []
    for i, j in n_fraud_region : 
        x.append(i)
        y.append(j)
    x_sorted, y_sorted = zip(*sorted(zip(x, y), key=lambda pair: pair[1]))
    return {"x" : x_sorted,
            "y" : y_sorted 
            }

def fraud_conf_det_encour () : 
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)
    table_name = "ResultsFraud"

    # Execute the query and fetch the results
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT 
        COUNT(CASE WHEN CONFIRMATION IS NULL THEN 1 END) as NullValues,
        COUNT(CASE WHEN CONFIRMATION = 0 THEN 1 END) as ZeroValues,
        COUNT(CASE WHEN CONFIRMATION = 1 THEN 1 END) as OneValues
    FROM 
        {table_name}
    ''')
    n_fraud_conf = cursor.fetchall()

    # Close the database connection
    conn.close()

    values=[]
    for i in n_fraud_conf[0]:
        values.append(i)

    return {"values" : values}

def fraud_billing_cat () :

    # Create a connection to the database
    conn = pyodbc.connect(connection_string)
    table_name = "ResultsFraud"

    # Execute the query and fetch the results
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT BILLING_CATEGORY_ELEC, COUNT(*) as TotalRows
    FROM {table_name}
    GROUP BY BILLING_CATEGORY_ELEC
    """)
    n_BL_region = cursor.fetchall()
    # Close the database connection
    conn.close()
    billing = []
    nb = []
    for i, j in n_BL_region: 
        billing.append(i)
        nb.append(j)
    billing, nb = zip(*sorted(zip(billing, nb), key=lambda pair: pair[1]))
    return {"billing" : billing,
            "nb"      : nb
            }

def fraud_sub_status () :
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)

    table_name = 'ResultsFraud'
    # Execute the query and fetch the results
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT SUBSCRIPTION_STATUS_LBL, COUNT(*) as TotalRows
    FROM {table_name}
    GROUP BY SUBSCRIPTION_STATUS_LBL
    """)
    n_SBL_region = cursor.fetchall()

    # Close the database connection
    conn.close()
    
    status = []
    nb = []
    for i, j in n_SBL_region: 
        status.append(i)
        nb.append(j)

    return {"status" : status,
            "nb" : nb 
            }

def fraud_detectd_lastdate_par_region () :
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)
    table_name = "ResultsFraud"
    # Execute the query and fetch the results
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT REGION, COUNT(*) as TotalRows, MAX(DATE_ANALYSE) as MaxDate
            FROM {table_name}
            WHERE DATE_ANALYSE = (SELECT MAX(DATE_ANALYSE) FROM {table_name})
            GROUP BY REGION
            """)
    n_fraud_rd = cursor.fetchall()

    # Close the database connection
    conn.close()
    x = []
    y = []
    for i, j, k in n_fraud_rd: 
        x.append(i)
        y.append(j)

    x_sorted, y_sorted = zip(*sorted(zip(x, y), key=lambda pair: pair[1], reverse=True))

    return {
            "x" : x_sorted,
            "y" : y_sorted,
            "date" : k.strftime('%d, %B, %Y').replace(',','').title()
    }

## Sending Data as Excel Files

def fraud_analyse_dates () : 
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)
    table_name = "ResultsFraud"
    
    # Execute the query and fetch the results
    cursor = conn.cursor()
    cursor.execute(f'''SELECT DISTINCT DATE_ANALYSE
            FROM {table_name}
            ORDER BY DATE_ANALYSE DESC
            ''')
    n_fraud_date = cursor.fetchall()

    # Close the database connection
    conn.close()
    date_analyse = []

    for i in n_fraud_date: 
        date_analyse.append(i[0].strftime('%d, %B, %Y').replace(',','').title())

    return {
        "dates" : date_analyse
    }

def fraud_data_by_date (DATE_ANALYSE) :
    # Create a connection to the database
    conn = pyodbc.connect(connection_string)
    table_name = "ResultsFraud"

    # Converting date d'analyse
    DATE_ANALYSE = datetime.datetime.strptime(DATE_ANALYSE, "%d %B %Y")
    DATE_ANALYSE = DATE_ANALYSE.strftime('%Y-%m-%d')

    # Execute the query and fetch the results
    cursor = conn.cursor()
    if DATE_ANALYSE == "Tout" :
        cursor.execute(f"""
                    SELECT *
                    FROM {table_name}
                    """)
    else :
        cursor.execute(f"""
                    SELECT *
                    FROM {table_name}
                    WHERE DATE_ANALYSE = '{DATE_ANALYSE}'
                    """)
    # Fetch the results
    results = cursor.fetchall()

    # Create a DataFrame from the results
    columns = [column[0] for column in cursor.description]
    data = [list(row) for row in results]

    # Specify the column data types
    dtype_map = {column: 'datetime64[ns]' if column == 'DATE_ANALYSE' else None for column in columns}

    df = pd.DataFrame(data, columns=columns).astype(dtype_map)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    return excel_file