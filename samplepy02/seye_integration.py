from time import time, sleep
import jwt
import requests
import pandas as pd
import openpyxl
import seye_utils


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    pass

    # while True:
    #    print(BColors.OKGREEN, seye_utils.get_no_active_review_ids())
    #   sleep(10)


    # seye_utils.save_active_review_ids()
    # seye_utils.save_inactive_review_ids()

    # seye_utils.unsubscribe_review_ids_from_csv('data/active_review_ids.csv')
    # seye_utils.delete_review_ids_from_csv('data/active_review_ids.csv')
    # seye_utils.load_batch_from_file('data/smartEYE_batch_ebrd (version 1)_top_1.xlsx')
    # seye_utils.load_batch_from_file('data/smartEYE_batch_ebrd (version 1) top 500.xlsx')
    # seye_utils.split_500_excel()

    seye_utils.split_full_excel()

    # excel_df = seye_utils.import_seye_batch('data/smartEYE_batch_ebrd (version 1) with owners.xlsx')
    # excel_df = seye_utils.import_seye_batch('data/batch073.xlsx')
    # excel_df['dateOfBirth'] = excel_df['dateOfBirth'].apply(normalize_date)
    # excel_df_2 = excel_df[(excel_df['dateOfBirth'] != '')]
    # print(excel_df_2['dateOfBirth'])

