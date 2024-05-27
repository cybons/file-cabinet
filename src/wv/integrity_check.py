"""
データの整合性チェックを行うモジュール。
"""

import constants as constants
import pandas as pd


def check_results_integrity(file_path: str, sheet_name: str = "未確定") -> pd.DataFrame:  # noqa: E501
    """
    ファイルの未確定シートを読み込み、データの整合性をチェックする関数。

    Args:
        file_path (str): Excelファイルのパス。
        sheet_name (str): シート名。

    Returns:
        pd.DataFrame: チェック済みのデータフレーム。

    Raises:
        ValueError: 確認列が不正な場合や重複がある場合。
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 確認列が含まれているかチェック
    if "確認" not in df.columns:
        raise ValueError("確認列が見つかりません。ファイルが正しいか確認してください。")

    # 確認列が "⚪︎" または "-" のみ含んでいるかチェック
    if not df["確認"].isin(["⚪︎", "-"]).all():
        raise ValueError("確認列に不正な値が含まれています。")

    # 確認列が "⚪︎" の前月組織が一意かチェック
    duplicate_prev_orgs = df[df["確認"] == "⚪︎"][constants.PREV_ORG].duplicated().any()  # noqa: E501
    if duplicate_prev_orgs:
        raise ValueError("確認列において前月組織が重複しています。")

    # 確認列が "⚪︎" の当月組織が一意かチェック
    duplicate_curr_orgs = df[df["確認"] == "⚪︎"][constants.CURR_ORG].duplicated().any()  # noqa: E501
    if duplicate_curr_orgs:
        raise ValueError("確認列において当月組織が重複しています。")

    return df
