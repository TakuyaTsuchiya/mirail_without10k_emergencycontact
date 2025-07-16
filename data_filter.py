# mirail_without10k_emergencycontact/data_filter.py

import pandas as pd
from datetime import datetime
from config import Config

def apply_filters(df_input: pd.DataFrame) -> pd.DataFrame:
    """
    入力DataFrameにミライル・オートコール用のフィルタリング条件を適用する。
    フィルタリング条件はconfig.pyから読み込む。
    """
    df = df_input.copy() # 元のDataFrameを変更しないようにコピー

    # configからフィルタリング条件を取得
    filter_conditions = Config.FILTER_CONDITIONS

    # 委託先法人IDのフィルタリング（空白のみ）
    if "委託先法人ID" in filter_conditions:
        df = df[df["委託先法人ID"].isna() | (df["委託先法人ID"].astype(str).str.strip() == "")]

    # 入金予定日のフィルタリング
    # 入金予定日がNaNか、前日以前（当日は含めない）
    today = pd.Timestamp.now().normalize()
    df["入金予定日"] = pd.to_datetime(df["入金予定日"], errors='coerce')
    df = df[df["入金予定日"].isna() | (df["入金予定日"] < today)]

    # 回収ランクのフィルタリング（弁護士介入のみ除外）
    if "回収ランク_not_in" in filter_conditions:
        df = df[~df["回収ランク"].isin(filter_conditions["回収ランク_not_in"])]

    # クライアントコードのフィルタリング（1のみ）
    if "クライアントコード" in filter_conditions:
        df["クライアントコード"] = pd.to_numeric(df["クライアントコード"], errors="coerce")
        df = df[df["クライアントコード"] == int(filter_conditions["クライアントコード"])]

    # 残債のフィルタリング（10,000円・11,000円除外）
    if "残債_not_in" in filter_conditions:
        df["残債"] = pd.to_numeric(df["残債"], errors='coerce')
        df = df[~df["残債"].isin(filter_conditions["残債_not_in"])]

    # 緊急連絡人１のTEL（携帯）のフィルタリング（空でない値のみ）
    if "緊急連絡人１のTEL（携帯）" in filter_conditions:
        df = df[
            df["緊急連絡人１のTEL（携帯）"].notna() &
            (~df["緊急連絡人１のTEL（携帯）"].astype(str).str.strip().isin(["", "nan", "NaN"]))
        ]

    print(f"[INFO] フィルタリング完了。残件数: {len(df)}件")
    return df