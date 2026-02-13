# Imports Python's built-in os module for working with file paths and directories.
import os

# Defines a function that splits a block of text into smaller "chunks" of about max_tokens words (default 500).
def chunk_text(text, max_tokens=500):
    # turns the full string into a list of words and stores it in an array called chunks
    words = text.split()
    chunks = []

    # for loop slices the list of words every 500 words
    for i in range(0, len(words), max_tokens):
        # Each chunk gets joined back into a string using
        chunk = ' '.join(words[i:i+max_tokens])
        chunks.append(chunk)

    # returns a list of those chunks
    return chunks

def main():
    # the file you want to chunk
    input_path = 'data/sample_final.txt'
    # Folder where individual chunk files will be saved.
    output_dir = 'data/chunks'

    # create output directory if it doesnt exist
    os.makedirs(output_dir, exist_ok=True)

    # read the cleaned final text
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # chunk the text
    chunks = chunk_text(text)

    # loops through each chunk and saves it to its own file
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(output_dir, f'chunk_{i+1}.txt')
        with open(chunk_path, 'w', encoding='utf-8') as f:
            f.write(chunk)

    print(f'{len(chunks)} chunks saved to {output_dir}')

if __name__ == '__main__':
    main()        
            