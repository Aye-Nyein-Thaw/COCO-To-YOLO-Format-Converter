import argparse
from coco2yolo import generate_yolo_labels


classes = ["person","bicycle","car","motorcycle","airplane","bus","train",
   "truck","boat","traffic light","fire hydrant","stop sign","parking meter",
   "bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra",
   "giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis",
   "snowboard","sports ball","kite","baseball bat","baseball glove","skateboard",
   "surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon",
   "bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza",
   "donut","cake","chair","couch","potted plant","bed","dining table","toilet","tv",
   "laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink",
   "refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]

    
def init_parser():
    parser = argparse.ArgumentParser(description='Converts COCO format to YOLO format')
    parser.add_argument('--coco-json', type=str, default='annotation.json', help='coco json file path')
    parser.add_argument('--output-folder', type=str, default='yolo_labels', help='output folder for label text files')
    parser.add_argument('--include-background', default=False, action='store_true', help='generate label text files for background images without annotations')

    return parser


if __name__ == "__main__":
    
    parser = init_parser()
    args = parser.parse_args()

    include_background = args.include_background
    coco_json_path = args.coco_json
    output_folder = args.output_folder

    generate_yolo_labels(coco_json_path, classes, output_folder, include_background)
