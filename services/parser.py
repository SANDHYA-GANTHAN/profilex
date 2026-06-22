import re
import fitz

import PyPDF2

import pdfplumber

from docx import Document

import os
import fitz




def extract_text_pdf(path):

    text = ""

    try:

        with open(path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                txt = page.extract_text()

                if txt:
                    text += txt

    except:

        pass

    try:

        with pdfplumber.open(path) as pdf:

            for page in pdf.pages:

                txt = page.extract_text()

                if txt:
                    text += txt

    except:

        pass

    return text


def extract_text_docx(path):

    doc = Document(path)

    return "\n".join(
        para.text for para in doc.paragraphs
    )


def get_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group() if match else ""


def get_phone(text):

    match = re.search(
        r'(\+91[\s\-]?\d{10}|\d{10})',
        text
    )

    if match:
        return match.group()

    return ""
def get_name_from_top_lines(text):

    INVALID_NAMES = {
        "about",
        "about me",
        "summary",
        "profile",
        "objective",
        "skills",
        "experience",
        "education",
        "projects",
        "project",
        "automated",
        "automation",
        "developer",
        "engineer",
        "consultant",
        "crm",
        "siebel",
        "assurance process."
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:20]:

        line = re.sub(r"\(.*?\)", "", line).strip()

        words = line.split()

        # Allow 1 to 4 words
        if not (1 <= len(words) <= 4):
            continue

        if line.lower() in INVALID_NAMES:
            continue

        if any(char.isdigit() for char in line):
            continue

        if "@" in line:
            continue

        if all(
            word.replace(".", "").replace("-", "").isalpha()
            for word in words
        ):
            return line.title()

    return None

def get_name(text):

    lines = text.split("\n")

    blacklist = [
        "developer",
        "engineer",
        "consultant",
        "manager",
        "architect",
        "skills",
        "experience",
        "summary",
        "about me",
        "education",
        "projects",
        "assurance process. ",
        "about",
        "about me",
        "summary",
        "profile",
        "objective",
        "skills",
        "experience",
        "education",
        "projects",
        "project",
        "automated",
        "automation",
        "developer",
        "engineer",
        "consultant",
        "crm",
        "siebel"
        
    ]

    for line in lines[:20]:

        line = line.strip()
        # Ignore email lines
        if "@" in line:
            continue

        # Ignore lines with numbers
        if any(char.isdigit() for char in line):
            continue
        # Ignore very long lines
        if len(line) > 40:
            continue

        # Ignore lines with special symbols
        if "|" in line or ":" in line:
            continue

        if not line:
            continue

        if len(line) > 50:
            continue

        if any(
            word in line.lower()
            for word in blacklist
        ):
            continue

        # Skip phone numbers and email lines
        if any(char.isdigit() for char in line):
            continue

        words = line.split()

        if 1 <= len(words) <= 5:
            return line

    return "Unknown"
def get_name_from_file(path):

    filename = os.path.basename(path)

    filename = os.path.splitext(filename)[0]

    filename = re.sub(r'[_\-]', ' ', filename)

    filename = re.sub(r'\d+', '', filename)

    filename = filename.strip()

    return filename.title()
def get_name_from_pdf_layout(pdf_path):

    INVALID_WORDS = {
        "resume", "summary", "profile", "objective",
        "skills", "experience", "education",
        "developer", "engineer", "consultant",
        "technical", "professional", "about", "me"
    }

    try:
        doc = fitz.open(pdf_path)

        page = doc[0]  # first page only

        blocks = page.get_text("dict")["blocks"]

        candidates = []

        for block in blocks:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                text = ""

                max_size = 0

                for span in line["spans"]:

                    text += span["text"] + " "

                    if span["size"] > max_size:
                        max_size = span["size"]

                text = text.strip()

                if not text:
                    continue

                words = text.split()

                # Allow 1-4 words
                if not (1 <= len(words) <= 4):
                    continue

                # Reject emails
                if "@" in text:
                    continue

                # Reject phone numbers
                if any(ch.isdigit() for ch in text):
                    continue

                # Reject headings
                if any(word.lower() in INVALID_WORDS for word in words):
                    continue

                # Keep only alphabetic names
                if not all(
                    word.replace(".", "").replace("-", "").isalpha()
                    for word in words
                ):
                    continue

                candidates.append((text, max_size))

        doc.close()

        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0].title()

        return None

    except Exception as e:
        print("PDF Layout Name Error:", e)
        return None
def get_name_near_email(text):

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for i, line in enumerate(lines):

        if "@" in line:

            start = max(0, i - 5)

            for j in range(start, i):

                candidate = lines[j]

                words = candidate.split()

                if (
                    1 <= len(words) <= 4
                    and all(
                        word.replace(".", "").replace("-", "").isalpha()
                        for word in words
                    )
                ):
                    return candidate.title()

    return None
def parse_resume(path):

    if path.endswith(".pdf"):
        text = extract_text_pdf(path)
    else:
        text = extract_text_docx(path)

    name = None

    # 1. PDF Layout
    if path.lower().endswith(".pdf"):
        name = get_name_from_pdf_layout(path)

    # 2. Email Based
    if not name:
        name = get_name_near_email(text)

    # 3. Top Lines
    if not name:
        name = get_name_from_top_lines(text)

    # 4. Filename
    if not name:
        name = get_name_from_file(path)

    # Last fallback
    if not name:
        name = "Unknown"

    return {
        "text": text,
        "name": name,
        "email": get_email(text),
        "phone": get_phone(text)
    }