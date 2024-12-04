import logging

def global_percentage_of_removed_data(df):
    try:
        total_rows = df.shape[0]
        removed_rows = df[df.isnull().any(axis=1)].shape[0]
        removed_percentage = (removed_rows / total_rows) * 100 if total_rows > 0 else 0
        logging.info(f"Percentage of rows with missing data: {removed_percentage:.3f}%")
        return removed_percentage
    except Exception as e:
        logging.error(f"Error calculating the percentage of removed data: {e}")
        return None

def remove_inconsistent_failures(df):
    try:
        failure_columns = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF']
        if 'Machine failure' in df.columns and all(col in df.columns for col in failure_columns):
            inconsistent_rows = df[
                (df['Machine failure'] == 1) & (df[failure_columns].sum(axis=1) == 0)
            ].index
            logging.info(f"Found {len(inconsistent_rows)} inconsistent rows to remove.")
            df.drop(index=inconsistent_rows, inplace=True)
        else:
            logging.warning("Required columns for identifying inconsistent failures are missing.")
    except Exception as e:
        logging.error(f"Error removing inconsistent failures: {e}")
    return df
