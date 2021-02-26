from os import listdir
import numpy as np
import pydicom

import argparse
from google.cloud import storage

parser = argparse.ArgumentParser(description='Process DICOM Images into Vectors.')

parser.add_argument('--input_dir',
                    type=str,
                    default="/mnt/data/dicom",
                    help='Directory containing DICOM Images')


parser.add_argument('--output_dir',
                    type=str,
                    default="/mnt/data/",
                    help='Directory to write output to.')

parser.add_argument('--output_file',
                    type=str,
                    default="converted_dicom.csv",
                    help='file name of dcm converted to 2d numerical matrix')

args = parser.parse_args()


def create_3d_matrix(path):
    dicoms = [pydicom.dcmread(f"{path}/{f}") for f in listdir(path)]
    slices = [d for d in dicoms if hasattr(d, "SliceLocation")]
    slices = sorted(slices, key=lambda s: s.SliceLocation)
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    ax_aspect = ps[1] / ps[0]
    sag_aspect = ps[1] / ss
    cor_aspect = ss / ps[0]

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d

    return {
        "img3d": img3d,
        "img_shape": img_shape,
        "ax_aspect": ax_aspect,
        "sag_aspect": sag_aspect,
        "cor_aspect": cor_aspect
    }


input_dir = args.input_dir
output_file = args.output_file

m = create_3d_matrix(f"{input_dir}")
np.savetxt('/mnt/data/converted_dicom.csv', m['img3d'].reshape((-1, m['img_shape'][2])), delimiter=",")
# upload_blob(args.bucket_name, "/tmp/s.csv", output_file)
