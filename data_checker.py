"""
data_checker.py: データの整合性をチェックするクラスを提供します。

このモジュールは、データフレーム内のデータが特定の基準を満たしているかどうかを検証するためのクラスを含んでいます。
主にデータの事前処理や検証段階で使用されます。
エラーは元のExcelファイルにコメントとして書き戻します。
"""

import gc
import json
import re

import pandas as pd
import win32com.client as win32


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
        self.errors = []

    def __check_employee(self, emp_id: str, name: str) -> str | None:
        """
        社員番号と名前が一致するかどうかをチェックします。

        Args:
            emp_id (str): 社員番号。
            name (str): 名前。

        Returns:
            str | None: 不一致の場合はエラーメッセージを返し、一致する場合は None を返します。
        """
        if emp_id not in self.employee_data:
            return f"社員番号 {emp_id} が存在しません。"
        if self.employee_data[emp_id] != name:
            return f"名前が一致しません: 登録されている名前は {self.employee_data[emp_id]} です。"
        return None

    def __check_organization(self, org_name: str) -> str | None:
        """
        組織名が存在するかどうかをチェックします。

        Args:
            org_name (str): 組織名。

        Returns:
            str | None: 組織名が存在しない場合はエラーメッセージを返し、存在する場合は None を返します。
        """
        if org_name not in self.organization_data:
            return f"組織名 {org_name} が存在しません。"
        return None

    def __check_group_name(self, group_name) -> str | None:
        """
        グループ名に不適切な文字が含まれているかどうかをチェックします。

        Args:
            group_name (str): グループ名。

        Returns:
            str | None: 不適切な文字が含まれている場合はエラーメッセージを返し、問題ない場合は None を返します。
        """
        if self.p.fullmatch(group_name) is None:
            return "グループ名に不適切な文字が含まれています。"
        return None

    def process_dataframe(self, df: pd.DataFrame) -> list:
        """
        データフレーム内のデータに対してチェックを行い、エラーがあれば詳細を記録します。

        Args:
            df (pd.DataFrame): チェックするデータフレーム。

        Returns:
            list[dict]: 各行に発見されたエラーの詳細を含む辞書のリスト。
        """
        self.errors = []
        df.apply(self.__check_all, axis=1)
        return self.errors

    def __check_all(self, row) -> pd.Series:
        """
        与えられた行に対して全てのチェックを実施し、エラーがあるかどうかを判断します。

        Args:
            row (pd.Series): チェックする行データ。

        Returns:
            bool: 行が全てのチェックをパスした場合はTrue、そうでない場合はFalseを返します。
        """

        emp_error = self.__check_employee(row["emp_id"], row["name"])
        org_error = self.__check_organization(row["org_name"])
        group_error = self.__check_group_name(row["group_name"])

        if any([emp_error, org_error, group_error]):
            error_info = {
                "row_number": row["original_row_number"],  # 保存した行番号を使用
                "submitted_values": {
                    "emp_id": row["emp_id"],
                    "name": row["name"],
                    "org_name": row["org_name"],
                    "group_name": row["group_name"],
                },
                "errors": {
                    "employee": emp_error or "ok",
                    "organization": org_error or "ok",
                    "group_name": group_error or "ok",
                },
                "sheet_name": row["sheet_name"],
            }
            self.errors.append(error_info)
        return not any([emp_error, org_error, group_error])

    def is_data_valid(self) -> bool:
        """
        チェック済みのデータが全てエラーなしであるかどうかを確認します。

        Returns:
            bool: データが全て有効であればTrue、一つでもエラーがあればFalse。
        """
        return not self.errors


def condition_data_checker(
    employee_dict: dict[str, str],
    organization_dict: dict[str, bool],
    target_df: pd.DataFrame,
) -> list:
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


def save_errors_to_excel(data, filename="your_file.xlsx"):
    """
    DataCheckerクラスから受け取ったエラーデータをExcelファイルに保存する。

    この関数は、DataCheckerクラスのインスタンスから生成されたエラーデータを
    Excelの指定されたセルにコメントとして追加し、エラー内容に応じてフォントカラーを
    赤色に設定します。また、コメントは常に表示されるよう設定します。

    Args:
        data (list of dict): エラー情報を含む辞書のリスト。各辞書は
            'row_number', 'errors', 'sheet_name' キーを持つ必要があります。
        filename (str): 保存するExcelファイルの名前。デフォルトは 'your_file.xlsx'。

    Returns:
        None
    """
    try:
        # Excelを起動
        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.Visible = True

        # 新しいワークブックを開く
        wb = excel.Workbooks.Add()
        # キーの最大長を計算
        max_key_length = max(len(key) for item in data for key in item["errors"])  # noqa: E501

        for item in data:
            ws = wb.Sheets.Add(After=wb.Sheets(wb.Sheets.Count))
            ws.Name = item["sheet_name"]
            row_number = item["row_number"]
            errors = item["errors"]

            # セルを選択してコメントを追加
            cell = ws.Cells(row_number, 2)
            error_text = ""
            for key, value in errors.items():
                padded_key = key.ljust(max_key_length)
                error_text += f"{padded_key}: {value}\n"

            if cell.Comment is None:
                comment = cell.AddComment(error_text.strip())
            else:
                comment = cell.Comment
                comment.Text(error_text.strip())

            # コメントのサイズを設定
            comment.Shape.Width = 200  # 幅を200ポイントに設定
            comment.Shape.Height = 100  # 高さを100ポイントに設定

            # コメントを常に表示
            comment.Visible = True

            # エラーメッセージごとに色を設定
            pos = 1
            for key, value in errors.items():
                padded_key = key.ljust(max_key_length)
                length = len(f"{padded_key}: {value}") + 1
                if value != "ok":
                    comment.Shape.TextFrame.Characters(pos, length).Font.Color = 255  # noqa: E501
                pos += length
        excel.DisplayAlerts = False
        wb.SaveAs(filename)

    except Exception as e:  # pylint: disable= W0718
        print(f"エラーが発生しました: {e}")
    finally:
        excel.DisplayAlerts = True
        # エラーが発生してもしなくても、Excelを閉じる
        if "wb" in locals():  # ワークブックが存在するかチェック
            wb.Close(False)  # 保存せずにワークブックを閉じる
            del wb
        if "excel" in locals():  # Excelアプリケーションが存在するかチェック
            excel.Quit()  # Excelアプリケーションを終了
            del excel
        gc.collect()


# データフレームの準備
test_df = pd.DataFrame(
    {
        "emp_id": ["001", "002", "004"],
        "name": ["Alice", "Bob", "David"],
        "org_name": ["Sales", "Engineering", "Unknown"],
        "group_name": ["開発部ア", "製造部", "研究部"],
        "sheet_name": ["sheet3", "sheet4", "sheet5"],
    }
)

test_df["original_row_number"] = test_df.index + 2
print(test_df)
# 辞書データの準備
employee_dict2 = {"001": "Alice", "002": "Bob"}
organization_dict2 = {"Sales": True, "Engineering": True}
data2 = condition_data_checker(employee_dict2, organization_dict2, test_df)
print(
    json.dumps(
        data2,
        indent=4,
        ensure_ascii=False,
    )
)
with open("test.json", "w", encoding="utf-8") as f:
    json.dump(
        data2,
        f,
        indent=2,
        ensure_ascii=False,
    )
save_errors_to_excel(data2)
