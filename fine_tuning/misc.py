import cv2
import numpy as np
import torch.nn as nn

from sklearn.base import BaseEstimator, TransformerMixin


class Resizer(BaseEstimator, TransformerMixin):
    def __init__(self, ratio):
        self.ratio = ratio

    def fit(self, image):
        pass

    def transform(self, image):
        new_size = [int(s * self.ratio) for s in image.shape[:2]]
        interpolation = cv2.INTER_AREA if self.ratio <= 1 else cv2.INTER_CUBIC
        return cv2.resize(image, new_size[::-1], interpolation=interpolation)


class HorizontalMirrorImage:
    def __init__(self):
        pass

    def __call__(self, image):
        return image[:, ::-1]


class ScaleVertically:
    def __init__(self, desired_height):
        self.desired_height = desired_height

    def __call__(self, image):
        pad_size = max(0, self.desired_height - image.shape[0])
        pad_size_top = pad_size//2 if pad_size % 2==0 else (pad_size - 1 )//2
        pad_size_bottom = pad_size//2 if pad_size % 2==0 else (pad_size + 1 )//2
        return np.pad(
            image,
            [(pad_size_top, pad_size_bottom), (0, 0)],
            constant_values=1.
        )


class ScaleHorizontally:
    def __init__(self, desired_width):
        self.desired_width = desired_width

    def __call__(self, image):
        return np.pad(
            image,
            [(0, 0), (0, max(0, self.desired_width - image.shape[1]))],
            constant_values=1.
        )


class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, padding=0, kernel_size=(3, 3), activation=nn.LeakyReLU, stride=1):
        super(CNNBlock, self).__init__()

        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, padding=padding, stride=stride),
            activation(),
            nn.InstanceNorm2d(out_channels)
        )

    def forward(self, x):
        return self.block(x)
