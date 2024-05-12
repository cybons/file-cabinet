"""
data_checker.py: データの整合性をチェックするクラスを提供します。

このモジュールは、データフレーム内のデータが特定の基準を満たしているかどうかを検証するためのクラスを含んでいます。
主にデータの事前処理や検証段階で使用されます。
"""

import re

import pandas as pd


class DataChecker:
    """
    社員番号、組織名、グループ名に関するデータ検証を行うクラスです。

    Attributes:
        employee_data (dict[str, str]): 社員番号と名前の辞書。
        organization_data (dict[str, bool]): 組織名が存在するかどうかの辞書。
        p (re.Pattern): グループ名に使用禁止の全角文字を検出する正規表現パターン。

    Args:
        employee_data (dict[str, str]): 社員番号をキー、名前を値とする辞書。
        organization_data (dict[str, bool]): 組織名をキー、存在するかどうかを値とする辞書。

    Returns:
        None
    """

    def __init__(
        self, employee_data: dict[str, str], organization_data: dict[str, str]
    ):
        self.employee_data = employee_data
        self.organization_data = organization_data

        self.p = re.compile("^.*[ァ-ヶＡ-Ｚａ-ｚ０-９]+.*$")

    def __check_employee(self, emp_id, name) -> bool:
        """
        社員番号と名前の照合を行います。

        Args:
            emp_id (str): 社員番号。
            name (str): 名前。

        Returns:
            bool: 社員番号と名前が一致するかどうか。
        """
        if emp_id in self.employee_data:
            return self.employee_data[emp_id] == name
        return False

    def __check_organization(self, org_name) -> bool:
        """
        組織名が存在するかをチェックします。

        Args:
            org_name (str): 組織名。

        Returns:
            bool: 組織名が存在するかどうか。
        """

        return org_name in self.organization_data

    def __check_group_name(self, group_name) -> bool:
        """
        グループ名に使用禁止の全角文字が含まれているかをチェックします。

        Args:
            group_name (str): グループ名。

        Returns:
            bool: 使用禁止の全角文字が含まれているかどうか。
        """
        return self.p.fullmatch(group_name) is not None

    def __check_all(self, row) -> pd.Series:
        """
        指定された行データに対して、全てのチェックを行い、結果を返します。

        Args:
            row (pd.Series): データフレームの行。

        Returns:
            pd.Series: 各チェックの結果を含むシリーズ。
        """
        return pd.Series(
            {
                "emp_id_valid": self.__check_employee(
                    row["emp_id"], row["name"]
                ),  # noqa: E501
                "org_valid": self.__check_organization(row["org_name"]),
                "group_name_valid": self.__check_group_name(row["group_name"]),
            }
        )

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        データフレームを受け取り、それぞれの行に対して定義されたチェックを行い、結果を追加した新しいデータフレームを返します。

        Args:
            df (pd.DataFrame): チェックを行うデータフレーム。

        Returns:
            pd.DataFrame: チェック結果が追加されたデータフレーム。
        """
        df_result = df.apply(self.__check_all, axis=1)
        df = pd.concat([df, df_result], axis=1)
        df["all_checks_passed"] = df[
            ["emp_id_valid", "org_valid", "group_name_valid"]
        ].all(axis=1)
        return df


def condition_data_checker(
    employee_dict: dict[str, str],
    organization_dict: dict[str, bool],
    target_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    指定されたデータフレームに対してデータ検証を行い、結果を返します。

    Args:
        employee_dict (dict[str, str]): 社員番号と名前の対応辞書。
        organization_dict (dict[str, bool]): 組織名の存在情報辞書。
        group_dict (str): チェック対象の全角文字列。
        target_df (pd.DataFrame): チェックを行うデータフレーム。

    Returns:
        pd.DataFrame: チェック結果が追加されたデータフレーム。
    """
    checker = DataChecker(employee_dict, organization_dict)
    processed_df = checker.process_dataframe(target_df)
    return processed_df


# データフレームの準備
df = pd.DataFrame(
    {
        "emp_id": ["001", "002", "004"],
        "name": ["Alice", "Bob", "David"],
        "org_name": ["Sales", "Engineering", "Unknown"],
        "group_name": ["開発部ア", "製造部", "研究部"],
    }
)

# 辞書データの準備
employee_dict2 = {"001": "Alice", "002": "Bob"}
organization_dict2 = {"Sales": True, "Engineering": True}
print(condition_data_checker(employee_dict2, organization_dict2, df))
