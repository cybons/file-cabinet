"""
組織の処理を行うモジュール。
"""

from itertools import product

import constants as cst
import pandas as pd
from organization_matcher import OrganizationMatcher
from utils import (
    build_org_user_set,
    calculate_employee_ratio,
    calculate_rank,
    calculate_ratio_difference,
)


class OrganizationProcessor:
    """
    組織の処理を行うクラス。
    """

    def __init__(self, config: dict):
        """
        コンストラクタ。

        Args:
            config (dict): 設定辞書。
        """
        self.matcher = OrganizationMatcher(config)

    def process_all_organizations(
        self, df_A: pd.DataFrame, df_B: pd.DataFrame
    ) -> pd.DataFrame:
        """
        全ての組織を処理する関数。

        Args:
            df_A (pd.DataFrame): 前月組織データフレーム。
            df_B (pd.DataFrame): 当月組織データフレーム。

        Returns:
            pd.DataFrame: 処理された組織データフレーム。
        """
        # データフレームから組織とユーザーのマッピングを作成
        org_users_A = build_org_user_set(
            df_A, additional_columns=["org_code", "group_code", "type"]
        )
        org_users_B = build_org_user_set(df_B, additional_columns=["org_code", "type"])  # noqa: E501

        # 結果リストを作成
        results = []
        for org_a, org_b in product(org_users_A.items(), org_users_B.items()):
            result = self.process_organization_pair(org_a, org_b)
            if result:
                results.append(result)

        # 組織の一致判定と確定処理
        df_results = pd.DataFrame(results)
        df_results = self.update_organization_matches(df_results)
        return df_results

    def process_organization_pair(self, org_a: tuple, org_b: tuple) -> dict:
        """
        組織ペアを処理する関数。

        Args:
            org_a (tuple): 前月組織。
            org_b (tuple): 当月組織。
            matcher（OrganizationMatcher）:

        Returns:
            dict: 処理された組織ペアのデータ。
        """
        org_a_name, data_A = org_a
        org_b_name, data_B = org_b
        users_A = data_A["users"]
        users_B = data_B["users"]
        size_a = len(users_A)
        size_b = len(users_B)
        intersection = users_A.intersection(users_B)
        if not intersection:
            return None

        union = users_A.union(users_B)
        intersection_size = len(intersection)
        union_size = len(union)
        ratio_a = calculate_employee_ratio(data_A["info"])
        ratio_b = calculate_employee_ratio(data_B["info"])
        ratio_diff = calculate_ratio_difference(ratio_a, ratio_b)
        rank_diff = calculate_rank(org_a_name) - calculate_rank(org_b_name)
        result = {
            cst.PREV_ORG: org_a_name,
            cst.CURR_ORG: org_b_name,
            cst.PREV_SIZE: size_a,
            cst.CURR_SIZE: size_b,
            cst.COMMON_MEMBERS: intersection_size,
            cst.COMMON_RATIO: intersection_size / size_b if size_b > 0 else 0,
            cst.SIMILARITY_INDEX: intersection_size / union_size
            if union_size > 0
            else 0,
            cst.RATIO_DIFF: ratio_diff,
            cst.RANK_DIFF: rank_diff,
        }

        similarity_scores = self.matcher.calculate_similarity_score_with_ratio(result)  # noqa: E501
        result.update(similarity_scores)
        return result

    def update_organization_matches(self, df_results: pd.DataFrame) -> pd.DataFrame:  # noqa: E501
        """
        組織の一致判定と確定処理を行う関数。

        Args:
            df_results (pd.DataFrame): 組織データフレーム。

        Returns:
            pd.DataFrame: 更新された組織データフレーム。
        """
        df_results[cst.CONFIRMED] = False

        # 同一組織と見なされている場合に一括でCONFIRMEDをTrueに更新
        df_results.loc[df_results[cst.SAME_ORG], cst.CONFIRMED] = True

        # 確定がTrueになった前月組織と当月組織の同じ名前のものをさらに更新
        confirmed_prev = df_results[df_results[cst.CONFIRMED]][cst.PREV_ORG].unique()  # noqa: E501
        confirmed_curr = df_results[df_results[cst.CONFIRMED]][cst.CURR_ORG].unique()  # noqa: E501

        df_results.loc[df_results[cst.PREV_ORG].isin(confirmed_prev), cst.CONFIRMED] = (  # noqa: E501
            True
        )
        df_results.loc[df_results[cst.CURR_ORG].isin(confirmed_curr), cst.CONFIRMED] = (  # noqa: E501
            True
        )

        return df_results

    def calculate_and_update_organization_scores(
        self,
        df_A: pd.DataFrame,
        df_B: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        全ての組織のスコアを計算して更新する関数。

        Args:
            df_A (pd.DataFrame): 前月組織データフレーム。
            df_B (pd.DataFrame): 当月組織データフレーム。

        Returns:
            pd.DataFrame: スコアが計算され更新された組織データフレーム。
        """
        org_users_A = build_org_user_set(df_A, additional_columns=[cst.TYPE])
        org_users_B = build_org_user_set(df_B, additional_columns=[cst.TYPE])

        # 結果リストを作成
        results = []
        for org_a, org_b in product(org_users_A.items(), org_users_B.items()):
            result = self.process_organization_pair(org_a, org_b)
            if result:
                results.append(result)

        # スコアを計算して各列に分解して代入
        df_results = pd.DataFrame(results)

        # 組織の一致判定と確定処理
        df_results = self.update_organization_matches(df_results)

        return df_results

    def find_disjoint_organizations(results, df_A, df_B):
        """
        全ての結果から新設組織と抹消組織を抽出する。

        Args:
            results(pd.DataFrame): 結果データフレーム
            df_A (pd.DataFrame): 前月組織データフレーム。
            df_B (pd.DataFrame): 当月組織データフレーム。

        Returns:
            pd.DataFrame: スコアが計算され更新された組織データフレーム。
        """

        # 結果から前月と当月の組織を抽出
        prev_orgs_in_results = set(results[cst.PREV_ORG])
        curr_orgs_in_results = set(results[cst.CURR_ORG])

        # 前月と当月の全組織を取得
        all_prev_orgs = set(df_A[cst.ORG])
        all_curr_orgs = set(df_B[cst.ORG])

        # 共通ユーザーがいない組織を特定
        disjoint_prev_orgs = all_prev_orgs - prev_orgs_in_results
        disjoint_curr_orgs = all_curr_orgs - curr_orgs_in_results

        # 結果をデータフレームに変換
        disjoint_df = pd.DataFrame(
            {
                "組織": list(disjoint_prev_orgs) + list(disjoint_curr_orgs),
                "状態": ["抹消"] * len(disjoint_prev_orgs)
                + ["新設"] * len(disjoint_curr_orgs),
            }
        )

        return disjoint_df
