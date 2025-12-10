import fitz
from llm.model import LocalLLM
from argparse import Namespace
from config.loggin_config import logger



# Method that ask LLM directly
def summarize_text(pdf_text: str, llm: LocalLLM) -> str:
    logger.debug("Request summary from LLM")
    try:
        answer = llm.ask_to_model(f"Resuma o texto a seguir. Texto: {pdf_text}.")
        logger.debug("LLM return a summary successfully")
        return answer
    except Exception as e:
        logger.error(f"Error while summarizing text with LLM: {e}", exc_info=True)
        return ""


def summarize_pdf_file(args: Namespace, report_path: str) -> None:
    logger.info(f"Start summarizing PDF file: {args.filename}")

    pdf_file = None
    llm = None

    # Load LLM
    try:
        llm = LocalLLM("qwen-4b")
        logger.info(f"Local LLM loaded successfully")
    except Exception as e:
        logger.error(f"Error while loading local LLM: {e}", exc_info=True)


    # Load PDF
    try:
        pdf_file = fitz.open(args.filename)
        logger.info(f"PDF file loaded successfully")
    except Exception as e:
        logger.error(f"Error while loading PDF: {e}", exc_info=True)

    text = ""

    # Process each page
    for page_number in range(len(pdf_file)):
        try:
            page = pdf_file[page_number]
            page_txt = page.get_text()
            logger.debug(f"Extracted text from page {page_number}")
            text += summarize_text(page_txt, llm)
        except Exception as e:
            logger.error(f"Error processing page {page_number}: {e}", exc_info=True)

    # Create global summary
    logger.info("Creating global summary from page summaries")
    answer = summarize_text(text, llm)
    pdf_file.close()
    logger.info(f"PDF file closed")
    print(answer)

    # Write the summary in the report .md file
    try:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("## Resumo do Arquivo ##\n")
            f.write(answer)
            f.write("\n")
    except Exception as e:
        logger.error(f"Error while writing summary to report file: {e}", exc_info=True)
