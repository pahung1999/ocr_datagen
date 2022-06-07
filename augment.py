from imageio import imread
from argparse import ArgumentParser
from os import listdir, makedirs
from os.path import join as joinpath, basename
from typing import *
from imgaug import augmenters as iaa
from functools import cache
import numpy as np
import cv2


@cache
def get_augmentations():
    augs = dict(
        rotate=iaa.Affine(rotate=(-10, 10), cval=255),
        shear=iaa.Affine(shear=(-5, 5), cval=255),
        blur=iaa.GaussianBlur(sigma=(0.5, 2.5)),
        cutout=iaa.Cutout(),
        # alpha=iaa.BlendAlpha(factor=(0.5, 0.99), foreground=(0, 0, 0)),
        fade=iaa.GammaContrast((.3, 0.7)),
        darken=iaa.GammaContrast((3, 5))
    )
    augs['darken_rotate'] = iaa.Sequential([augs['rotate'], augs['darken']])
    augs['fade_rotate'] = iaa.Sequential([augs['rotate'], augs['fade']])
    augs['blur_rotate'] = iaa.Sequential([augs['rotate'], augs['blur']])
    augs['cutout_rotate'] = iaa.Sequential([augs['rotate'], augs['cutout']])
    # augs['alpha_rotate'] = iaa.Sequential([augs['rotate'], augs['alpha']])
    return augs


def augment(image: np.ndarray):
    augs = get_augmentations()
    return {key: aug(image=image) for (key, aug) in augs.items()}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_dir", required=True)
    parser.add_argument("-o", "--output", dest="output_dir", required=True)
    parser.add_argument("-l", "--label-file", dest="labelfile", required=True)
    parser.add_argument("--out-label-file", dest="out_labelfile")

    args = parser.parse_args()
    if args.out_labelfile is None:
        args.out_labelfile = args.labelfile.replace('.txt', '.augmented.txt')

    return args


def load_labelfile(file):
    with open(file) as f:
        lines = f.readlines()
        lines = [line for line in lines if line.strip() != ""]
        lines = [line.split("\t") for line in lines]
        return {k: v.strip() for (k, v) in lines}


def dump_labelfile(labels: dict) -> str:
    labels_str = [f"{key}\t{value}" for (key, value) in labels.items()]
    return "\n".join(labels_str)


def get_paths(path: str) -> List[str]:
    files = listdir(path)
    return [joinpath(path, file) for file in files]


def main():
    args = parse_args()
    input_files = get_paths(args.input_dir)
    makedirs(args.output_dir, exist_ok=True)
    labels = load_labelfile(args.labelfile)
    for input_file in input_files:
        image = imread(input_file)
        print(f"processing {input_file}")
        augmented = augment(image)
        for (k, image) in augmented.items():
            input_name = basename(input_file)
            input_name = f"{k}_{input_name}"
            output_file = joinpath(args.output_dir, input_name)
            cv2.imwrite(output_file, image)
            labels[output_file] = labels[input_file]
    with open(args.out_labelfile, 'w') as f:
        f.write(dump_labelfile(labels))


if __name__ == "__main__":
    main()
