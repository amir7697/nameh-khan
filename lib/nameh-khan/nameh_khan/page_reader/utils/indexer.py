import pandas as pd


from sklearn.base import BaseEstimator, TransformerMixin


class TopRightIndexer(BaseEstimator, TransformerMixin):
    def __init__( self):
        pass

    def transform(self, image, box_locations_list):
        box_locations_pdf = (
            pd.DataFrame(box_locations_list)
            .sort_values(by=['y1'], ascending=[True])
            .assign(lineChange=lambda x: (x.y1 > x.y2.shift(1)).astype(int))
            .assign(lineNumber=lambda x: x.lineChange.cumsum())
            .sort_values(by=['lineNumber', 'x2'], ascending=[True, False])
            .reset_index(drop=True)
        )

        image_list = [
            {
                'idx': row.Index,
                'line': row.lineNumber,
                'image': (image[row.y1: row.y2, row.x1: row.x2]).astype('float32') / 255 #todo: this is not good 
            }
            for row in box_locations_pdf.itertuples()
        ]

        return image_list