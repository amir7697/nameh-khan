CHARACTER_WHITE_LIST = ' ً!*ءىەاآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ()1234567890؟/»«؛.:،أآإؤ+“”%' + '\u200c'

MODEL_PARAMS = {
    'in_channels': 1,
    'num_classes': len(CHARACTER_WHITE_LIST) + 1,
    'blank_label': len(CHARACTER_WHITE_LIST),
    'gru_hidden_size': 64,
    'gru_num_layers': 2,
    'bidirectional': True,
    'first_fully_connected_output_size': 64,
    'scale': 12,
    'desired_image_height': 50,
    'desired_image_width': 200
}

ENCODING_DICT = {character: index for index, character in enumerate(CHARACTER_WHITE_LIST)}
ENCODING_DICT['blank'] = len(CHARACTER_WHITE_LIST)

DECODING_DICT = {encoding: character for encoding, character in enumerate(CHARACTER_WHITE_LIST)}
DECODING_DICT[len(CHARACTER_WHITE_LIST)] = 'blank'