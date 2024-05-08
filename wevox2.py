"""
このモジュールは、異なる月に記録されたユーザーの組織パスデータを比較し、組織間の類似性を評価するための機能を提供します。

主な機能:
- ユーザーの組織パスを解析し、それぞれの組織についてDataFrameを生成。
- 月間データを比較して、ユーザー集合の類似度を計算し、組織間の関連性を評価。
- Jaccard指数とランク差を基に、組織がどれだけ似ているかを数値化。
- 類似度が高い組織ペアを特定し、それらを'finalized'としてマーク。

使用方法:
このモジュール内の `main` 関数を実行することで、全プロセスが自動的に処理され、結果がExcelファイルに保存されます。
"""

import json
from typing import NamedTuple

import pandas as pd

from excel_exporters import export_excel_data_formatting
from test_data import last_month, this_month


class OrgUsers(NamedTuple):
    """
    組織の名前とユーザーの集合を管理するクラス。

    Attributes:
        org_name (str): 組織の名前。
        users (set[str]): その組織に所属するユーザーの集合。
    """

    org_name: str
    users: set[str]

    def count(self) -> int:
        """
        組織に所属するユーザーの数をカウントする。

        Returns:
            int: 所属するユーザーの数。
        """
        return len(self.users)

    def rank(self) -> int:
        """
         組織のランクを返す。

        Returns:
            int: 組織ランク。
        """
        # 組織ランクは1からなので+1しとく
        return self.org_name.count("/") + 1


def load_rules(filename):
    """jsonのコンフィグファイルを読み込む"""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    rules: dict[str, dict[str, int | float] | None] = {
        # キーが存在しない場合は空の辞書を返す
        "allow_rules": data.get("allow_rules", {}),
        "deny_rules": data.get("deny_rules", {}),
    }
    return rules


def dict_to_df(data: dict[str, str]):
    """指定された辞書からデータフレームを生成する。ユーザーごとのパスを展開し、組織の階層ごとに行を作成する。"""
    rows = []
    for user, paths in data.items():
        for path in paths.split(","):
            full_path = ""
            orgs = path.strip().split("/")
            for org in orgs:
                full_path = f"{full_path}/{org}" if full_path else org
                rows.append({"user": user, "org": full_path})
    return pd.DataFrame(rows)


def create_comparison_result(
    last_org_data: OrgUsers,
    this_org_data: OrgUsers,
    common_users: set[str],
) -> dict[str, str | int | float]:
    """組織間の比較結果を辞書形式で作成する"""
    total_users = last_org_data.users.union(this_org_data.users)
    common_count = len(common_users)
    common_user_ratio = common_count / len(last_org_data.users)
    jaccard_index = common_count / len(total_users)
    rank_difference = abs(last_org_data.rank() - this_org_data.rank())

    return {
        "org_last": last_org_data.org_name,
        "org_this": this_org_data.org_name,
        "last_user_count": last_org_data.count(),
        "this_user_count": this_org_data.count(),
        "last_rank": last_org_data.rank(),
        "this_rank": this_org_data.rank(),
        "common_user_count": common_count,
        "common_user_ratio": common_user_ratio,
        "rank_difference": rank_difference,
        "jaccard_index": jaccard_index,
    }


def apply_rules_to_dataframe(df, rules):
    """DataFrame全体にルールを適用する関数"""
    # データフレームに対するdenyルールの適用
    # if "deny_rules" in rules and rules["deny_rules"]:
    #     for rule in rules["deny_rules"]:
    #         df["deny"] = (  # noqa: E501
    #             df["common_user_count"] <= rule.get("max_users", 0)
    #         ) & (df["rank_difference"] == 0)

    # allow_rulesの適用
    df["is_same_organization"] = False

    for rule in rules["allow_rules"]:
        conditions = (
            (df["common_user_count"] >= rule.get("min_users", 0))
            & (df["common_user_count"] <= rule.get("max_users", float("inf")))
            & (df["common_user_ratio"] >= rule.get("common_ratio", 0))
            & (df["jaccard_index"] >= rule.get("jaccard_index", 0))
            & (df["rank_difference"] == 0)
        )
        df["is_same_organization"] |= conditions

    return df


def adjustment_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """不要な列の削除、並び替え、列見出しの変更"""
    # 列の名称を変更
    columns_dict = {
        "org_last": "前月の組織",
        "org_this": "当月の組織",
        "common_user_count": "共通ユーザー数",
        "common_user_ratio": "共通ユーザー比率",
        "last_user_count": "前回ユーザー数",
        "this_user_count": "今回ユーザー数",
        "last_rank": "前回ランク",
        "this_rank": "今回ランク",
        "rank_difference": "ランク差",
        "jaccard_index": "ジャッカード指数",
        "is_same_organization": "同一組織と判定",
        "finalized": "確定",
    }
    # リネームと並び替えを統合して行う
    df = df.rename(columns=columns_dict)[list(columns_dict.values())]

    return df


def calculate_similarity(last_df: pd.DataFrame, this_df: pd.DataFrame):
    """前月と今月のデータから各組織のユーザー集合を作り、それぞれの組織間でユーザーの類似度を計算する。"""

    # 各組織のユーザーセットをハッシュマップに格納
    last_groups: dict[str, set[str]] = {
        org: set(users) for org, users in last_df.groupby("org")["user"]
    }  # 前月組織セット
    this_groups: dict[str, set[str]] = {
        org: set(users) for org, users in this_df.groupby("org")["user"]
    }  # 当月組織セット

    results: list[dict[str, str | int | float]] = []

    for last_org, last_users in last_groups.items():
        for this_org, this_users in this_groups.items():
            common_users = last_users.intersection(this_users)
            if common_users:  # 共通ユーザーが存在する場合のみ結果を生成
                last_org_data = OrgUsers(last_org, last_users)
                this_org_data = OrgUsers(this_org, this_users)
                result = create_comparison_result(
                    last_org_data, this_org_data, common_users
                )
                results.append(result)

    return pd.DataFrame(results)


def main():
    """メイン処理"""

    # last_monthとthis_monthのデータをDataFrameに変換
    last_month_df = dict_to_df(last_month)
    this_month_df = dict_to_df(this_month)

    rules = load_rules("config.json")

    # 類似度計算
    comparison_result = calculate_similarity(last_month_df, this_month_df)  # noqa: E501

    # ルール適用
    comparison_result = apply_rules_to_dataframe(comparison_result, rules)
    print(comparison_result)

    comparison_result["finalized"] = comparison_result.groupby("org_last")[
        "is_same_organization"
    ].transform("any") | comparison_result.groupby("org_this")[
        "is_same_organization"
    ].transform(
        "any"
    )

    comparison_result = adjustment_dataframe(comparison_result)

    # Excelファイルへの書き込み
    export_excel_data_formatting("comparison_results.xlsx", comparison_result)

    # 結果を出力
    print("処理が完了しました。結果は 'comparison_results.xlsx' に保存されています。")


if __name__ == "__main__":
    main()
