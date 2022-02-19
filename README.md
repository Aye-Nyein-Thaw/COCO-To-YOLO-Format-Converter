# COCO To YOLO Format Converter
For converting COCO annotation format to YOLO format.


### Requirements
- Requires [pycocotools](https://pypi.org/project/pycocotools/)


### Usage:
	python main.py \
	--coco-json annotation.json \
	--output-folder yolo_labels \
	--include-background
 
 **Note**: Please put your dataset's class names in "classes" variable in `main.py`
 
	 classes = ["person", "car", "airplane"]

 
### Parameters:

| Parameter        | Description |
| :-------------------| :-------------|
| --coco-json 	   | path to coco json annotation file
| --output-folder | folder for yolo label text files
| --include-background	| generate label text files for images without annotations
