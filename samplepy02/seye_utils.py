from time import time
import jwt
import requests
import pandas as pd
import openpyxl

secret = "kG2M@]j*vdPrb4y8u)88fatQz/8'?'{R"

header = {
  "alg": "HS256",
  "typ": "JWT"
}

data = {
  "iss": "ppm-tech-user",
  "iat": int(round(time() * 1000))
}

server_prefix = 'https://smarteye.ebrd-tst.smartkyc.ai/smarteye/t/EBRD/api/LATEST'


def call_api(method, api_to_call, payload={}):
    data["iat"] = int(round(time() * 1000))
    token_ser = jwt.encode(data, secret, algorithm="HS256", headers=header)
    #print(token_ser)
    headers = {
        'Authorization': token_ser
    }
    response = requests.request(method, server_prefix + api_to_call, headers=headers, data=payload)
    #print(response.status_code)
    #print(response.text)
    return response


def unsubscribe_seye_review(review_id):
    # POST /action/subscriptions/reviews/1725454618401/providers/metabase/unsubscribe
    return call_api('POST', f'/action/subscriptions/reviews/{review_id}/providers/metabase/unsubscribe')


def delete_seye_review(review_id):
    # POST /etc/delete/reviews/1725454618401/delete
    # https://smarteye.ebrd-tst.smartkyc.ai/smarteye/t/EBRD/api/LATEST/etc/delete/reviews/1725383425973/delete
    return call_api('POST', f'/etc/delete/reviews/{review_id}/delete')


def get_all_active_seye_reviews():
    # /state/dashboard/summaries?count=50&firstIndex=0&docFilter=all&subscriptionStatus=active&sort=lastRelevantChangeDesc&includeLatestAlerts=3
    first_index = 0
    review_ids = []
    while True:
        api_to_call = f'/state/dashboard/summaries?count=50&firstIndex={first_index}&docFilter=all&subscriptionStatus=active&sort=lastRelevantChangeDesc&includeLatestAlerts=3'
        response_json = call_api('GET', api_to_call).json()
        rows = response_json['rows']
        current_review_ids = [row['reviewId'] for row in rows]
        if current_review_ids:
            review_ids += current_review_ids
            first_index += 50
        else:
            return review_ids


def get_all_inactive_seye_reviews():
    first_index = 0
    review_ids = []
    while True:
        api_to_call = f'/state/dashboard/summaries?count=50&firstIndex={first_index}&docFilter=all&subscriptionStatus=inactive&sort=lastRelevantChangeDesc&includeLatestAlerts=3'
        response_json = call_api('GET', api_to_call).json()
        rows = response_json['rows']
        current_review_ids = [row['reviewId'] for row in rows]
        if current_review_ids:
            review_ids += current_review_ids
            first_index += 50
        else:
            return review_ids


def unsubscribe_review_ids(review_ids):
    for review_id in review_ids:
        response = unsubscribe_seye_review(review_id)
        msg = f'review_id: {review_id}, response: {response.status_code}'
        print(msg)


def delete_review_ids(review_ids):
    for review_id in review_ids:
        response = delete_seye_review(review_id)
        msg = f'review_id: {review_id}, response: {response.status_code}'
        print(msg)


def delete_review_ids_from_csv(csv_file_name):
    active_review_ids_df = pd.read_csv(csv_file_name, header=None)
    print(active_review_ids_df)
    active_review_ids_column = active_review_ids_df[0]
    delete_review_ids(active_review_ids_column)


def unsubscribe_review_ids_from_csv(csv_file_name):
    active_review_ids_df = pd.read_csv(csv_file_name, header=None)
    print(active_review_ids_df)
    active_review_ids_column = active_review_ids_df[0]
    unsubscribe_review_ids(active_review_ids_column)


def save_active_review_ids():
    active_review_ids = get_all_active_seye_reviews()
    active_review_ids_dataframe = pd.DataFrame(active_review_ids)
    active_review_ids_dataframe.to_csv('data/active_review_ids.csv', index=False, header=False)
    print('Saved active review ids', active_review_ids_dataframe)


def save_inactive_review_ids():
    inactive_review_ids = get_all_inactive_seye_reviews()
    inactive_review_ids_dataframe = pd.DataFrame(inactive_review_ids)
    inactive_review_ids_dataframe.to_csv('data/inactive_review_ids.csv', index=False, header=False)
    print('Saved inactive review ids', inactive_review_ids_dataframe)


def load_batch_from_file(file_path):
    api_to_call = f'/action/batches/reviews/file'
    files = {'file': open(file_path, 'rb')}
    data["iat"] = int(round(time() * 1000))
    token_ser = jwt.encode(data, secret, algorithm="HS256", headers=header)
    headers = {
        'Authorization': token_ser
    }
    response = requests.post(server_prefix + api_to_call, headers=headers, files=files)
    print(response.status_code)
    return response


def import_seye_batch(file_name):
    return pd.read_excel(file_name, dtype=str).fillna('')


def save_seye_batch(file_name, excel_df):
    excel_df.to_excel(file_name, index=False)


def split_500_excel():
    excel_df = import_seye_batch('data/smartEYE_batch_ebrd (version 1) top 500.xlsx')
    excel_df['dateOfBirth'] = excel_df['dateOfBirth'].apply(normalize_date)
    print(excel_df)
    no_splits = 10
    split_size = 50
    for batch_index in range(no_splits):
        current_df = excel_df[(batch_index * split_size):((batch_index + 1) * split_size)]
        save_seye_batch(f'data/batch{batch_index + 1:03d}.xlsx', current_df)


def split_full_excel():
    excel_df = import_seye_batch('data/smartEYE_batch_ebrd (version 1) with owners.xlsx')
    excel_df['dateOfBirth'] = excel_df['dateOfBirth'].apply(normalize_date)
    print(excel_df)
    no_splits = 125
    split_size = 500
    for batch_index in range(no_splits):
        current_df = excel_df[(batch_index * split_size):((batch_index + 1) * split_size)]
        save_seye_batch(f'data/batch{batch_index + 1:03d}.xlsx', current_df)


def normalize_date(input_date):
    if input_date.endswith('00:00:00'):
        output_date = input_date[0:11]
        print('>>>C', input_date, output_date)
        return output_date
    if '/' in input_date:
        print('>>>D', input_date)
        return ''
    print('>>>S', input_date)
    return input_date


def get_no_active_review_ids():
    first_index = 0
    api_to_call = f'/state/dashboard/summaries?count=10&firstIndex={first_index}&docFilter=all&subscriptionStatus=active&sort=lastRelevantChangeDesc&includeLatestAlerts=3'
    response_json = call_api('GET', api_to_call).json()
    return response_json['availableRowsCount']
