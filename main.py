# mirail_without10k_emergencycontact/main.py

import pandas as pd
from data_loader import get_latest_contract_file, read_csv_auto_encoding
from data_filter import apply_filters
from data_mapper import map_data_to_template
from data_writer import write_filtered_csv, write_final_output_csv
from config import Config

def main():
    print("--- ミライル・オートコール（緊急連絡人・残債除外）開始 ---")

    try:
        # 1. 入力ファイルの読み込み
        input_file_path = get_latest_contract_file()
        df_input = read_csv_auto_encoding(input_file_path)
        print(f"[INFO] 入力ファイル読み込み完了: {input_file_path} ({len(df_input)}件)")

        # 2. フィルタ処理
        df_filtered = apply_filters(df_input)
        write_filtered_csv(df_filtered) # 中間出力

        # 3. テンプレートに転記（マッピング）
        df_mapped = map_data_to_template(df_filtered)

        # 4. 最終出力
        write_final_output_csv(df_mapped)

        print("--- ミライル・オートコール（緊急連絡人・残債除外）正常終了 ---")

    except FileNotFoundError as e:
        print(f"[ERROR] ファイルが見つかりません: {e}")
    except ValueError as e:
        print(f"[ERROR] データ処理エラー: {e}")
    except Exception as e:
        print(f"[ERROR] 予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    main()