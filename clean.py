import os
import fitz


def extract_text(data_folder, text_folder):
    if not os.path.exists("text"):
        os.makedirs("text")

    for file in os.listdir(data_folder):
        path = os.path.join(data_folder, file)
        doc = fitz.open(path)

        root, _ = os.path.splitext(file)
        textpath = os.path.join(text_folder, root + ".txt")

        text = ""
        for page in doc:
            text += page.get_text()

        with open(textpath, "w", encoding="utf-8") as f:
            f.write(text)


def clean_text(text_folder):
    for file in os.listdir(text_folder):
        path = os.path.join(text_folder, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        clean_content = " ".join(content.split()).lower()

        with open(path, "w", encoding="utf-8") as fi:
            fi.write(clean_content)
