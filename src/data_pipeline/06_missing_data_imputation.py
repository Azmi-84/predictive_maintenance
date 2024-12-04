import logging
from config import COLUMNS

def target_anomalies(df):
    if not validate_dataset(df, COLUMNS["failure_columns"]):
        return df

    try:
        failure_mapping = {
            'TWF': 'Tool Wear Failure',
            'HDF': 'Heat Dissipation Failure',
            'PWF': 'Power Failure',
            'OSF': 'Overstrain Failure',
            'RNF': 'Random Failure'
        }
        df['Failure Type'] = df[COLUMNS["failure_columns"]].idxmax(axis=1).map(failure_mapping)
        logging.info(f"Derived 'Failure Type' column:\n{df['Failure Type'].value_counts()}")
    except Exception as e:
        logging.error(f"Error processing target anomalies: {e}")
    return df

def remove_rnf(df):
    try:
        if 'Failure Type' in df.columns:
            idx_RNF = df[df['Failure Type'] == 'Random Failure'].index
            df.drop(index=idx_RNF, inplace=True)
            logging.info(f"Removed Random Failures: {len(idx_RNF)} rows.")
        else:
            logging.warning("'Failure Type' column not found.")
    except Exception as e:
        logging.error(f"Error removing Random Failures: {e}")
    return df
