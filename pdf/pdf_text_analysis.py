import argparse
import re
import os
import heapq
from collections import Counter
import fitz
from argparse import Namespace
from config.loggin_config import logger

def detect_titles_and_sections(pdf: fitz.Document) -> dict:
    import statistics
    logger.info("Detecting titles and sections...")

    titles = []
    sections = []

    # Regex for numbered sections
    section_pattern = re.compile(
        r"^\d+(\.\d+)*[\s\-–]*.+",
        re.IGNORECASE
    )

    # Collect all font sizes in the document
    all_sizes = []
    for page in pdf:
        for block in page.get_text("dict").get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    all_sizes.append(span["size"])

    if not all_sizes:
        return {"titles": [], "sections": []}

    max_font = max(all_sizes)
    common_font = statistics.mode(all_sizes)  # mode: most common font size

    logger.info(f"Max font size = {max_font}")
    logger.info(f"Most common font size (body text) = {common_font}")

    # Thresholds
    section_threshold = common_font * 1.55   # if > 55% larger than the common font → section/subsection

    # Process each page
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        page_dict = page.get_text("dict")

        for block in page_dict.get("blocks", []):
            if "lines" not in block:
                continue

            # Extract the block text
            full_text = " ".join(
                span["text"]
                for line in block["lines"]
                for span in line["spans"]
            ).strip()

            if not full_text:
                continue

            # Compute average font size for the block
            font_sizes = [
                span["size"]
                for line in block["lines"]
                for span in line["spans"]
            ]
            avg_font = sum(font_sizes) / len(font_sizes)

            # Bold detection
            is_bold = any(
                "Bold" in span["font"] or (span["flags"] & 2)
                for line in block["lines"]
                for span in line["spans"]
            )

            # Search main title as the absolute largest font in the document
            if avg_font == max_font and len(full_text.split()) <= 20:
                titles.append((page_number + 1, full_text))
                logger.debug(f"Main title detected: {full_text}")
                continue

            # Numbered section - even if font size is similar, numbers indicate a section
            if section_pattern.match(full_text):
                sections.append((page_number + 1, full_text))
                logger.debug(f"Numbered section detected: {full_text}")
                continue

            # Section by font size - any text significantly larger than the common font is a section/subsection
            if avg_font > section_threshold and len(full_text.split()) <= 15:
                sections.append((page_number + 1, full_text))
                logger.debug(f"Section by font size detected: {full_text}")
                continue

            # Bold titles/subtitles (fallback detection)
            if is_bold and len(full_text.split()) <= 12 and avg_font > common_font:
                sections.append((page_number + 1, full_text))
                logger.debug(f"Bold subsection detected: {full_text}")
                continue

    return {
        "titles": titles,
        "sections": sections
    }


# (OPTIONAL) method to format the file size to bytes measures
def format_file_size_unit(size_value: int) -> str:
    units = ["bytes", "KB", "MB", "GB", "TB"]
    size = size_value
    unit_index = 0

    while size > 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"

def read_file_with_argparse() -> Namespace:
    parser = argparse.ArgumentParser(description="Read a file from command line.")
    parser.add_argument("filename", help="The path to the file to read")
    args = parser.parse_args()
    logger.info(f"File receive as argument: {args.filename}")
    return args

def extract_text_from_pdf(doc: fitz.Document) -> str:
    logger.info("Extracting text from PDF...")
    text = []
    for page in doc:
        logger.info(f"Extracting text from {page}...")
        text.append(page.get_text("text"))
    return "\n".join(text)

def file_analysis(args: Namespace, report_path: str) -> None:
    logger.info("File analysis started...")
    try:
        pdf_document = fitz.open(args.filename)
        logger.info(f"Successfully opened pdf file: {args.filename}")
    except Exception as e:
        logger.error(f"Error opening {args.filename}: {e}")
        return

    # Structural Analysis(titles and sections)
    structure = detect_titles_and_sections(pdf_document)

    titles = structure["titles"]
    sections = structure["sections"]


    # Pages Number
    num_pages = len(pdf_document)
    print(f"Número de páginas: {num_pages}")

    # Extract the text
    text = extract_text_from_pdf(pdf_document)

    # Words Number
    formated_text = re.findall(r'\b\w+\b', text.lower())
    total_words = len(formated_text)

    print(f"Total de palavras: {total_words}")

    # File Size
    file_size_bytes = os.path.getsize(args.filename)
    print(f"Tamanho do documento em bytes: {file_size_bytes}")

    #  Frequent words search section
    stop_words = [
        "a", "à", "o", "os", "as", "um", "uma", "de", "da", "do", "das", "dos",
        "em", "no", "na", "nos", "nas", "por", "para", "com",
        "e", "é", "ou", "mas",
        "que", "quem", "qual",
        "se", "sem",
        "eu", "tu", "ele", "ela", "nós", "vos", "eles", "elas",
        "me", "te", "lhe", "nos", "vos", "lhes",
        "isso", "isto", "aquilo", "esse", "essa", "aquele", "aquela",
        "este", "esta",
        "sua", "seu", "suas", "seus",
        "não", "sim",
        "já", "ainda",
        "como", "quando", "onde",
        "muito", "muita", "muitos", "muitas",
        "pouco", "pouca", "poucos", "poucas"
    ]
    # Filter the stop words in original text
    logger.info(f"Filtering out stopwords")
    text_filtered = [word for word in formated_text if word not in stop_words and len(word) > 1]
    cnt = Counter(text_filtered)

    #Most frequent words search
    k = 10
    top_k_words = heapq.nlargest(k, cnt.items(), key=lambda x: x[1])
    print(f"{k} palavras mais comums e suas frequências: {top_k_words}")

    #Distincted Words Result
    distinct_words_amount = Counter(text_filtered).keys()
    print(f"Quantidade de Palavras Distintas(após filtragem): {len(distinct_words_amount)}\n")

    pdf_document.close()
    logger.info("PDF closed.")

    # Write into the shared report file
    with open(report_path, "a", encoding="utf-8") as f:
        # Base file analysis
        f.write("## Análise do Arquivo ##\n")
        f.write(f"- **Nome do arquivo:** `{os.path.basename(args.filename)}`\n")
        f.write(f"- **Número de páginas:** {num_pages}\n")
        f.write(f"- **Número de palavras:** {total_words}\n")
        f.write(f"- **Tamanho em bytes do arquivo:** `{file_size_bytes}`\n")
        f.write(f"- **{k} palavras mais comuns e suas frequências:** {top_k_words}\n")
        f.write(f"- **Quantidade de Palavras Distintas(após filtragem):** {len(distinct_words_amount)}\n")
        f.write("\n")

        # Structure analysis report (Titles and sections)
        f.write("## Estrutura Detectada \n")
        f.write("\n### Títulos Detectados ###\n")
        if titles:
            for p, t in titles:
                f.write(f"- **[Página {p}]** {t}\n")
        else:
            f.write("- **Nenhum título detectado.**\n")

        f.write("\n### Seções Detectadas ###\n")
        if sections:
            for p, s in sections:
                f.write(f"- **[Página {p}]** {s}\n")
        else:
            f.write("- **Nenhuma seção detectada.**\n")

        f.write("\n")

    logger.info("File analysis completed.")