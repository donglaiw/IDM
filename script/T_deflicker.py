"""****************************************************************************
* Name: T_deflicker.py
* Author: Matin Raayai Ardakani, Donglai Wei
* A Benchmark/Test run for comparing the performance of the em_pre and 
* em_pre_cuda deflicker function. 
****************************************************************************"""
import cProfile
import h5py
import torch
import numpy as np
import em_pre.deflicker as dfkr_cpu
import em_pre_cuda.deflicker as dfkr_gpu
from T_util import writeh5

IN_DATA_PATH = "/home/matinraayai/Desktop/coxfs01/donglai/ppl/matin/data_h5/cerebellum_ds_orig.h5"
INPUT_DATASET = "main"
OUTPUT_DATASET = "main"
CPU_IM_OUT_PATH = "tmp/T_deflicker_cpu_out.h5"
GPU_IM_OUT_PATH = "tmp/T_deflicker_gpu_out.h5"
GPU_IM_OUT_PATH_2 = "tmp/T_deflicker_gpu_out_2.h5"
CPU_PROF_OUT_PATH = "tmp/cpu.profile"
GPU_PROF_OUT_PATH = "tmp/gpu.profile"


def read_h5_as_np(data_path, dataset_name):
    return h5py.File(data_path, 'r')[dataset_name]


def test_snemi():
    # load data: 100x1024x1024
    ims_np = np.array(read_h5_as_np(IN_DATA_PATH, INPUT_DATASET))
    #ims_torch = torch.from_numpy(ims_np.copy()).cuda()
    cpu_profile = gpu_profile = cProfile.Profile()

    def get_n_np(idx):
        """Getter for em_pre.deflicker."""
        return ims_np[idx + 1300]

    # def get_n_cuda(idx):
    #     """Getter fir em_pre_cuda.deflicker."""
    #     return ims_torch[idx]

    # em_pre.deflicker test:
    cpu_profile.enable()
    out_cpu = dfkr_cpu.deflicker_online(get_n_np, 200, 
                                        opts=[1, 0, 0], 
                                        globalStat=[150, -1], 
                                        filterS_hsz=[25, 25],
                                        filterT_hsz=5)
    cpu_profile.disable()
    # em_pre_cuda.deflicker test:
    # gpu_profile.enable()
    # # out_gpu = dfkr_gpu.deflicker_online(get_n_cuda, slice_range=range(0,100),
    #                                     pre_proc_method='threshold',
    #                                     global_stat=(150, -1), 
    #                                     s_flt_rad=15, 
    #                                     t_flt_rad=2,
    #                                     write_dir="%d.png")
    # gpu_profile.disable();torch.cuda.empty_cache()
    
    #writeh5(CPU_IM_OUT_PATH, OUTPUT_DATASET, out_cpu)

    # def get_n_np_2(idx):
    #     return out_cpu[:, :, idx]
    # out_cpu_2 = dfkr_cpu.deflicker_online(get_n_np_2, 
    #                                     opts=[1, 0, 0], 
    #                                     globalStat=[150, -1], 
    #                                     filterS_hsz=[15, 15],
    #                                     filterT_hsz=6)
    writeh5(GPU_IM_OUT_PATH, OUTPUT_DATASET, out_cpu)
    #writeh5(GPU_IM_OUT_PATH_2, OUTPUT_DATASET, out_cpu_2)
    
    cpu_profile.print_stats(sort=1); 
    cpu_profile.dump_stats(CPU_PROF_OUT_PATH)
    gpu_profile.dump_stats(GPU_PROF_OUT_PATH)


if __name__ == "__main__":
    test_snemi()
