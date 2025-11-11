import pandas as pd
import json
from pandas import json_normalize
import logging
import sys
import traceback
 
def main():
#    -------csv file processing ---------
 
    csv_file_path = '/Users/yongyongli/Downloads/chata_test/crm_leads.csv' 
    
    df_crm = pd.read_csv(csv_file_path)
    # Format the 'creation_date' to YYYY-MM-DD string format
    df_crm['creation_date'] = pd.to_datetime(df_crm['creation_date'] )

    # remove duplicates based on email, keep the records with the latest creation_date
    df_crm = df_crm.sort_values(by='creation_date', ascending=False)
    df_crm = df_crm.drop_duplicates(subset='email', keep="first")

    # Standardize the 'full_name' to title case
    df_crm.full_name = df_crm.full_name.str.title()
    



    #  -------json file processing ---------

    json_file_path = '/Users/yongyongli/Downloads/chata_test/web_activity.json'
    df_web = pd.read_json(json_file_path, lines=True)
    df_web['user_uuid'] = df_web['user_uuid'].str.strip()

    # separate error and valid data
    df_web_error = df_web[ df_web['user_uuid'].isnull() | (df_web['user_uuid'] == '') ]

    # write error data to a log file
    df_web_error.to_csv('web_error_log.txt', 
              sep=' ', 
              index=True, 
              header=True)
    
    df_web_valid = df_web[ ~(df_web['user_uuid'].isnull() | (df_web['user_uuid'] == '') ) ]

    #  -------txt file processing ---------


    txt_file_path = '/Users/yongyongli/Downloads/chata_test/transactions.txt'
    df_trans = pd.read_csv(txt_file_path, sep='|' )

    # clean the data, convert amount to numeric, strip user_uuid 
    df_trans['user_uuid'] = df_trans['user_uuid'].str.strip()
    df_trans.amount = pd.to_numeric(df_trans.amount, errors='coerce')
    

    #  -------data merging and final processing ---------
    #  the crm_leads data cannot be joined as there is no common key with the other two datasets.

    df_customers = pd.merge( df_trans, df_web_valid ,  on='user_uuid',    how='left' )
    df_customers_error = df_customers[ df_customers['amount']< 0]
    df_customers_valid = df_customers[ df_customers['amount']>= 0]
#  write error transactions to a log file
    with open('transaction_error_log.txt', 'w') as f:
        for (index, row) in df_customers_error.iterrows():
            f.write( f"transaction_id: {row['transaction_id']}, Negative amount {row['amount']}\n" )
        
    
    file_path = '/Users/yongyongli/Downloads/chata_test/customer_360.parquet'
    
    df_customers_valid.to_parquet(file_path)



 
# Run your main script here:
if __name__ == '__main__':
    main()