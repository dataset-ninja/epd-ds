import glob
import os
import shutil
import xml.etree.ElementTree as ET

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    dataset_path = "/home/alex/DATASETS/TODO/EPD/EPD Dataset"
    split_path = "/home/alex/DATASETS/TODO/EPD/EPD Dataset/EPD-S Dataset/ImageSets/Main"
    batch_size = 30
    images_ext = ".jpg"
    anns_ext = ".xml"
    ann_ext = "_labels.csv"

    def create_ann(image_path):
        labels = []

        ann_path = image_path.replace("JPEGImages", "Annotations").replace(images_ext, anns_ext)

        tree = ET.parse(ann_path)
        root = tree.getroot()

        img_height = 1024  # int(root.find(".//height").text)
        img_wight = 1024  # int(root.find(".//width").text)

        if image_path.split("/")[-3][4] == "S":
            drone = sly.Tag(epd_s)
        else:
            drone = sly.Tag(epd_c)

        coords_xml = root.findall(".//bndbox")
        for curr_coord in coords_xml:
            left = int(curr_coord[0].text)
            top = int(curr_coord[1].text)
            right = int(curr_coord[2].text)
            bottom = int(curr_coord[3].text)
            rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
            label = sly.Label(rect, obj_class)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[drone])

    obj_class = sly.ObjClass("pylon", sly.Rectangle, color=(255, 0, 0))
    epd_c = sly.TagMeta("epd c", sly.TagValueType.NONE)
    epd_s = sly.TagMeta("epd s", sly.TagValueType.NONE)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=[epd_c, epd_s])
    api.project.update_meta(project.id, meta.to_json())

    images_pathes = glob.glob(dataset_path + "/*/JPEGImages/*.jpg")
    image_name_to_path = {}
    for im_path in images_pathes:
        image_name_to_path[get_file_name(im_path)] = im_path

    for ds_name in os.listdir(split_path):

        if ds_name == "trainval.txt":
            continue

        dataset = api.dataset.create(
            project.id, get_file_name(ds_name), change_name_if_conflict=True
        )

        curr_split_path = os.path.join(split_path, ds_name)
        with open(curr_split_path) as f:
            content = f.read().split("\n")
            images_names = [im_name for im_name in content if len(im_name) > 1]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = []
            im_names_batch = []
            for image_name in images_names_batch:
                im_names_batch.append(image_name + images_ext)
                img_pathes_batch.append(image_name_to_path[get_file_name(image_name)])

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
