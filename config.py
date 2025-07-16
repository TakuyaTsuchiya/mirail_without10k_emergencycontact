# mirail_without10k_emergencycontact/config.py

class Config:
    """
    ミライル・オートコール（緊急連絡人・残債除外）の設定値を管理するクラス。
    """
    # 入力ファイル関連
    INPUT_FILE_PATTERN = "ContractList_*.csv"

    # テンプレートファイル関連
    TEMPLATE_FILE_NAME = "template.csv"

    # 出力ファイル関連
    INTERMEDIATE_OUTPUT_FILE_NAME = "filtered_mirail_without10k_emergencycontact.csv"
    FINAL_OUTPUT_FILE_PREFIX = "ミライル_without10k_連絡人"
    OUTPUT_ENCODING = "cp932"

    # フィルタリング条件
    FILTER_CONDITIONS = {
        "委託先法人ID": "空白のみ",                    # 委託先なし案件のみ
        "入金予定日": "前日以前またはNaN",              # 当日は除外
        "回収ランク_not_in": ["弁護士介入"],          # 弁護士介入のみ除外
        "クライアントコード": "1",                   # クライアントコード1に絞り込み
        "残債_not_in": [10000, 11000],              # 10,000円・11,000円除外
        "緊急連絡人１のTEL（携帯）": "空でない値のみ"  # 緊急連絡人電話番号が必須
    }

    # マッピングルール（テンプレート列名: 入力データ列名）
    MAPPING_RULES = {
        "電話番号": "緊急連絡人１のTEL（携帯）",
        "架電番号": "緊急連絡人１のTEL（携帯）", 
        "入居ステータス": "入居ステータス",
        "滞納ステータス": "滞納ステータス",
        "管理番号": "管理番号",
        "契約者名（カナ）": "契約者カナ",
        "物件名": "物件名",
        "クライアント": "クライアント名"
    }

# 設定値にアクセスする例:
# from config import Config
# print(Config.INPUT_FILE_PATTERN)
# print(Config.FILTER_CONDITIONS["クライアントコード"])