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

        img_height = int(root.find(".//height").text)
        img_wight = int(root.find(".//width").text)

        coords_xml = root.findall(".//bndbox")
        for curr_coord in coords_xml:
            left = int(curr_coord[0].text)
            top = int(curr_coord[1].text)
            right = int(curr_coord[2].text)
            bottom = int(curr_coord[3].text)
            rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
            label = sly.Label(rect, obj_class)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    obj_class = sly.ObjClass("pylon", sly.Rectangle, color=(255, 0, 0))

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class])
    api.project.update_meta(project.id, meta.to_json())

    for ds_name in os.listdir(dataset_path):

        dataset = api.dataset.create(
            project.id, get_file_name(ds_name.split(" ")[0]), change_name_if_conflict=True
        )

        curr_dataset_path = os.path.join(dataset_path, ds_name)

        images_pathes = glob.glob(curr_dataset_path + "/JPEGImages/*.jpg")

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))

    return project
