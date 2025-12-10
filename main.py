from pdf.extract_images import extract_images_from_pdf
from pdf.pdf_text_analysis import read_file_with_argparse, file_analysis
from llm.summarize import summarize_pdf_file
from pdf.create_report_path import create_report_path

def main():
    # Read the file via CLI
    args = read_file_with_argparse()

    report_path = create_report_path(args)

    # Generate the file analysis report
    file_analysis(args, report_path)

    # Summarize the pdf content using the LLM
    summarize_pdf_file(args, report_path)

    # Extract Images and store in the images folder
    extract_images_from_pdf(args.filename, "images")



if __name__ == "__main__":
    main()
