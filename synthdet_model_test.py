import json
import io
import numpy as np
import sys
import time
import torch
import torchvision
from class_labels import GROCERY_LIST_V0
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone

model = FasterRCNN(resnet_fpn_backbone("resnet50", False), num_classes=64)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model_path = "synthdet_faster_rcnn.pth"
model_save = torch.load(model_path, map_location=device) # no CUDA on macOS   
model.load_state_dict(model_save["model"])
model.to(device)
model.eval()

# preprocess on test image
image_path = sys.argv[1]
image = Image.open(image_path)
image_to_tensor = transforms.Compose([
    transforms.ToTensor()
])
tensor = image_to_tensor(image)

# inference
threshold = 0.5

# Start timing
time_inference_start = time.time()

img = Variable(tensor).to(device)
pred = model([img])  # Pass the image to the model

pred_class = [i for i in list(pred[0]["labels"].cpu().numpy())]  # Get the Prediction Score
pred_boxes = [{
    "top_left": {
        "x": str(i[0]),
        "y": str(i[1])
    },
    "bottom_right": {
        "x": str(i[2]),
        "y": str(i[3])
    }
} for i in list(pred[0]["boxes"].cpu().detach().numpy())]

pred_scores = list(pred[0]["scores"].cpu().detach().numpy())

pred_threshold_index = [pred_scores.index(x) for x in pred_scores if x > threshold][-1]

pred_class = pred_class[:pred_threshold_index + 1]
pred_boxes = pred_boxes[:pred_threshold_index + 1]
pred_scores = pred_scores[:pred_threshold_index + 1]
inference_output = [pred_class, pred_boxes, pred_scores]

# post process
retval = [{
    "label": str(GROCERY_LIST_V0[class_index]), # Cast to str in case output is an int64 to prevent JSON key TypeError
    "box": bounding_box,
    "score": str(score)
} for class_index, bounding_box, score in zip(*inference_output)]

# Stop timing
time_inference_stop = time.time()

print(f"Took {round((time_inference_stop - time_inference_start) * 1000)}ms on inference")

print(json.dumps(retval, indent=2))
