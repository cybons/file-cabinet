"""
メインスクリプト。
"""

import pandas as pd
from integrity_check import check_results_integrity
from prepare_data import prepare_update_data
from simulate_updates import simulate_updates_with_hierarchy
from update_results import update_results_with_confirmation


def main():
    """
    メイン関数。データの準備、整合性チェック、結果の更新、および更新シミュレーションを行う。
    """
    # データの準備
    confirmed_df = pd.read_excel("confirmed_data.xlsx")
    prev_df = pd.read_excel("prev_month_orgs.xlsx")
    curr_df = pd.read_excel("curr_month_orgs.xlsx")

    # データの整合性チェック
    checked_df = check_results_integrity("unchecked_data.xlsx")

    # resultsの更新
    df_results = update_results_with_confirmation(confirmed_df, checked_df)

    # 更新データの準備
    combined_df = prepare_update_data(df_results, prev_df, curr_df)

    # 更新シミュレーション
    update_df = simulate_updates_with_hierarchy(prev_df, curr_df, combined_df)

    # 結果の出力
    update_df.to_excel("update_data.xlsx", index=False)


if __name__ == "__main__":
    main()
