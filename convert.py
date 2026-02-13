from pdfminer.high_level import extract_text

def convert_pdf_to_text(input_path, output_path):
    # extract text from pdf
    text = extract_text(input_path)

    # save it to a .txt file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

# example: convert sample.pdf to sample.txt
convert_pdf_to_text('data/WhatisSociology.pdf', 'data/sample.txt')        