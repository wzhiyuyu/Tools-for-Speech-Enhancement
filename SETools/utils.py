import os

import librosa
import numpy as np


def find_aligned_wav_files(wav_files_dir_A, wav_files_dir_B, limit=0, offset=0):
    """
    搜索目录中的 wav 文件，并要求两个目录中的 wav *文件数量相等*且*文件名一一对应*
    Args:
        wav_files_dir_A:
        wav_files_dir_B:
        limit: 加载文件的数量限制

    Returns:
        length:
            1. limit == None时，length = 实际数量
            2. limit <= len(wav_file_paths_A) 时，length = limit
            2. limit > len(wav_file_paths_A) 时，length = 实际数量
    """
    if limit == 0:
        limit = None  # 当 limit == None 时，librosa 默认加载全部文件
    wav_file_paths_A = librosa.util.find_files(wav_files_dir_A, ext="wav", limit=limit, offset=offset)
    wav_file_paths_B = librosa.util.find_files(wav_files_dir_B, ext="wav", limit=limit, offset=offset)

    # 两个目录数量相等，且文件数量 > 0
    assert len(wav_file_paths_A) == len(wav_file_paths_B) > 0, \
        "目录 {} 和目录 {} 文件数量不同或目录为空".format(wav_files_dir_A, wav_files_dir_B)

    # limit 未指定时，返回实际数量；limit >= 实际数量时，返回实际数量；否则返回 limit
    length = len(wav_file_paths_A)

    # 两个目录中的 wav 文件应当文件名一一对应
    for wav_file_path_A, wav_file_path_B in zip(wav_file_paths_A, wav_file_paths_B):
        assert os.path.basename(wav_file_path_A) == os.path.basename(wav_file_path_B), \
            "文件 {} 与 文件 {} 不对称，这可能由于两个目录文件数量不同".format(wav_file_path_A, wav_file_path_B)

    return wav_file_paths_A, wav_file_paths_B, length

