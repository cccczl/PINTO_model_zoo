import os
import sys
from glob import glob
from PIL import Image
import numpy as np

def resize(all_file):

  tmp = None
  for f in all_file:
    img = Image.open(f)
    nparray = np.array(img)
    nparray = nparray[np.newaxis, :, :, :]

    tmp = np.vstack((tmp, nparray)) if tmp is not None else nparray.copy()
    print("tmp.shape=", tmp.shape)
    np.save('calibration_data_img_person', tmp)

path = "./images/"
all_file = os.listdir(path)
all_file = [os.path.join(path, f) for f in all_file]
resize(all_file)
print("Finish!!")