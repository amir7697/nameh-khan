from sklearn.base import BaseEstimator, TransformerMixin


class PageReader(BaseEstimator, TransformerMixin):
    def __init__(self, word_reader_model):
        raise NotImplementedError

    def transform(self, image):
        pre_processed_image = self.preprocessing_pipeline.transform(image)
        box_locations_list = self.page_segmentation.transform(pre_processed_image)
        word_image_list = self.segment_indexer.transform(pre_processed_image, box_locations_list)
        text = self.text_builder.transform(word_image_list)
        return text
