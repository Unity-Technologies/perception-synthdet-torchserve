import json
import io
import logging
import numpy as np
import os
import time
import torch
import torchvision
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone

MODEL_PTH_FILE = "synthdet_faster_rcnn.pth"
MODEL_DEF_FILE = "synthdet.py"
NAME_DICTIONARY_FILE = "index_to_name.json"

class SynthDetModelHandler(object):
    """
    SynthDetModelHandler handler class. This handler takes an image
    and returns list of detected classes and bounding boxes respectively.
    This class is based on ObjectDetector, but is slightly different to handle 
    our models. SynthDet FastRCNN models store the state dict under the "model"
    key. 
    """

    def __init__(self):
        self.model = None
        self.mapping = None
        self.device = None
        self.initialized = False
        self.logger = logging.getLogger()

        logging.basicConfig()
        self.logger.setLevel(logging.INFO)

    def initialize(self, ctx):
        self.initialized = False

        properties = ctx.system_properties

        self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")

        model_dir = properties.get("model_dir")
        model_pth_path = os.path.join(model_dir, MODEL_PTH_FILE)
        model_def_path = os.path.join(model_dir, MODEL_DEF_FILE)
        if not os.path.isfile(model_def_path) or not os.path.isfile(model_pth_path):
            raise RuntimeError("Missing the model definition file and/or model pth file")

        from synthdet import Net
        self.model = Net()
        model_save = torch.load(model_pth_path, map_location=self.device)
        self.model.load_state_dict(model_save["model"])
        self.model.to(self.device)
        self.model.eval()

        mapping_file_path = os.path.join(model_dir, NAME_DICTIONARY_FILE)
        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)
        else:
            self.logger.warning("Missing the index_to_name.json file. Inference output will not include class name.")

        self.initialized = True

    def preprocess(self, data):
        """
        Do any scaling/cropping here
        """
        image = data[0].get("data")
        if image is None:
            image = data[0].get("body")

        image_to_tensor = transforms.Compose([transforms.ToTensor()])
        image = Image.open(io.BytesIO(image))
        image = image_to_tensor(image)
        return image

    def inference(self, img, threshold=0.5):
        """
        Runs model on `img` and produces an array of three arrays: 
        prediction classes, bounding boxes, and prediction scores
        """

        # Start timing
        time_inference_start = time.time()

        # Predict the classes and bounding boxes in an image using a trained deep learning model
        img = Variable(img).to(self.device)
        pred = self.model([img]) # Pass the image to the model

        pred_classes = list(pred[0]["labels"].cpu().numpy())
        pred_boxes = [{
            "top_left": {
                "x": float(i[0]),
                "y": float(i[1])
            },
            "bottom_right": {
                "x": float(i[2]),
                "y": float(i[3])
            }
        } for i in list(pred[0]["boxes"].cpu().detach().numpy())]
        pred_scores = list(pred[0]["scores"].cpu().detach().numpy())

        # Index of last score that is greater than threshold
        valid_indexes = [pred_scores.index(x) for x in pred_scores if x > threshold]

        # Stop timing
        time_inference_stop = time.time()
        self.logger.info(f"Took {round((time_inference_stop - time_inference_start) * 1000)}ms on inference")

        if len(valid_indexes) > 0:
            pred_threshold_index = valid_indexes[-1]

            pred_boxes = pred_boxes[:pred_threshold_index + 1]
            pred_classes = pred_classes[:pred_threshold_index + 1]
            pred_scores = pred_scores[:pred_threshold_index + 1]

            return [pred_classes, pred_boxes, pred_scores]
        else:
            return [[], [], []]

    def postprocess(self, inference_output):
        """
        `inference_output`: Array of three arrays: prediction classes,
        bounding boxes, and prediction scores. This function zips these arrays
        and produces a JSON object representing each box, and assigns label names
        if index_to_name.json is present
        """
        try:
            if self.mapping:
                labels = self.mapping["object_type_names"]
            else:
                labels = None

            return [[{
                "label": str(labels[class_index] if labels else class_index), # Cast to str in case output is an int64 to prevent JSON key TypeError
                "label_id": int(class_index), 
                "box": bounding_box,
                "score": float(score)
            } for class_index, bounding_box, score in zip(*inference_output)]]
        except:
            raise Exception('Object name list file should be json format - {"object_type_names":["person","car"...]}"')


_service = SynthDetModelHandler()

def handle(data, context):
    if not _service.initialized:
        _service.initialize(context)

    if data is None:
        return None

    data = _service.preprocess(data)
    data = _service.inference(data)
    data = _service.postprocess(data)

    return data
