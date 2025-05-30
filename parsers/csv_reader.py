import pandas as pd


def return_messges_df():
    messages_df = pd.read_excel("data/person_files_excel.xlsx")  # Update path if needed
    return messages_df
