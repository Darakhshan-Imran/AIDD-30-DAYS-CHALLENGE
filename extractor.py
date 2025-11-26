import pypdf

def extract_pdf_text(file_path: str) -> str:
    """
    Extracts raw text from a PDF file using PyPDF.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The combined raw text from all pages of the PDF, or an empty string if
        the file cannot be processed or contains no text.
    """
    text = ""
    try:
        reader = pypdf.PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.strip() + "\n" # Add a newline for basic separation
    except pypdf.errors.PdfReadError:
        # Handle cases where the PDF is corrupted or cannot be read
        return ""
    except Exception as e:
        # Catch any other unexpected errors during processing
        print(f"Error extracting text from {file_path}: {e}")
        return ""
    return text.strip()

if __name__ == '__main__':
    # Simple test case (replace with an actual PDF file path for testing)
    # create a dummy pdf file for testing
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(500, 500)
    writer.add_blank_page(500, 500)
    with open("dummy.pdf", "wb") as fp:
        writer.write(fp)

    test_file = "dummy.pdf" # Replace with your test PDF
    # For a real test, you'd want a PDF with content.
    # For now, this just tests error handling and basic flow.
    extracted_content = extract_pdf_text(test_file)
    print(f"Extracted content:\n{extracted_content}")
    # You can add more comprehensive tests with actual PDF files here.

