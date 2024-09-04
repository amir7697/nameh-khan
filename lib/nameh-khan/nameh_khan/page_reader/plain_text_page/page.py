import torch 

from sklearn.pipeline import Pipeline

from nameh_khan.page_reader.base import PageReader
from nameh_khan.page_reader.plain_text_page.config import MODEL_PATH
from nameh_khan.page_reader.utils import TopRightIndexer, SimpleSegmentation, LineBasedTextBuilder
from nameh_khan.word_reader import WordReader
from nameh_khan.pre_process import RGB2Gray


class PlainTextPageReader(PageReader):
    def __init__(self):
        self.preprocessing_pipeline = Pipeline([
            ('rgb2gray', RGB2Gray())
        ])
        self.page_segmentation = SimpleSegmentation()
        self.segment_indexer = TopRightIndexer()

        word_reader_model = WordReader()
        word_reader_model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu'), weights_only=False))
        self.text_builder = LineBasedTextBuilder(word_reader_model)
