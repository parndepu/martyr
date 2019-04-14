import sys
import re
from tika import parser
from langdetect import detect
from progress.bar import ChargingBar

def semantic_search(text):
    """ Semantic search algorithms find specific keyword in chapter"""

    # Get keyword input
    keyword = raw_input("Search keyword (type 'exit' to exit the program): ")

    while keyword != "exit":
        # Get chapter input
        chapter = input("Chapter (type 0 for all chapters, or specific number 1 to 372): ")
        # Iterate all over the text
        for idx,elem in enumerate(text.splitlines()):
            # All chapters
            if chapter == 0:
                # Search by keyword (need to lower case all letters)
                pos = elem.lower().find(keyword.lower())
                if pos != -1:
                    sentence = elem[ pos: len(elem) - 1]
                    # Use list to track the full stop
                    current_elem = sentence.split('.')
                    # Create empty space between line
                    print(' ')
                    # If no full stop find the next line
                    counter = 1
                    while len(current_elem) < 2:
                        sentence += " " + text.splitlines()[(idx + counter) % len(text.splitlines())]
                        current_elem = sentence.split('.')
                        counter += 1

                    print(sentence.split('.')[0] + '.')
            else:
                current_chapter = elem.lower().split(' ')
                # This condition will search on specific chapter
                if len(current_chapter) == 3:

                    if current_chapter[0].find('chapter') != -1 and int(current_chapter[1]) == int(chapter):
                        # Set starting line counter
                        line_counter = 1
                        new_chapter = current_chapter
                        # Keep iterate if still in the same chapter
                        while new_chapter[0].find('chapter') != -1 and int(new_chapter[1]) == int(chapter):
                            # Get next line
                            new_line = text.splitlines()[(idx + line_counter) % len(text.splitlines())]
                            pos = new_line.lower().find(keyword.lower())
                            # Check if keyword is existed
                            if pos != -1:
                                sentence = new_line[ pos: len(new_line) - 1]
                                # Use list to track full stop
                                current_elem = sentence.split('.')
                                # Create empty space between line
                                print(' ') 
                                # If no full stop find the next line
                                counter = line_counter
                                while len(current_elem) < 2:
                                    sentence += " " + text.splitlines()[(idx + counter) % len(text.splitlines())]
                                    current_elem = sentence.split('.')
                                    counter += 1
                                print(sentence.split('.')[0] + '.')
                            # Find new chapter
                            find_chapter = new_line.lower().split(' ')
                            line_counter += 1
                            # Track the next chapter
                            if len(find_chapter) == 3 and find_chapter[0].find('chapter') != -1 and int(find_chapter[1]) != int(chapter):
                                new_chapter = find_chapter
        
        # Get keyword input to iterate back
        keyword = raw_input("Search keyword (type 'exit' to exit the program): ")

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
    print('Processing .pdf document:')
    
    result = ''
    line_length = len(text.splitlines())
    # Progress bar
    bar = ChargingBar('Processing', max=line_length)
    # Add chapter indexing
    # Sentences
    
    for line in text.splitlines():
        # Remove special characters
        line_str = re.sub(r"[^a-zA-Z0-9.]+", ' ', line)
        # Check no empty, not contain only numbers
        if (not line_str.isspace()) and line_str and (not bool(re.match('^[0-9 .]+$', line_str))):
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
    # print(text_processed)
    # Start semantic search
    semantic_search(text_processed)