# mirail_without10k_emergencycontact/data_writer.py

import pandas as pd
from datetime import datetime
from config import Config

def write_filtered_csv(df: pd.DataFrame):
    """
    フィルタリング後の中間CSVを出力する。
    ファイル名とエンコーディングはconfig.pyから読み込む。
    """
    output_path = Config.INTERMEDIATE_OUTPUT_FILE_NAME
    output_encoding = Config.OUTPUT_ENCODING

    try:
        df.to_csv(output_path, index=False, encoding=output_encoding)
        print(f"[INFO] 中間出力完了: {output_path}（{len(df)}件）")
    except Exception as e:
        print(f"[ERROR] 中間CSVの書き込みに失敗しました: {e}")
        raise

def write_final_output_csv(df: pd.DataFrame):
    """
    最終出力CSVを書き込む。
    ファイル名生成ロジックとエンコーディングはconfig.pyから読み込む。
    """
    today_str = datetime.now().strftime("%m%d")
    output_prefix = Config.FINAL_OUTPUT_FILE_PREFIX
    output_file = f"{today_str}{output_prefix}.csv"
    output_encoding = Config.OUTPUT_ENCODING

    try:
        df.to_csv(output_file, index=False, encoding=output_encoding)
        print(f"[INFO] 最終出力完了: {output_file}（{len(df)}件）")
    except Exception as e:
        print(f"[ERROR] 最終CSVの書き込みに失敗しました: {e}")
        raise