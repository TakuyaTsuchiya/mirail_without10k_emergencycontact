# mirail_without10k_emergencycontact/data_mapper.py

import pandas as pd
from config import Config
from data_loader import read_csv_auto_encoding

def map_data_to_template(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    フィルタリング済みデータとテンプレートを結合し、整形する。
    テンプレートパスとマッピングルールはconfig.pyから読み込む。
    """
    template_path = Config.TEMPLATE_FILE_NAME
    mapping_rules = Config.MAPPING_RULES

    df_template = read_csv_auto_encoding(template_path)

    # テンプレートが空の場合の対処
    if len(df_template) == 0:
        print("[WARNING] テンプレートファイルにデータ行がありません。ヘッダーのみのテンプレートとして処理します。")
        # 入力データの行数分の空行を作成
        empty_data = [{}] * len(df_input)
        df_template = pd.DataFrame(empty_data, columns=df_template.columns)
    
    # テンプレート行数をフィルタ済みに合わせる
    elif len(df_input) > len(df_template):
        print(f"[WARNING] フィルタリング済みデータ ({len(df_input)}行) がテンプレート ({len(df_template)}行) より多いです。テンプレートを拡張します。")
        # テンプレートをdf_inputの行数まで複製して拡張
        last_row = df_template.iloc[-1]
        rows_to_add = len(df_input) - len(df_template)
        for _ in range(rows_to_add):
            df_template = pd.concat([df_template, pd.DataFrame([last_row])], ignore_index=True)
    elif len(df_input) < len(df_template):
        df_template = df_template.iloc[:len(df_input)].copy()
    
    # 必要カラムの転記
    for template_col, input_col in mapping_rules.items():
        if input_col in df_input.columns:
            df_template[template_col] = df_input[input_col].values
        else:
            print(f"[WARNING] 入力データにカラム '{input_col}' が見つかりません。'{template_col}' は空になります。")
            df_template[template_col] = None # または適切なデフォルト値

    # クライアント列の設定（ミライル用）
    # クライアント名をそのまま使用（空白の場合は空白のまま）
    if "クライアント名" in df_input.columns:
        df_template["クライアント"] = df_input["クライアント名"].values
    else:
        print("[WARNING] 入力データにカラム 'クライアント名' が見つかりません。'クライアント' 列は空になります。")
        df_template["クライアント"] = None

    print(f"[INFO] データマッピング完了。出力行数: {len(df_template)}件")
    return df_template