import os
import warnings
from ebooklib import epub
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module='ebooklib')
warnings.filterwarnings("ignore", category=FutureWarning, module='ebooklib')

def epub_to_pdf(epub_path, pdf_path):
    try:
        # Load EPUB
        book = epub.read_epub(epub_path)

        # Initialize PDF
        pdf_canvas = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        text_object = pdf_canvas.beginText(40, height - 40)

        # Extract text from EPUB
        for item in book.get_items():
            # Check if the item is an HTML or XHTML document
            if item.media_type in ['application/xhtml+xml', 'text/html']:
                # Parse content with BeautifulSoup
                soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                text = soup.get_text()

                # Add text to PDF (wrap lines to avoid overflow)
                for line in text.split('\n'):
                    text_object.textLine(line)

        # Write text to PDF
        pdf_canvas.drawText(text_object)
        pdf_canvas.showPage()
        pdf_canvas.save()

        print(f"Converted {epub_path} to {pdf_path}")
    except Exception as e:
        print(f"Failed to convert {epub_path} to {pdf_path}: {e}")

def convert_epub_directory(epub_dir, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all EPUB files in the directory
    for filename in os.listdir(epub_dir):
        if filename.endswith('.epub'):
            epub_path = os.path.join(epub_dir, filename)
            pdf_filename = filename.replace('.epub', '.pdf')
            pdf_path = os.path.join(output_dir, pdf_filename)

            # Convert the EPUB to PDF
            epub_to_pdf(epub_path, pdf_path)

def main():
    import argparse

    # Default output directory
    default_output_dir = os.path.expanduser("~/default_output_dir")

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Convert EPUB files to PDF.")
    parser.add_argument("epub_dir", help="Path to the directory containing EPUB files")
    parser.add_argument("--output_dir", default=default_output_dir, help=f"Path to save the converted PDF files (default: {default_output_dir})")

    args = parser.parse_args()

    epub_dir = args.epub_dir
    output_dir = args.output_dir

    # Convert EPUB directory
    convert_epub_directory(epub_dir, output_dir)

if __name__ == "__main__":
    main()

