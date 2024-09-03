from sklearn.base import BaseEstimator, TransformerMixin


class LineBasedTextBuilder(BaseEstimator, TransformerMixin):
    def __init__( self, word_reader_model):
        self.word_reader_model = word_reader_model


    def transform(self, word_image_list):
        final_text = ''
        current_line = 0
        for i, word_image_item in enumerate(word_image_list):
            word_text = self.word_reader_model(word_image_item['image'])
            if word_image_item['line'] > current_line:
                current_line = word_image_item['line']
                final_text += '\n'
            else:
                final_text += ' '

            final_text += word_text

        return final_text