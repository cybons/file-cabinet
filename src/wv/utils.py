"""
ユーティリティ関数を提供するモジュール。
"""

from collections import defaultdict

import constants as constants
import pandas as pd


# データフレームから組織とユーザーのマッピングをdictとして作成する関数
def build_org_user_set(
    df: pd.DataFrame, additional_columns: list[str] = None
) -> defaultdict:
    """
    データフレームから組織とユーザーのマッピングを作成する関数。

    Args:
        df (pd.DataFrame): データフレーム。
        additional_columns (list[str], optional): 追加の列名のリスト。デフォルトはNone。

    Returns:
        defaultdict: 組織とユーザーのマッピング。
    """
    if additional_columns is None:
        additional_columns = []

    org_users = defaultdict(lambda: {"users": set(), "info": defaultdict(list)})  # noqa: E501
    for record in df.to_dict("records"):
        org_name = record[constants.ORG]

        # 「組織」という最上位組織を除外
        if org_name == "組織":
            continue

        org_hierarchy = org_name.split("/")

        # 上位の組織にユーザーを追加
        for i in range(len(org_hierarchy)):
            current_org = "/".join(org_hierarchy[: i + 1])
            if current_org == "組織":
                continue
            org_users[current_org]["users"].add(record[constants.USER])
            for col in additional_columns:
                org_users[current_org]["info"][col].append(record[col])

    return org_users


# 社員と派遣社員の比率を計算する関数
def calculate_employee_ratio(info):
    """
    社員と派遣社員、契約社員の比率を計算する関数。

    Args:
        info (defaultdict): 組織の情報。

    Returns:
        dict: 社員、派遣社員、契約社員の比率。
    """
    total = len(info[constants.TYPE])
    full_time = info[constants.TYPE].count(constants.FULL_TIME)
    part_time = info[constants.TYPE].count(constants.PART_TIME)
    contract_employee = info[constants.TYPE].count(constants.CONTRACT_EMPLOYEE)
    return {
        "full_time_ratio": full_time / total if total > 0 else 0,
        "part_time_ratio": part_time / total if total > 0 else 0,
        "contract_employee_ratio": contract_employee / total if total > 0 else 0,  # noqa: E501
    }


# 組織の構成比率の差を計算する関数
def calculate_ratio_difference(ratio_a, ratio_b):
    """
    構成比の違いを計算する関数。

    Args:
        ratio_a (dict): 比率A。
        ratio_b (dict): 比率B。

    Returns:
        float: 構成比の違い。
    """
    full_time_diff = abs(ratio_a["full_time_ratio"] - ratio_b["full_time_ratio"])  # noqa: E501
    part_time_diff = abs(ratio_a["part_time_ratio"] - ratio_b["part_time_ratio"])  # noqa: E501
    contract_employee_diff = abs(
        ratio_a["contract_employee_ratio"] - ratio_b["contract_employee_ratio"]
    )

    # 各比率の差の平均を計算し、100から引いて100%表記の似ている度合いを示す
    avg_diff = (full_time_diff + part_time_diff + contract_employee_diff) / 3
    similarity_percentage = 1 - avg_diff
    return similarity_percentage


def calculate_rank(org: str) -> int:
    """
    組織のランクを計算する。

    Args:
        org (str): 組織名。

    Returns:
        int: ランク。
    """
    return org.count("/") + 1
