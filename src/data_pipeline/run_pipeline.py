from log import setup_logger

logger = setup_logger(name="run_pipeline", log_file="logs/pipeline.log")

def run_pipeline():
    script_dir = os.path.dirname(__file__)
    script_files = [
        f for f in os.listdir(script_dir) if f.endswith(".py") and f.startswith(("01_", "02_", "03_", "04_", "05_", "06_"))
    ]
    script_files.sort()

    logger.info("Starting pipeline execution...")
    for script in script_files:
        script_path = os.path.join(script_dir, script)
        logger.info(f"Running {script}...")
        try:
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Successfully executed {script}.")
            else:
                logger.error(f"Error in {script}: {result.stderr}")
        except Exception as e:
            logger.critical(f"Critical failure in {script}: {e}")
            raise
    logger.info("Pipeline execution completed.")