import fitz  # PyMuPDF

def highlight_text_in_pdf(input_pdf_path, output_pdf_path, target_text):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)

    # Iterate through each page of the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Search for the target text and highlight it
        matches = page.search_for(target_text)
        for match in matches:
            # Highlight the found text
            page.add_highlight_annot(match)

    # Save the modified PDF to a new file
    pdf_document.save(output_pdf_path)
    pdf_document.close()

if __name__ == "__main__":
    input_pdf_path = "Extracto_16-05-2024_162025_.pdf"
    output_pdf_path = "output_highlighted.pdf"
    target_text = "TRF. P/O eppf Services S.A."

    highlight_text_in_pdf(input_pdf_path, output_pdf_path, target_text)
