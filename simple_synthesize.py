# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
                help="path to the image file")
ap.add_argument("-bg", "--bg_img", required=True,
                help="path to background images")  # 100x100 bgs
ap.add_argument("-t", "--object", required=True,
                help="path to target object images")  # 50x50 objects
args = vars(ap.parse_args())

# load the image from disk
image = cv2.imread(args["image"])


def rotate_crop():
    # loop over the rotation angles
    for angle in np.arange(0, 180, 15):
        rotated = imutils.rotate(image, angle)
        cv2.imshow("Rotated (Problematic)", rotated)
        print("angle: ", angle, "shape: ", rotated.shape[:2])
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass


def rotate_bound():
    # loop over the rotation angles again, this time ensuring
    # no part of the image is cut off
    for angle in np.arange(0, 180, 15):
        rotated = imutils.rotate_bound(image, angle)
        print("angle: ", angle, "shape: ", rotated.shape[:2])
        cv2.imshow("Rotated (Correct)", rotated)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass


def synthesized_imgs():
    output = "./out_images/"
    if not os.path.exists(output):
        os.makedirs(output)
        pass

    bgDir = args["bg_img"]
    objectDir = args["object"]

    # path = os.getcwd() + ""
    print("bgDir: ", bgDir)
    (dir_path, dir_names, filenames) = next(os.walk(os.path.abspath(bgDir)))

    (t_dir_path, t_dir_names, t_filenames) = next(
        os.walk(os.path.abspath(objectDir)))

    for filename in filenames:
        print("bg: ", filename)
        bgfile = os.path.join(dir_path, filename)
        bgImg = cv2.imread(bgfile)

        (h, w) = bgImg.shape[:2]
        # image = np.dstack([bgImg, np.ones((h, w), dtype="uint8") * 255])

        # overlay = np.zeros((h, w, 3), dtype="uint8")

        for t_filename in t_filenames:
            print("target: ", t_filename)
            objfile = os.path.join(t_dir_path, t_filename)
            objImg = cv2.imread(objfile, cv2.IMREAD_UNCHANGED)

            for angle in np.arange(0, 360, 15):
                rotated = imutils.rotate_bound(objImg, angle)
                (wH, wW) = rotated.shape[:2]
                x = 10
                y = 10
                temp = bgImg.copy()
                temp[y: y + wH, x: x + wW] = rotated

                # blend the two images together using transparent overlays
                # finalout = bgImg.copy()
                # cv2.addWeighted(overlay, 0, output, 1.0, 0, output)

                # write the output image to disk
                final_filename = str(angle) + "_" + \
                    filename.split('.')[0] + "_" + t_filename
                p = os.path.join(output, final_filename)
                cv2.imwrite(p, temp)

                #save label info
                bx = (wW/2.0 + x)/w
                by = (wH/2.0 + y)/h
                bw = (wW*1.0)/w
                bh = (wH*1.0)/h
                label_fname = final_filename.split('.')[0] + ".txt"
                with open(os.path.join(os.path.abspath(output), label_fname), 'w') as labelfile:
                	print("0", bx, by, bw, bh, file=labelfile)


    pass


synthesized_imgs()
# rotate_bound()
# rotate_crop()
