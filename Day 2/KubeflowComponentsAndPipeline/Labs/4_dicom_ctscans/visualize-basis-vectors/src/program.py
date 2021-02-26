from ast import literal_eval

from os import listdir

import matplotlib.pyplot as plt
import numpy as np

import argparse

parser = argparse.ArgumentParser(
    description='Convert DRMs into DICOMs and Images')
parser.add_argument('--directory',
                    type=str,
                    help='name of directory to write output to.')
args = parser.parse_args()


def read_mahout_drm(path):
    data = {}
    counter = 0
    parts = [p for p in listdir(path) if "part"]
    for p in parts:
        with open(f"{path}/{p}", 'r') as f:
            lines = f.read().split("\n")
            for l in lines[:-1]:
                counter += 1
                t = literal_eval(l)
                arr = np.array([t[1][i] for i in range(len(t[1].keys()))])
                data[t[0]] = arr
    print(f"read {counter} lines from {path}")
    return data


def plot_3d_matrix(img3d, img_shape, ax_aspect, sag_aspect, cor_aspect):
    # plot 3 orthogonal slices
    a1 = plt.subplot(2, 2, 1)
    plt.imshow(img3d[:, :, img_shape[2] // 2])
    a1.set_aspect(ax_aspect)

    a2 = plt.subplot(2, 2, 2)
    plt.imshow(img3d[:, img_shape[1] // 2, :])
    a2.set_aspect(sag_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(img3d[img_shape[0] // 2, :, :].T)
    a3.set_aspect(cor_aspect)
    plt.show(cmap=plt.cm.bone)


def plot_2_3d_matrices(img1, img2, aspect, slice, cmap):
    a1 = plt.subplot(1, 2, 1)
    plt.imshow(img1[:, slice, :], cmap=cmap)
    a1.set_aspect(aspect)

    a2 = plt.subplot(1, 2, 2)
    plt.imshow(img2[:, slice, :], cmap=cmap)
    a2.set_aspect(aspect)



import os



drmU = read_mahout_drm("/mnt/data/drmU")
drmV = read_mahout_drm("/mnt/data/drmV")

print(os.listdir("/mnt/data"))
print(os.listdir("/mnt/data/s"))

drmU_p5 = np.transpose(np.array([drmU[i] for i in range(len(drmU.keys()))]))
drmV_p5 = np.array([drmV[i] for i in range(len(drmV.keys()))])

with open(f"/mnt/data/s/s_part-00000", 'r') as f:
    diags = [float(d) for d in f.read().split('\n') if d != '']

recon = drmU_p5 @ np.diag(diags) @ drmV_p5.transpose()
# plot_3d_matrix(recon.transpose().reshape((512,512,301)), (512,512,301), 1.0, 0.810547, 1.2337347494963278)
composite_img = recon.transpose().reshape((512, 512, 301))

diags_orig = diags
percs = [0.001, 0.01, 0.05, 0.1, 0.3]

for p in range(len(percs)):
    perc = percs[p]
    diags = [
        diags_orig[i] if i < round(len(diags) - (len(diags) * perc)) else 0
        for i in range(len(diags))
    ]
    recon = drmU_p5 @ np.diag(diags) @ drmV_p5.transpose()
    # plot_3d_matrix(recon.transpose().reshape((512,512,301)), (512,512,301), 1.0, 0.810547, 1.2337347494963278)
    composite_img = recon.transpose().reshape((512, 512, 301))
    a1 = plt.subplot(1, 1, 1)
    plt.imshow(composite_img[:, :, 150], cmap=plt.cm.bone)
    plt.title(
        f"{perc*100}% denoised.  (k={len(diags)}, oversample=15, power_iters=2)"
    )
    a1.set_aspect(1.0)
    plt.axis('off')
    fname = f"{100-(perc*100)}%-denoised-img.png"
    plt.savefig(f"/mnt/data/{fname}")
