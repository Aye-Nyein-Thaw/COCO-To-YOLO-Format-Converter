import os
from pycocotools.coco import COCO


def coco2yolo_bbox(bbox, img_width, img_height):
    """
    Converts coco bbox to YOLO format (xcenter, ycenter, w, h - normalized).
    
    arguments:
        bbox (list): coco bbox format: top left xy, width, height. [x, y, w, h]
        img_width (int): image width
        img_height (int): image height
        
    returns:
        list: bbox in YOLO format [xcenter, ycenter, w, h] (normalized)
    """
    
    x1, y1, w, h = bbox
    
    xcenter = x1 + w/2
    ycenter = y1 + h/2
    
    # Normalize
    xcenter = xcenter / img_width
    ycenter = ycenter / img_height
    w = w / img_width
    h = h / img_height
    
    return [xcenter, ycenter, w, h]


def get_yolo_format_boxes(anns, classes, class_map, img_width, img_height):
    """
    Given a list of coco annotation dicts for a single image, return a list of YOLO format bboxes.
    
    arguments:
        anns(list): a list of annotation dicts. [{}, {}, {}, ...] for a single image
        classes(list): a list of class names (new)
        class_map(dict): a dictionary that maps class id & class names in coco json file
        img_width(int): image width
        img_height(int): image height
        
    returns:
        formatted_bboxes(list): 
    """
    
    formatted_bboxes = []
    
    for ann in anns:

        bbox = ann['bbox']

        # convert bbox format - from coco(xywh) to YOLO (xcenter, ycenter, w, h) normalized
        bbox = coco2yolo_bbox(bbox, img_width, img_height)
        
        # old class id to new class id
        class_name = class_map[ann['category_id']]
        class_id = classes.index(class_name)

        # insert object class id
        bbox.insert(0, class_id)

        # convert int to str values
        bbox = [str(i) for i in bbox]
        
        # join values in list with space
        bbox = ' '.join(bbox)

        formatted_bboxes.append(bbox)
        
    return formatted_bboxes


def generate_yolo_labels(coco_json_dir, classes, output_folder, include_background = True):
    """
    Generate yolo labels from a single coco json file.
    
    arguments:
        coco_json_dir(str): file path of coco json file
        classes(list): a list of class names
        output_folder(str): output folder for generated yolo label text files
        include_background(bool): also generate label txt files(blank) for background images with no annotations
        
    returns:
        None
    """
    
    # create folder for yolo label txt files
    os.makedirs(output_folder, exist_ok = True)
    
    # load coco file
    coco = COCO(coco_json_dir)
    img_ids = coco.getImgIds()
    imgs = coco.loadImgs(img_ids)
    
    # load category list 
    cat_list = coco.loadCats(coco.getCatIds())
    
    # make class id, class name mapping dictionary
    class_map = {i['id']: i['name'] for i in  cat_list}
    
    # save bbox for each image
    for img in imgs:

        file_name = img['file_name'].split('.')[0]

        # load annotations for chosen images
        annids = coco.getAnnIds(imgIds = img['id'])

        # if there's annotations for an image
        if annids:
            # load all ann objects for a single image
            anns = coco.loadAnns(annids)
            formatted_bboxes = get_yolo_format_boxes(anns, classes, class_map, img['width'], img['height'])
            content = '\n'.join(formatted_bboxes)

        # if no associated annotation is found for the image
        elif include_background:
            content = ''
        else:
            continue

        # write txt files for evaluation
        txt_write_dir = os.path.join(output_folder, file_name+'.txt')
        with open(txt_write_dir, 'w') as textfile:
            textfile. write(content)
