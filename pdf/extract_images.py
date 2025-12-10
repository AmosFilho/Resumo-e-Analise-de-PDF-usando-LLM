import os
import fitz
from config.loggin_config import logger

def extract_images_from_pdf(filepath: str, output_folder: str) -> None:

    logger.info(f"Extracting images from {filepath}")
    pdf_name = os.path.splitext(os.path.basename(filepath))[0]

    final_output= os.path.join(output_folder, pdf_name)

    # Create the folder
    try:
        os.makedirs(final_output, exist_ok=True)
        logger.debug(f"Directory {final_output} created/exists")
    except OSError:
        logger.error(f"Error in creating {final_output}")
        return

    # Open the folder
    try:
        pdf_doc = fitz.open(filepath)
        logger.info(f"Successfully opened {filepath}")
    except (RuntimeError, OSError, ValueError):
        logger.error(f"Error in opening {filepath}")
        return

    # Read pages and extract images
    for page_num in range(pdf_doc.page_count):
        try:
            page = pdf_doc.load_page(page_num)
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf_doc.extract_image(xref)
                image_bytes = base_image["image"]

                filename = f"image_{page_num}_{img_index}.png"
                full_path = os.path.join(final_output, filename)
                with open(full_path, 'wb') as f:
                    f.write(image_bytes)

                logger.debug(f"Saved image {filename}")

        except (Exception, OSError, ValueError):
            logger.error(f"Error in extracting/saving images of {filepath}")

    pdf_doc.close()
    logger.info(f"Finished extracting images")

