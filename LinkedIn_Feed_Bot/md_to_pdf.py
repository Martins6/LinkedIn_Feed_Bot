import markdown
from xhtml2pdf import pisa 

def convert_md_to_pdf(input_md_filepath, output_pdf_filename):

    with open(input_md_filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    source_html = markdown.markdown(text)

    # open output file for writing (truncated binary)
    result_file = open(output_pdf_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return False on success and True on errors
    return pisa_status.err