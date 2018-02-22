import numpy as np
cimport numpy as np

def idm(np.ndarray[np.float32_t, ndim=3] img1, 
             np.ndarray[np.float32_t, ndim=3] img2, 
             patch_sz=11, warp_sz=5):
    # size: c*y*x (C-order, change last dim first)
    img1 = np.ascontiguousarray(img1)
    img2 = np.ascontiguousarray(img2) 
    dim = img1.shape
    cdef np.ndarray[np.float32_t, ndim=2] dist = np.zeros((dim[1], dim[2]), dtype=np.float32);
    idm_dist(&img1[0,0,0], &img2[0,0,0], &dist[0,0], 
             dim[0], dim[1], dim[2], patch_sz, warp_sz);
    return dist

def idm_ims(np.ndarray[np.float32_t, ndim=4] imgs, 
             patch_sz=11, warp_sz=5):
    # size: c*y*x (C-order, change last dim first)
    dim = imgs.shape
    out = np.zeros((dim[0]-1,dim[2],dim[3]),dtype=np.float32)
    cdef np.ndarray[np.float32_t, ndim=2] dist = np.zeros((dim[2], dim[3]), dtype=np.float32);
    for im_id in range(dim[0]-1):
        img1 = np.ascontiguousarray(img1)
        img2 = np.ascontiguousarray(img2) 
        idm_dist(&img1[0,0,0], &img2[0,0,0], &dist[0,0], 
                 dim[0], dim[1], dim[2], patch_sz, warp_sz);
        out[im_id] = dist.copy()
    return out

cdef extern from "src/idm_main.h":
    void idm_dist(float *img1, float *img2, float *out, int im_chan,
                 int im_col, int im_row, int patch_sz, int warp_sz);
