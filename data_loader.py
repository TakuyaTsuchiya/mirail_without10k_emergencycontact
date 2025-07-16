# mirail_without10k_emergencycontact/data_loader.py

import pandas as pd
import os
import glob
from config import Config

def read_csv_auto_encoding(file_path):
    """文字コードを自動判別してCSVを読み込む"""
    encodings = ['utf-8', 'utf-8-sig', 'shift_jis', 'cp932']
    for enc in encodings:
        try:
            print(f"[INFO] 読み込み中: encoding='{enc}'")
            return pd.read_csv(file_path, encoding=enc, dtype=str)
        except Exception:
            continue
    raise ValueError(f"{file_path} を読み込めませんでした。")

def get_latest_contract_file():
    """ダウンロードフォルダから最新のContractList_*.csvを取得"""
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    # config.pyからパターンを読み込む
    file_pattern = Config.INPUT_FILE_PATTERN
    files = glob.glob(os.path.join(downloads, file_pattern))
    if not files:
        raise FileNotFoundError(f"{file_pattern} がダウンロードフォルダに見つかりません")
    latest_file = max(files, key=os.path.getctime)
    print(f"[INFO] 最新の入力ファイルを選択: {os.path.basename(latest_file)}")
    return latest_file