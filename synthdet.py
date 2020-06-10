from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone

class Net(FasterRCNN):
    def __init__(self, num_classes=64, **kwargs):
        backbone = resnet_fpn_backbone('resnet50', False)
        super(Net, self).__init__(backbone, num_classes, **kwargs)
