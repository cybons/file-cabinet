"""
このモジュールは組織とユーザーデータの処理を行う関数を含んでいます。
提供されたDataFrameに基づいてユーザーデータをフィルタリングおよびラベリングし、組織構造と条件に応じたデータの取り扱いを可能にします。
"""

import numpy as np
import pandas as pd

# サンプルデータの作成
data_org = {
    "org_code": ["001", "002", "003", "004"],
    "org_name": ["本社", "支社A", "支社B", "部署X"],
    "parent_org_code": [None, "001", "001", "003"],
    "org_fullname": ["本社", "本社/支社A", "本社/支社B", "本社/支社B/部署X"],
}
org_df = pd.DataFrame(data_org)

data_condition = {
    "org_code": ["001", "003"],
    "配下含む": ["いいえ", "はい"],
    "正社員": ["いいえ", "いいえ"],
    "派遣": ["いいえ", "はい"],
    "契約": ["はい", "はい"],
    "create_type_org": ["はい", "いいえ"],
}
condition_df = pd.DataFrame(data_condition)

data_user_org = {
    "org_code": ["001", "002", "003", "004"],
    "user_code": ["U001", "U002", "U003", "U004"],
    "employee_type": ["正社員", "正社員", "派遣", "契約"],
}
user_org = pd.DataFrame(data_user_org)


def get_all_sub_orgs(org_code, org_df):
    """
    指定された組織コードに対するすべての子組織コードを再帰的に取得します。

    パラメータ:
    - org_code: 親組織の組織コード。
    - org_df: 組織データを含むDataFrame。

    戻り値:
    - 対象組織コードのリスト。
    """

    sub_orgs = set()
    direct_subs = org_df[
        org_df["parent_org_code"] == org_code
    ].index  # インデックスを直接利用
    sub_orgs.update(direct_subs)
    for sub in direct_subs:
        sub_orgs.update(get_all_sub_orgs(sub, org_df))
    return sub_orgs


# 社員タイプを条件にマッチさせるための関数
def filter_employee_types(row, user_org_df):
    """
    社員タイプ（正社員、派遣、契約）に基づいてユーザーをフィルタリングします。

    パラメータ:
    - row: 条件を含むDataFrameからの行で、社員タイプの条件が含まれます。
    - user_org_df: ユーザーと組織の情報を含むDataFrame。

    戻り値:
    - 条件に一致するユーザーのDataFrame。
    """
    conditions = []
    if row["正社員"] == "はい":
        conditions.append(user_org_df["employee_type"] == "正社員")
    if row["派遣"] == "はい":
        conditions.append(user_org_df["employee_type"] == "派遣")
    if row["契約"] == "はい":
        conditions.append(user_org_df["employee_type"] == "契約")
    return (
        user_org_df[np.logical_or.reduce(conditions)] if conditions else pd.DataFrame()
    )


# 組織名に社員タイプを追加する関数
def add_employee_type_to_orgname(user_row, org_df):
    """
    必要に応じて組織名にユーザーの雇用タイプ（正社員、派遣、契約）を追加します。

    パラメータ:
    - user_row: ユーザーデータの行。
    - org_df: 組織データを含むDataFrame。

    戻り値:
    - 変更後の組織フルネーム。
    """
    if user_row["create_type_org"] == "はい":
        org_fullname = org_df.loc[user_row["org_code"], "org_fullname"]
        return f"{org_fullname}/{user_row['employee_type']}"
    return org_df.loc[user_row["org_code"], "org_fullname"]


# matching_dfを作る際に必要なカラムを保持する
# ここで「対象組織コード」を元にしてユーザー情報と組織情報を結合させる例
def filter_and_label_users_by_org(org_df, condition_df, user_org):
    """
    組織構造と指定された条件に基づいてユーザーをフィルタリングし、ラベル付けを行います。
    結果としてマッチングしたユーザーとマッチングしないユーザーの2つのDataFrameを返します。

    パラメータ:
    - org_df: 組織データを含むDataFrame。
    - condition_df: 組織とユーザーの条件を含むDataFrame。
    - user_org: ユーザーとその所属組織情報を含むDataFrame。

    戻り値:
    - (マッチングしたユーザーのDataFrame, マッチングしないユーザーのDataFrame)
    """
    org_df.set_index("org_code", inplace=True)
    condition_df["対象組織コード"] = condition_df.apply(
        lambda x: (
            [x["org_code"]] + list(get_all_sub_orgs(x["org_code"], org_df))
            if x["配下含む"] == "はい"
            else [x["org_code"]]
        ),
        axis=1,
    )

    matching_df = pd.DataFrame()
    for _, condition in condition_df.iterrows():
        applicable_users = user_org[
            user_org["org_code"].isin(condition["対象組織コード"])
        ]
        filtered_users = filter_employee_types(condition, applicable_users)
        if not filtered_users.empty:
            filtered_users["create_type_org"] = condition["create_type_org"]
            matching_df = pd.concat([matching_df, filtered_users], ignore_index=True)

    # matching_dfに含まれるユーザーを除外してnon_matching_dfを作成
    non_matching_df = user_org[~user_org["user_code"].isin(matching_df["user_code"])]

    return matching_df, non_matching_df


matching_df, non_matching_df = filter_and_label_users_by_org(
    org_df, condition_df, user_org
)
print(matching_df)
print(non_matching_df)
