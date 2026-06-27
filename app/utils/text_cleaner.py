import re

def text_cleaner(text):
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Replace common unicode characters
    replacements = {
        "\uf0b7": "-",
        "\xa0": " ",
        "\u200b": "",
        "•": "-",
        "▪": "-",
        "●": "-",
        "◦": "-",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove non-printable characters (except newlines)
    text = "".join(ch for ch in text if ch.isprintable() or ch == "\n")

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Trim each line
    lines = [line.strip() for line in text.split("\n")]

    # Collapse multiple blank lines
    cleaned = []
    blank = False

    for line in lines:
        if line == "":
            if not blank:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(line)
            blank = False

    text = "\n".join(cleaned)

    # Normalize colon spacing
    text = re.sub(r"\s*:\s*", ": ", text)

    return text.strip()