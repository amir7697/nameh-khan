from itertools import groupby

import torch
import torch.nn as nn
import torch.nn.functional as F

from config import MODEL_PARAMS, ENCODING_DICT, DECODING_DICT
from misc import CNNBlock, HorizontalMirrorImage, ScaleHorizontally, ScaleVertically


class WordReader(nn.Module):

    def __init__(
            self,
            in_channels=MODEL_PARAMS['in_channels'],
            scale=MODEL_PARAMS['scale'],
            gru_hidden_size=MODEL_PARAMS['gru_hidden_size'],
            gru_num_layers=MODEL_PARAMS['gru_num_layers'],
            num_classes=MODEL_PARAMS['num_classes'],
            bidirectional=MODEL_PARAMS['bidirectional'],
            first_fully_connected_output_size=MODEL_PARAMS['first_fully_connected_output_size'],
            decoding_dict=DECODING_DICT,
            encoding_dict=ENCODING_DICT
    ):

        super(WordReader, self).__init__()

        self.encoding_dict = encoding_dict
        self.decoding_dict = decoding_dict
        self.cnn = nn.Sequential(
            CNNBlock(in_channels=in_channels, out_channels=4 * scale, padding=1, stride=2),
            CNNBlock(in_channels=4 * scale, out_channels=4 * scale, padding=1, stride=2),
            CNNBlock(in_channels=4 * scale, out_channels=8 * scale),
            CNNBlock(in_channels=8 * scale, out_channels=8 * scale),
            CNNBlock(in_channels=8 * scale, out_channels=8 * scale),
            CNNBlock(in_channels=8 * scale, out_channels=8 * scale),
        )
        self.gru_input_size = 8 * scale
        self.gru = nn.GRU(
            self.gru_input_size,
            gru_hidden_size,
            gru_num_layers,
            batch_first=True,
            bidirectional=bidirectional
        )

        first_fully_connected_input_size = 2* gru_hidden_size if bidirectional else gru_hidden_size
        self.first_fully_connected = nn.Linear(first_fully_connected_input_size, first_fully_connected_output_size)
        self.second_fully_connected = nn.Linear(first_fully_connected_output_size, num_classes)

    def forward(self, x):
        batch_size = x.shape[0]

        out = self.cnn(x)

        # Since GRU module needs input data in (batch_size, sequence_length, input_size) size
        out = out.reshape(batch_size, self.gru_input_size, -1)
        out = out.permute(0, 2, 1)

        out, _ = self.gru(out)

        out = torch.stack([
            F.log_softmax(self.second_fully_connected(F.relu(self.first_fully_connected(out[i]))), dim=-1)
            for i in range(batch_size)]
        )
        return out

    def predict(self, mirrored_image):
        with torch.no_grad():
            model_output = self.forward(mirrored_image)

        model_output = model_output.permute(1, 0, 2)
        _, max_index = torch.max(model_output, dim=2)

        raw_prediction = list(max_index[:, 0].detach().cpu().numpy())
        return [label for label, _ in groupby(raw_prediction) if
                label != self.encoding_dict['blank']]

    def transform(self, image):
        mirror_image = HorizontalMirrorImage()
        mirrored_image = mirror_image(image)

        scale_vertically = ScaleVertically(desired_height=MODEL_PARAMS['desired_image_height'])
        scale_horizontally = ScaleHorizontally(desired_width=MODEL_PARAMS['desired_image_width'])

        scaled_image = scale_vertically(mirrored_image)
        scaled_image = scale_horizontally(scaled_image)

        model_input = torch.from_numpy(scaled_image.copy()).unsqueeze(0).unsqueeze(0)

        prediction = self.predict(model_input)
        decoded_prediction = ''.join([
            self.decoding_dict[label] if label in self.decoding_dict else str(label) for label in prediction
        ]).replace(' ', '')

        return decoded_prediction