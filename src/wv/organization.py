"""
組織の親子関係を管理するモジュール。
"""


class SimulationOrg:
    """
    組織の親子関係を管理するクラス。
    """

    def __init__(
        self,
        org_name: str,
        group_id: str = None,
        rank: int = None,
        parent: "SimulationOrg" = None,
    ):
        """
        コンストラクタ。

        Args:
            org_name (str): 組織名。
            group_id (str, optional): グループID。デフォルトはNone。
            rank (int, optional): ランク。デフォルトはNone。
            parent (SimulationOrg, optional): 親組織。デフォルトはNone。
        """
        self.org_name = org_name
        self.group_id = group_id
        self.rank = rank
        self.parent = parent
        self.children: list[SimulationOrg] = []

    def add_child(self, child_org: "SimulationOrg") -> None:
        """
        子組織を追加する。

        Args:
            child_org (SimulationOrg): 子組織のインスタンス。
        """
        self.children.append(child_org)
        child_org.parent = self

    def update_org_name(self, new_name: str) -> None:
        """
        組織名を更新する。

        Args:
            new_name (str): 新しい組織名。
        """
        self.org_name = new_name
        for child in self.children:
            child.update_tree_name()

    def update_tree_name(self) -> None:
        """
        ツリーネームを更新する。
        """
        if self.parent:
            self.org_name = f"{self.parent.get_tree_name().split('/')[-1]}/{self.org_name.split('/')[-1]}"  # noqa: E501
            for child in self.children:
                child.update_tree_name()

    def get_tree_name(self) -> str:
        """
        ツリーネームを取得する。

        Returns:
            str: ツリーネーム。
        """
        if self.parent:
            return f"{self.parent.get_tree_name()}/{self.org_name.split('/')[-1]}"  # noqa: E501
        return self.org_name

    def __repr__(self) -> str:
        """
        組織の文字列表現を返す。

        Returns:
            str: 組織の文字列表現。
        """
        return f"SimulationOrg(org_name={self.org_name}, group_id={self.group_id}, rank={self.rank})"  # noqa: E501
