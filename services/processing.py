import pandas as pd
from parser.hex_parser import process_hex_row

def process_dataframe(df: pd.DataFrame):
    df['custom.235.hex'] = df['custom.235.hex'].fillna('')
    
    parsed_data = df.apply(process_hex_row, axis=1)
    df = pd.concat([df, parsed_data], axis=1)

    return df