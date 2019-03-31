import sys
import re
from tika import parser
from langdetect import detect

def tika_parser(file_path):
    # Extract text from document
    content = parser.from_file(file_path)
    if 'content' in content:
        text = content['content']
    else:
        return
    # Convert text to string
    text = str(text)
    # Ensure text is utf-8 formatted
    safe_text = text.encode('utf-8', errors='ignore')
    # Escape any \ issues
    safe_text = str(safe_text).replace('\\','\\\\').replace('"', '\\"')
    # Output textxs
    return safe_text

def extract_english_text(text):
    # Detect english text and print it
    for line in text.splitlines():
        # Remove all special characters and except only letters
        line_str = re.sub(r"[^a-zA-Z]+", ' ', line)
        # Check if line is not space or empty
        if (not line_str.isspace()) and line_str:
            # Decode utf8 and detect only english language
            if detect(line_str.decode("utf-8")) == 'en':
                print(line_str)

def set_utf8_encoding():
    # Set default encoding to utf8 (This is not safe thing to do)
    reload(sys)
    sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    # Set default encoders
    set_utf8_encoding()
    # Start parsing
    text = tika_parser('./data/pdf/en_Riyad_us_Saliheen.pdf')
    extract_english_text(text)