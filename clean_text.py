def clean_text(text):
    # Splits the input text into a list of lines, using the newline character \n.
    lines = text.split('\n')
    # store the cleaned paragraphs.
    cleaned_lines = []
    # holds text temporarily while building paragraphs from broken lines.
    buffer = ''

    # loops through each line and strip() removes whitespace from the beginning and end of the line
    for line in lines:
        stripped = line.strip()
        # If the line is empty (a paragraph break), finish the current paragraph in buffer and reset it.
        if not stripped:
            if buffer:
                cleaned_lines.append(buffer)
                buffer = ''
        else: 
            # If a buffer already exists: 
            if buffer:
                # if current line starts lowercase, it's probably a continuation -> append it to the buffer. Otherwise, treat it as a new paragraph → save the old buffer and start a new one.
                if stripped[0].islower():
                    buffer += ' ' + stripped
                else: 
                    cleaned_lines.append(buffer)
                    buffer = stripped
            else:
                buffer = stripped

    # After the loop ends, add whatever is left in the buffer as the last paragraph.
    if buffer:
        cleaned_lines.append(buffer)

    # Join all paragraphs with double line breaks for readability.
    return '\n\n'.join(cleaned_lines)     

def remove_copyright_lines(text):
    # Split the input text into lines again.
    # Prepare an empty list to hold lines we want to keep.
    lines = text.split('\n')
    filtered_lines = []

    # loop through each line, if it contains any of the unwanted keywords (e.g., ©, "2024"), skip it. Otherwise, keep the line.
    for line in lines:
        if any(keyword in line for keyword in ['©', 'Copyright', 'copyright', '2024', '2023']):
            continue
        filtered_lines.append(line)

    # Join the filtered lines back into a single string.
    return '\n'.join(filtered_lines)

def main():
    # Define where to read from and write to (input, intermediate, and final output).
    input_path = 'data/sample.txt'
    intermediate_path = 'data/sample_cleaned.txt'
    output_path = 'data/sample_final.txt'

    # read original text into raw_text
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # clean broken lines
    cleaned = clean_text(raw_text)

    # save intermediate cleaned text
    with open(intermediate_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    # remove copyright lines
    final_text = remove_copyright_lines(cleaned)  

    # save final cleaned text
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_text)      

    print(f'Cleaning complete. Final text saved to {output_path}')  

# Ensures that the main() function only runs if this script is run directly (not imported into another script).
if __name__ == '__main__':
    main()                                      