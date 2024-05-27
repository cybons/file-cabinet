"""
更新シミュレーションを行うモジュール。
"""

from collections import defaultdict

import constants as constants
import pandas as pd
from organization import SimulationOrg


def simulate_updates_with_hierarchy(
    prev_orgs: pd.DataFrame,
    curr_orgs: pd.DataFrame,
    confirmed_df: pd.DataFrame,  # noqa: E501
) -> pd.DataFrame:
    """
    ランク別辞書を用いて組織の更新シミュレーションを行う関数。

    Args:
        prev_orgs (pd.DataFrame): 前月組織データフレーム。
        curr_orgs (pd.DataFrame): 当月組織データフレーム。
        confirmed_df (pd.DataFrame): 確定データフレーム。

    Returns:
        pd.DataFrame: 更新データを含むデータフレーム。
    """
    # ランク別辞書を作成
    rank_dict = defaultdict(list)

    # 前月組織をランク別に分類
    for _, row in prev_orgs.iterrows():
        org = SimulationOrg(
            org_name=row["org"], group_id=row["group_id"], rank=row["rank"]
        )
        rank_dict[row["rank"]].append(org)

    # 当月組織をランク別に分類
    for _, row in curr_orgs.iterrows():
        org = SimulationOrg(org_name=row["org"], rank=row["rank"])
        rank_dict[row["rank"]].append(org)

    # 親子関係の構築
    for rank in sorted(rank_dict.keys()):
        for org in rank_dict[rank]:
            parent_name = "/".join(org.org_name.split("/")[:-1])
            if parent_name:
                for parent_org in rank_dict[rank - 1]:
                    if parent_org.org_name.split("/")[-1] == parent_name:
                        parent_org.add_child(org)
                        break

    # ツリーネームリストの初期化
    tree_name_list = {
        org.get_tree_name() for rank in rank_dict for org in rank_dict[rank]
    }

    # 確定データをもとに同一組織の更新シミュレーションを行う
    updates = []
    for _, row in confirmed_df.iterrows():
        if row[constants.SAME_ORG]:
            prev_org_name = row[constants.PREV_ORG]
            curr_org_name = row[constants.CURR_ORG]
            for org in rank_dict[row["rank_prev"]]:
                if org.org_name == prev_org_name:
                    if curr_org_name not in tree_name_list:
                        org.update_org_name(curr_org_name)
                        tree_name_list = {
                            org.get_tree_name()
                            for rank in rank_dict
                            for org in rank_dict[rank]
                        }
                    else:
                        # 一時的な名前に変更してから更新する
                        temp_name = f"{curr_org_name}_temp"
                        org.update_org_name(temp_name)
                        tree_name_list = {
                            org.get_tree_name()
                            for rank in rank_dict
                            for org in rank_dict[rank]
                        }
                        org.update_org_name(curr_org_name)
                        tree_name_list = {
                            org.get_tree_name()
                            for rank in rank_dict
                            for org in rank_dict[rank]
                        }

    # 更新データの作成
    for rank in sorted(rank_dict.keys()):
        for org in rank_dict[rank]:
            if org.group_id:
                tree_name = org.get_tree_name()
                updates.append({"group_id": org.group_id, "org_name": tree_name})  # noqa: E501

    return pd.DataFrame(updates)
