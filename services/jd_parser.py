import PyPDF2
from docx import Document


def extract_jd_text(path):

    if path.endswith(".pdf"):

        text = ""

        with open(path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                txt = page.extract_text()

                if txt:
                    text += txt

        return text

    elif path.endswith(".docx"):

        doc = Document(path)

        return "\n".join(
            para.text
            for para in doc.paragraphs
        )

    return ""