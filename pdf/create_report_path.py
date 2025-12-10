import os
from argparse import Namespace
from config.loggin_config import logger

def create_report_path(args: Namespace)-> str:
    try:
        # create a common path to report file
        os.makedirs("utils", exist_ok=True)

        base_name = os.path.basename(args.filename)

        # Remove .pdf extension and spaces
        name_without_ext = os.path.splitext(base_name)[0]

        # Build the report file name
        report_path = os.path.join("utils", f"relatorio-{name_without_ext}.md")

        # Ensure the file is empty before writing
        open(report_path, "w", encoding="utf-8").close()
        logger.info("Initialized report file path")

        return report_path

    except Exception as e:
        logger.exception(f"Error creating report path: {e}")
        raise