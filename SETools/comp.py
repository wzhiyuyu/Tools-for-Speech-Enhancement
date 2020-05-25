#!/usr/bin/env python
# coding=utf-8

import argparse
import json
import time
from pathlib import Path
import librosa
import tablib
from tqdm import tqdm
import os

from .metrics import compute_STOI, compute_PESQ
from .utils import find_aligned_wav_files


def comp(
        noisy_dir="./noisy", 
        clean_dir="./clean", 
        denoisy_dir="./denoisy", 
        sr=16000, 
        limit=0, 
        offset=0, 
        output_path="./output.xls"):
    print("diaoyongle cal()")
    noisy_dir = Path(noisy_dir)
    clean_dir = Path(clean_dir)
    denoisy_dir = Path(denoisy_dir)

    noisy_wavs_paths, clean_wavs_paths, shorter_length = find_aligned_wav_files(
        noisy_dir.as_posix(), clean_dir.as_posix(), limit=limit, offset=offset
    )

    denoisy_wavs_paths, _, shorter_length = find_aligned_wav_files(
        denoisy_dir.as_posix(), clean_dir.as_posix(), limit=limit, offset=offset
    )

    noisy_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(noisy_wavs_paths, desc="Loading noisy wavs..")]
    clean_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(clean_wavs_paths, desc="Loading clean wavs..")]
    denoisy_wavs = [librosa.load(path, sr=sr)[0] for path in tqdm(denoisy_wavs_paths, desc="Loading denoisy wavs..")]

    assert (len(noisy_wavs) == len(clean_wavs) == len(denoisy_wavs)), f"{noisy_dir} 与 {clean_dir} 中的文件数量不一致"

    headers = (
        "语音编号",
        "噪声类型",
        "信噪比",
        "STOI 纯净与带噪",
        "STOI 纯净与降噪 ",
        "PESQ 纯净与带噪",
        "PESQ 纯净与降噪",
        "STOI 提升",
        "PESQ 提升",
    )  # 定义导出为 Excel 文件的格式
    metrics_seq = []

    for i, (noisy_wav, clean_wav, denoisy_wav) in tqdm(
            enumerate(zip(noisy_wavs, clean_wavs, denoisy_wavs)), desc="正在计算评价指标："
    ):
        lengths = [len(noisy_wav), len(clean_wav), len(denoisy_wav)]
        lengths.sort()
        shorter_length = lengths[0]
        stoi_c_n = compute_STOI(clean_wav[:shorter_length], noisy_wav[:shorter_length])
        stoi_c_d = compute_STOI(clean_wav[:shorter_length], denoisy_wav[:shorter_length])
        pesq_c_n = compute_PESQ(clean_wav[:shorter_length], noisy_wav[:shorter_length])
        pesq_c_d = compute_PESQ(clean_wav[:shorter_length], denoisy_wav[:shorter_length])

        num, noise, snr = os.path.splitext(os.path.basename(noisy_wavs_paths[i]))[
            0
        ].split("_")

        metrics_seq.append(
            (
                num,
                noise,
                snr,
                stoi_c_n,
                stoi_c_d,
                pesq_c_n,
                pesq_c_d,
                (stoi_c_d - stoi_c_n) / stoi_c_n,
                (pesq_c_d - pesq_c_n) / pesq_c_n,
            )
        )

    data = tablib.Dataset(*metrics_seq, headers=headers)
    print(f"测试过程结束，结果将存储至 {output_path}.")
    with open(output_path, "wb") as f:
        f.write(data.export("xls"))