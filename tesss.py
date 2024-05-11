import datetime

import numpy as np
import pandas as pd
import streamlit as st

# サンプルデータの作成
# data1 = {"org_code": ["A001", "A002", "A003"], "user_code": ["U001", "U002", "U003"]}


# df1 = pd.DataFrame(data1)

# data2 = {
#     "user_code": ["U001", "U002", "U003", "U004"],
#     "email": [
#         "user1@example.com",
#         "user2@example.com",
#         "user3@example.com",
#         "user4@example.com",
#     ],
# }
# df2 = pd.DataFrame(data2)

# df1とdf2を'user_code'をキーにして内部結合
# merged_df = pd.merge(df1, df2, on="user_code").drop(columns="user_code")


# print(merged_df)
# def on_data_edited(key, editor_key):

#     # st.session_state[key] = df.assign(**st.session_state[editor_key])
#     st.session_state[DF_KEY] = df.assign(**edited_df)
#     print(key)
#     print(st.session_state[key])
#     print(editor_key)
#     print(st.session_state[editor_key])


# 初期データフレームの作成
data = {
    "名前": ["田中", "鈴木", "佐藤"],
    "年齢": [28, 34, 22],
    "職業": ["エンジニア", "デザイナー", "マーケター"],
    "許可": [True, False, True],
    "再申請": [False, True, False],
}
st.markdown(
    """
        <style>
        button {
            height: auto;
            padding-top: 20px !important;
            padding-bottom: 20px !important;
        }
        </style>
    """,
    unsafe_allow_html=True,
)

DF_KEY = "my_def"
DF_EDITOR_KEY = "data_editor"
if DF_KEY not in st.session_state:
    st.session_state[DF_KEY] = pd.DataFrame(data)


@st.experimental_dialog("承認確認")
def approve_button3():
    st.write("本当に良い？")
    if st.button("OKですって"):
        st.session_state["ok_button3"] = True
        st.rerun()


if "ok_button3" not in st.session_state:
    if st.button("承認"):
        approve_button3()
if st.session_state.get("ok_button3", False):
    st.success("承認されました3")


d = st.date_input("作業日を入力してください。", datetime.datetime.now())
st.write("基準日：", d)
st.divider()


def button2():
    rows = 3
    cols = 2
    # ボタンのタイトルとクリック時の関数
    button_dict = {
        "ボタン1": lambda: st.write("ボタン1が押されました"),
        "ボタン2": lambda: st.write("ボタン2が押されました"),
        "ボタン3": lambda: st.write("ボタン3が押されました"),
        "ボタン4": lambda: st.write("ボタン4が押されました"),
        "ボタン5": lambda: st.write("ボタン5が押されました"),
        "ボタン6": lambda: st.write("ボタン6が押されました"),
    }

    # 各ボタンの配置
    for r in range(rows):
        # この行に対する列オブジェクトを作成
        columns = st.columns(cols)  # ここで cols は列オブジェクトのリストを表す

        for c in range(cols):
            # 各列にボタンを配置
            i = r * cols + c
            if i < len(button_dict):
                title = list(button_dict.keys())[i]
                func = button_dict[title]
                # cols[c] を使用して特定の列にアクセスし、ボタンを配置
                columns[c].button(title, key=f"button_{i}", on_click=func)


def app():
    button2()

    st.title("データレビューアプリケーション")

    df = st.session_state[DF_KEY]

    with st.container():

        edited_df = st.data_editor(
            df,
            num_rows="fixed",
            disabled=("名前", "年齢", "職業"),
            # on_change=on_data_edited,
            # args=(DF_KEY, DF_EDITOR_KEY),
            key=DF_EDITOR_KEY,
        )  # DataFrame全体を表示

    # 更新ボタン
    if st.button("更新"):
        # セッション状態からデータフレームへの適用

        st.write(st.session_state[DF_EDITOR_KEY])
        # 編集後のデータを `assign` で元のデータフレームにマージ

        # セッション状態のデータフレームを更新
        st.session_state[DF_KEY] = df.assign(**edited_df)

        # print(st.session_state[DF_KEY])
        st.session_state["update_message"] = "データフレームを更新しました。"
        st.rerun()
    update_message = st.session_state.get("update_message", "")
    st.text(update_message)
    df2 = pd.DataFrame(np.random.randn(3000, 5), columns=list("ABCDE"))

    df2 = pd.DataFrame(np.random.randn(3000, 5), columns=list("ABCDE"))
    st.dataframe(df2, height=600)


app()
