from sklearn.pipeline import Pipeline

from nameh_khan.page_reader import PageReader
from nameh_khan.page_reader.utils import TopRightIndexer, SimpleSegmentation, LineBasedTextBuilder


class PlainTextPageReader(PageReader):
    def __init__(self, word_reader_model):
        self.preprocessing_pipeline = Pipeline([])
        self.page_segmentation = SimpleSegmentation()
        self.segment_indexer = TopRightIndexer()
        self.text_builder = LineBasedTextBuilder(word_reader_model)
