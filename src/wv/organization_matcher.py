"""
組織の一致を判定するモジュール。
"""

import constants as constants


class OrganizationMatcher:
    """
    組織の一致を判定するクラス。
    """

    def __init__(self, config: dict):
        """
        コンストラクタ。

        Args:
            config (dict): 設定辞書。
        """
        self.config = config
        self.total_weight = (
            config["weights"]["rank_weight"]
            + config["weights"]["similarity_weight"]
            + config["weights"]["member_weight"]
        )

    def get_thresholds(self, size: int) -> dict:
        """
        組織サイズに基づいて閾値を取得する。

        Args:
            size (int): 組織サイズ。

        Returns:
            dict: 閾値辞書。
        """
        thresholds = sorted(
            self.config[constants.THRESHOLDS], key=lambda x: x[constants.SIZE]
        )
        for threshold in thresholds:
            if size <= threshold[constants.SIZE]:
                return threshold
        return thresholds[-1]  # 最大サイズを超えた場合は最後の閾値を返す

    def calculate_rank_score(self, rank_diff: int) -> float:
        """
        ランク差のスコアを計算する。

        Args:
            rank_diff (int): ランク差。

        Returns:
            float: ランクスコア。
        """
        base_rank_weight = self.config["weights"][constants.RANK_WEIGHT]
        if rank_diff == 0:
            return base_rank_weight
        elif rank_diff > 0:
            # ランクダウンの場合、スコアはランク差に応じて減少（0.5ずつ減少）
            return (
                base_rank_weight - rank_diff * 0.5
                if base_rank_weight - rank_diff * 0.5 > 0
                else 0
            )
        else:
            # ランクアップの場合、スコアはランク差に応じてさらに減少（1ずつ減少）
            return (
                base_rank_weight - abs(rank_diff)
                if base_rank_weight - abs(rank_diff) > 0
                else 0
            )

    def calculate_similarity_score_with_ratio(self, row_dict: dict) -> dict:
        """
        構成比を考慮して類似度スコアを計算する。

        Args:
            row_dict (dict): 行データの辞書。

        Returns:
            dict: スコア辞書。
        """
        size_a = row_dict[constants.PREV_SIZE]
        size_b = row_dict[constants.CURR_SIZE]
        thresholds_a = self.get_thresholds(size_a)
        thresholds_b = self.get_thresholds(size_b)

        similarity_threshold = min(
            thresholds_a[constants.SIMILARITY_THRESHOLD],
            thresholds_b[constants.SIMILARITY_THRESHOLD],
        )
        member_ratio_threshold = min(
            thresholds_a[constants.MEMBER_RATIO_THRESHOLD],
            thresholds_b[constants.MEMBER_RATIO_THRESHOLD],
        )

        # ランク差のスコアを設定
        rank_score = self.calculate_rank_score(row_dict[constants.RANK_DIFF])

        similarity_score = (
            row_dict[constants.SIMILARITY_INDEX] >= similarity_threshold
        ) * self.config["weights"][constants.SIMILARITY_WEIGHT]
        member_score = (
            row_dict[constants.COMMON_RATIO] >= member_ratio_threshold
        ) * self.config["weights"][constants.MEMBER_WEIGHT]
        total_score = rank_score + similarity_score + member_score
        same_org = total_score >= self.total_weight

        # 3人未満で同じ組織名の場合、同一組織と見なす
        if (
            size_a < 3
            and size_b
            and row_dict[constants.PREV_ORG] == row_dict[constants.CURR_ORG]
        ):
            same_org = True

        return {
            "ランクスコア": rank_score,
            "類似度スコア": similarity_score,
            "メンバースコア": member_score,
            "総合スコア": total_score,
            "適用ルール": thresholds_a["comment"],
            constants.SAME_ORG: same_org,
        }
