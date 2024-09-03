def encode_character(label, alphabet_to_num_dictionary):
    return [alphabet_to_num_dictionary[character] for character in label]

def decode_text(encoded_text, alphabets_decoding):
    return ''.join(alphabets_decoding[int(character)] for character in encoded_text)