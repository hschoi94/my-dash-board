import numpy as np
import os
import shutil
import tifffile
from PIL import Image


def mkdir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)
    return path


def sample_random(i_list, i_num):
    sampled_list = np.random.choice(
        range(0, len(i_list)), i_num, replace=False)
    r_list = []
    for i in sampled_list:
        r_list.append(i_list[i])
    return r_list


def imread(img_path):
    ext = os.path.splitext(img_path)[1]
    if ext in [".png", ".jpg"]:
        img = Image.open(img_path)
        img = np.asarray(img)
    elif ext in [".tiff", ".tif"]:
        img = tifffile.imread(img_path)
    return img


def imwrite(img_path, img):
    ext = os.path.splitext(img_path)[1]
    if ext in [".png", ".jpg"]:
        img = np.array(img, dtype=np.uint8)
        img = Image.fromarray(img)
        img.save(img_path)
    elif ext in [".tiff", ".tif"]:
        tifffile.imwrite(img_path, img)


def get_file_list(dir_path, file_list=None, ext_list=None):
    tmp = []
    if file_list is None:
        file_list = os.listdir(dir_path)
    for i in range(len(file_list)):
        source_path = file_list[i]
        if ext_list is not None and (os.path.splitext(source_path)[1] in ext_list):
            tmp.append(source_path)
        elif ext_list is None:
            tmp.append(source_path)

    return tmp


def renew(path):
    if os.path.exists(path) is True:
        shutil.rmtree(path)
    os.mkdir(path)
    return path


def path_exists(path):
    if os.path.exists(path) is False:
        print(path+" is not exists")
        raise ValueError
    else:
        return path


def get_same_files2dst(path_inp, path_get, path_dst, file_list=None, ext_list=None):
    path_inp = path_exists(path_inp)
    path_get = path_exists(path_get)
    path_dst = mkdir(path_dst)

    file_list = []
    file_list = get_file_list(path_inp, file_list, ext_list)

    for file in file_list:
        file_basename = os.path.basename(file)
        get_file_path = path_exists(os.path.join(path_get, file_basename))
        shutil.copy(get_file_path, os.path.join(path_dst, file_basename))


def get_random_list_split(list_, get_num):
    import numpy as np
    sampled_list = sorted(np.random.choice(
        range(0, len(list_)), get_num, replace=False))

    tmp = []
    els = []
    for i in range(len(list_)):
        if i in sampled_list:
            tmp.append(list_[i])
        else:
            els.append(list_[i])
    return tmp, els


def get_random_files(path_inp, file_num, ext_list=None):
    path_inp = path_exists(path_inp)
    file_list = get_file_list(path_inp, ext_list=ext_list)
    tmp = get_random_list_split(file_list, file_num)[0]
    return tmp


def genTargetPathData(source_path, target_dir, function=lambda x: x):
    source_img = tifffile.imread(source_path)
    target_img = function(source_img)
    bs_name, ext = os.path.splitext(os.path.basename(source_path))
    if type(target_img) is list:
        for i in range(len(target_img)):
            tifffile.imwrite(os.path.join(
                target_dir, bs_name+"-"+str(i)+ext), target_img[i])
    else:
        tifffile.imwrite(os.path.join(target_dir, bs_name+ext), target_img)


def splitImg(img, block_size=512):
    h, w, c = img.shape
    h_num = int(h/block_size)
    w_num = int(w/block_size)
    tmp = []
    for hh in range(h_num):
        for ww in range(w_num):
            blk = img[block_size*hh:block_size *
                      int(hh+1), block_size*ww:block_size*(ww+1), :]
            tmp.append(blk)
    return tmp


def diff_dirpath(root_path, now_path):
    tmp_path = now_path
    name_list = []
    while (root_path != tmp_path):
        name_list.append(os.path.basename(tmp_path))
        tmp_path = os.path.dirname(tmp_path)
    return name_list


def get_dirlist(dir_path, reculsive=False):
    if isinstance(dir_path, list):
        tmp = []
        for dir_ in dir_path:
            tmp.extend(get_dirlist(dir_))
        return tmp
    else:
        sub_dirlist = os.listidr(dir_path)
        dir_list = []
        for sub_dir in sub_dirlist:
            sub_path = os.path.join(dir_path, sub_dir)
            if os.path.isdir(sub_path):
                if reculsive:
                    dir_list.extend(get_dirlist(sub_path, reculsive))
                dir_list.append(sub_path)
        return dir_list


def same_filename_sampler(root_path, res_path, file_name, naming_rule):
    dir_list = get_dirlist(root_path, True)
    for dir_ in dir_list:
        file_path = os.path.join(dir_, file_name)
        if os.path.exists(file_path):
            res_name = naming_rule(root_path, dir_, file_name)
            res_path = os.path.join(res_path, res_name)
            shutil.copy(file_path, res_path)
