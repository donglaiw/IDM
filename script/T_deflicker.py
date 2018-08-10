# test video deflicker
import h5py
import torch
import numpy as np
import em_pre.deflicker as dfkr_cpu
import em_pre_cuda.deflicker as dfkr_gpu
import cv2
from T_util import writeh5
import cProfile
import unittest


def test_snemi():
    # load data: 100x1024x1024
    ims_np = np.array(h5py.File('test_data.h5', 'r')['main'], dtype=np.float32)
    ims_torch = torch.from_numpy(ims_np).cuda()
    cpu_profile = cProfile.Profile()
    gpu_profile = cProfile.Profile()


    # online version
    def getN_np(i):
        return ims_np[i]
    def getN_cuda(i):
        return ims_torch[i]

    cpu_profile.enable()
    out_cpu = dfkr_cpu.deflicker_online(getN_np, opts=[0, 0, 0], globalStat=[150, -1], filterS_hsz=[15,15], filterT_hsz=2)
    cpu_profile.disable()
    gpu_profile.enable()
    out_gpu = dfkr_gpu.deflicker_online(getN_cuda, opts=(0, 0, 0), global_stat=(150, -1), s_flt_rad=15, t_flt_rad=2)
    gpu_profile.disable()
    for i in range(100):
        cv2.imwrite("output_cpu%d.png" % i, out_cpu[:, :, i])
        cv2.imwrite("output_gpu%d.png" % i, out_gpu[:, :, i])
    #writeh5('snemi_df150_online_cpu.h5', 'main', out_cpu)
    #writeh5('snemi_df150_online_gpu.h5', 'main', out_gpu)
    cpu_profile.print_stats()
    gpu_profile.print_stats()
    cpu_profile.dump_stats("cpu.profile")
    gpu_profile.dump_stats("gpu.profile")


if __name__ == "__main__":
    test_snemi()
