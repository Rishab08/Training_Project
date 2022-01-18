from .utils import UserTests
import pandas as pd

SHEETNAMES = ["create_user"]


def run_tests(test_excel_file):
    test_excel_file.open()
    test_data_create_user = pd.read_excel(test_excel_file, sheet_name=SHEETNAMES[0])
    user_tests = UserTests()
    tested_file = user_tests.test_create_users(test_data_create_user)
    return tested_file
