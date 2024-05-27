"""
メインスクリプト。
"""

import os

import pandas as pd
import yaml
from export_to_excel import export_to_excel
from organization_processor import OrganizationProcessor

data_A = [
    {"org": "営業部", "user": "u1", "type": "full_time"},
    {"org": "営業部", "user": "u2", "type": "full_time"},
    {"org": "営業部", "user": "u3", "type": "full_time"},
    {"org": "営業部/営業課", "user": "u4", "type": "part_time"},
    {"org": "営業部/営業課", "user": "u5", "type": "part_time"},
    {"org": "営業部/営業課", "user": "u6", "type": "part_time"},
    {"org": "開発部", "user": "u7", "type": "full_time"},
    {"org": "開発部", "user": "u8", "type": "full_time"},
    {"org": "開発部", "user": "u9", "type": "full_time"},
    {"org": "開発部/開発課", "user": "u10", "type": "part_time"},
    {"org": "開発部/開発課", "user": "u11", "type": "part_time"},
    {"org": "開発部/開発課", "user": "u12", "type": "part_time"},
    {"org": "サポート部", "user": "u13", "type": "full_time"},
    {"org": "サポート部", "user": "u14", "type": "full_time"},
    {"org": "サポート部", "user": "u15", "type": "full_time"},
    {"org": "サポート部/サポート課", "user": "u16", "type": "part_time"},
    {"org": "サポート部/サポート課", "user": "u17", "type": "part_time"},
    {"org": "サポート部/サポート課", "user": "u18", "type": "part_time"},
    {"org": "企画部", "user": "u19", "type": "full_time"},
    {"org": "企画部", "user": "u20", "type": "full_time"},
    {"org": "企画部", "user": "u21", "type": "full_time"},
    {"org": "企画部/企画課", "user": "u22", "type": "part_time"},
    {"org": "企画部/企画課", "user": "u23", "type": "part_time"},
    {"org": "企画部/企画課", "user": "u24", "type": "part_time"},
    {"org": "人事部", "user": "u25", "type": "full_time"},
    {"org": "人事部", "user": "u26", "type": "full_time"},
    {"org": "人事部", "user": "u27", "type": "full_time"},
    {"org": "人事部/人事課", "user": "u28", "type": "part_time"},
    {"org": "人事部/人事課", "user": "u29", "type": "part_time"},
    {"org": "人事部/人事課", "user": "u30", "type": "part_time"},
    {"org": "法務部", "user": "u31", "type": "full_time"},
    {"org": "法務部", "user": "u32", "type": "full_time"},
    {"org": "法務部", "user": "u33", "type": "full_time"},
    {"org": "法務部/法務課", "user": "u34", "type": "part_time"},
    {"org": "法務部/法務課", "user": "u35", "type": "part_time"},
    {"org": "法務部/法務課", "user": "u36", "type": "part_time"},
    {"org": "経理部", "user": "u37", "type": "full_time"},
    {"org": "経理部", "user": "u38", "type": "full_time"},
    {"org": "経理部", "user": "u39", "type": "full_time"},
    {"org": "経理部/経理課", "user": "u40", "type": "part_time"},
    {"org": "経理部/経理課", "user": "u41", "type": "part_time"},
    {"org": "経理部/経理課", "user": "u42", "type": "part_time"},
]


df_A = pd.DataFrame(data_A)

data_B = [
    {"org": "営業部", "user": "u1", "type": "full_time"},
    {"org": "営業部", "user": "u2", "type": "full_time"},
    {"org": "営業部", "user": "u3", "type": "full_time"},
    {"org": "営業部/営業課", "user": "u4", "type": "part_time"},
    {"org": "営業部/営業課", "user": "u5", "type": "part_time"},
    {"org": "営業部/営業課", "user": "u6", "type": "part_time"},
    {"org": "開発部", "user": "u9", "type": "full_time"},
    {"org": "開発部", "user": "u10", "type": "full_time"},
    {"org": "開発部", "user": "u11", "type": "full_time"},
    {"org": "開発部/開発課", "user": "u12", "type": "part_time"},
    {"org": "開発部/開発課", "user": "u13", "type": "part_time"},
    {"org": "開発部/開発課", "user": "u14", "type": "part_time"},
    {"org": "サポート部", "user": "u15", "type": "full_time"},
    {"org": "サポート部", "user": "u16", "type": "full_time"},
    {"org": "サポート部", "user": "u17", "type": "full_time"},
    {"org": "サポート部/サポート課", "user": "u18", "type": "part_time"},
    {"org": "サポート部/サポート課", "user": "u19", "type": "part_time"},
    {"org": "サポート部/サポート課", "user": "u20", "type": "part_time"},
    {"org": "企画部", "user": "u21", "type": "full_time"},
    {"org": "企画部", "user": "u22", "type": "full_time"},
    {"org": "企画部", "user": "u23", "type": "full_time"},
    {"org": "企画部/企画課", "user": "u24", "type": "part_time"},
    {"org": "企画部/企画課", "user": "u25", "type": "part_time"},
    {"org": "企画部/企画課", "user": "u26", "type": "part_time"},
    {"org": "人事部", "user": "u27", "type": "full_time"},
    {"org": "人事部", "user": "u28", "type": "full_time"},
    {"org": "人事部", "user": "u29", "type": "full_time"},
    {"org": "人事部/人事課", "user": "u30", "type": "part_time"},
    {"org": "人事部/人事課", "user": "u31", "type": "part_time"},
    {"org": "人事部/人事課", "user": "u32", "type": "part_time"},
    {"org": "法務部", "user": "u33", "type": "full_time"},
    {"org": "法務部", "user": "u34", "type": "full_time"},
    {"org": "法務部", "user": "u35", "type": "full_time"},
    {"org": "法務部/法務課", "user": "u36", "type": "part_time"},
    {"org": "法務部/法務課", "user": "u37", "type": "part_time"},
    {"org": "法務部/法務課", "user": "u38", "type": "part_time"},
    {"org": "経理部", "user": "u39", "type": "full_time"},
    {"org": "経理部", "user": "u40", "type": "full_time"},
    {"org": "経理部", "user": "u41", "type": "full_time"},
    {"org": "経理部/経理課", "user": "u42", "type": "part_time"},
    {"org": "経理部/経理課", "user": "u43", "type": "part_time"},
    {"org": "経理部/経理課", "user": "u44", "type": "part_time"},
]
df_B = pd.DataFrame(data_B)


def load_config():
    path = os.path.dirname(__file__)
    filepath = os.path.join(path, "organization_matching_config.yaml")
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    return config


def main():
    """
    メイン関数。データの準備、整合性チェック、結果の更新、および更新シミュレーションを行う。
    """
    config = load_config()
    orgProcess = OrganizationProcessor(config)

    df_results = orgProcess.calculate_and_update_organization_scores(df_A, df_B)
    export_to_excel(df_results, "pandas_to_excel.xlsx")


if __name__ == "__main__":
    main()
