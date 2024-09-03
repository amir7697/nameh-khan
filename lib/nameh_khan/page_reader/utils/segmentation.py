import cv2


from sklearn.base import BaseEstimator, TransformerMixin


class SimpleSegmentation(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            blur_kernel_size=(1, 1),
            dilation_kernel_size=(3, 3),
            dilation_iterations=3,
            min_acceptable_contour_area=100,
            threshold_block_size=11,
            threshold_C=30
    ):
        self.blur_kernel_size = blur_kernel_size
        self.dilation_kernel_size = dilation_kernel_size
        self.dilation_iterations = dilation_iterations
        self.min_acceptable_contour_area = min_acceptable_contour_area
        self.threshold_block_size = threshold_block_size
        self.threshold_C = threshold_C

    def transform(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blured_gray_image = cv2.GaussianBlur(gray_image, self.blur_kernel_size, 0)
        threshold_image = cv2.adaptiveThreshold(
            blured_gray_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            self.threshold_block_size,
            self.threshold_C
        )

        # Dilate to combine adjacent text contours
        dilation_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            self.dilation_kernel_size
        )
        dilated_threshold_image = cv2.dilate(
            threshold_image,
            dilation_kernel,
            iterations=self.dilation_iterations
        )

        contours = cv2.findContours(
            dilated_threshold_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        contours = contours[0] if len(contours) == 2 else contours[1]

        box_locations_list = []
        for contour in contours:
            contour_area = cv2.contourArea(contour)
            if contour_area > self.min_acceptable_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                box_locations_list.append({'x1': x, 'y1': y, 'x2': x + w, 'y2': y + h})

        return box_locations_list