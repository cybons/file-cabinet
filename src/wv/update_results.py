"""
結果を更新するモジュール。
"""

import constants as constants
import pandas as pd


def update_results_with_confirmation(
    df_results: pd.DataFrame, checked_df: pd.DataFrame
) -> pd.DataFrame:
    """
    チェックされたデータフレームに基づいてresultsを更新する関数。

    Args:
        df_results (pd.DataFrame): 結果データフレーム。
        checked_df (pd.DataFrame): チェック済みのデータフレーム。

    Returns:
        pd.DataFrame: 更新された結果データフレーム。
    """
    # 確認列が "⚪︎" の行を取得
    confirmed_rows = checked_df[checked_df["確認"] == "⚪︎"]

    # 既存の確定データを一旦未確定にして同一組織もFalseにする（確認が "⚪︎" になった組織のみ）
    for _, row in confirmed_rows.iterrows():
        prev_org = row[constants.PREV_ORG]
        curr_org = row[constants.CURR_ORG]

        # 該当する組織ペアを未確定にして同一組織をFalseに設定
        df_results.loc[
            (df_results[constants.PREV_ORG] == prev_org)
            | (df_results[constants.CURR_ORG] == curr_org),
            [constants.SAME_ORG, constants.CONFIRMED],
        ] = False

    # confirmed_rowsの同一組織と判定された組織ペアをresultsに反映
    for _, row in confirmed_rows.iterrows():
        prev_org = row[constants.PREV_ORG]
        curr_org = row[constants.CURR_ORG]

        # 該当する組織ペアを確定と同一組織に設定
        df_results.loc[
            (df_results[constants.PREV_ORG] == prev_org)
            & (df_results[constants.CURR_ORG] == curr_org),
            [constants.SAME_ORG, constants.CONFIRMED],
        ] = True

    # 同名組織の確定を再度行う
    for i, row in df_results.iterrows():
        if row[constants.CONFIRMED]:
            prev_org = row[constants.PREV_ORG]
            curr_org = row[constants.CURR_ORG]
            df_results.loc[
                (df_results[constants.PREV_ORG] == prev_org)
                | (df_results[constants.CURR_ORG] == curr_org),
                constants.CONFIRMED,
            ] = True

    return df_results
