import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_dataset(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        return False
    return True

def analyze_failure_relationship(df):
    try:
        if not validate_dataset(df, ['RNF', 'Machine failure']):
            return None

        conditions = df[(df['RNF'] == 1) & (df['Machine failure'] == 0)]
        count = conditions.shape[0]
        rows = conditions.index.tolist()

        logging.info(f"Random=1, Machine=0: {count} occurrences. Rows: {rows}")
        return {"Random=1, Machine=0": {"count": count, "rows": rows}}
    except Exception as e:
        logging.error(f"Error analyzing and counting failures: {e}")
        return None

if __name__ == "__main__":
    setup_logging()