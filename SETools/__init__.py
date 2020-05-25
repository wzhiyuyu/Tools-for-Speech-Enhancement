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
from .comp import comp

def cal():

    parser = argparse.ArgumentParser(
        description="Speech Enhancement Evaluation Metrics"
    )
    parser.add_argument("--noisy_dir", required=True, type=str, help="带噪语音目录")
    parser.add_argument("--denoisy_dir", required=True, type=str, help="降噪语音的目录")
    parser.add_argument("--clean_dir", required=True, type=str, help="纯净语音的目录")
    parser.add_argument("--output_path", default="./output.xls", type=str, help="评价指标存储的全路径，必须以拓展名 .xls 结尾")
    parser.add_argument("--limit", default=0, type=int, help="被测试语音的数量。默认为0，表示不限制数量")
    parser.add_argument("--offset", default=0, type=int, help="从某个索引位置开始计算评价指标，默认为0，表示从索引为 0 的语音开始计算")
    parser.add_argument("--sr", default=16000, type=int, help="语音文件的采样率")

    args = parser.parse_args()

    comp(
        noisy_dir=args.noisy_dir,
        clean_dir=args.clean_dir,
        denoisy_dir=args.denoisy_dir,
        sr=args.sr,
        limit=args.limit,
        offset=args.offset,
        output_path=args.output_path,
    )
