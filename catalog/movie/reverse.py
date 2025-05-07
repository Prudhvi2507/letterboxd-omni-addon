import json

def reverse_json(input_file, output_file):
    # Load the JSON data from input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if 'metas' exists and is a list
    if 'metas' in data and isinstance(data['metas'], list):
        data['metas'].reverse()  # Reverse the list in-place

    # Save the modified data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Example usage
input_filename = 'watchlist.json'
output_filename = 'watchlist_r.json'
reverse_json(input_filename, output_filename)
