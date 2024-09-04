import cv2


from sklearn.base import BaseEstimator, TransformerMixin


class RGB2Gray(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def transform(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)