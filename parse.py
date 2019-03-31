import sys
import re
from tika import parser
from langdetect import detect
from progress.bar import ChargingBar

def semantic_search(text):
    """ Semantic search chapter by chapter"""
    print("Search: ")

def parse_pdf(file_path):
    """ Extract text from pdf document """
    content = parser.from_file(file_path)

    if 'content' in content:
        text = content['content']
    else:
        return

    text = str(text)
    # Ensure text is utf-8 formatted
    safe_text = text.encode('utf-8', errors='ignore')
    # Escape any \ issues
    safe_text = str(safe_text).replace('\\','\\\\').replace('"', '\\"')

    return safe_text

def preprocess(text):
    """ Detect english text and print it """
    print('Processing your document:')
    
    result = ''
    line_length = len(text.splitlines())
    # Progress bar
    bar = ChargingBar('Processing', max=line_length)
    
    for line in text.splitlines():
        # Remove special characters
        line_str = re.sub(r"[^a-zA-Z0-9]+", ' ', line)
        # Check no empty, not contain only numbers
        if (not line_str.isspace()) and line_str and (not bool(re.match('^[0-9 ]+$', line_str))):
            # Detect english language
            if detect(line_str.decode("utf-8")) == 'en':
                result += line_str + '\n'
        
        bar.next()
    bar.finish()

    return result

def set_utf8_encoding():
    """ Set default encoding to utf8 (This is not a safe thing to do) """
    reload(sys)
    sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    # Set default encoders
    set_utf8_encoding()
    # Start parsing
    text = parse_pdf('./data/pdf/en_Riyad_us_Saliheen.pdf')
    text_processed = preprocess(text)
    print(text_processed)
    # Start semantic search
    semantic_search(text_processed)