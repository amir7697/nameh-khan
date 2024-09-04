from sklearn.base import BaseEstimator, TransformerMixin


class PixelNormalizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def transform(self, image):
        return image#.astype('float32')