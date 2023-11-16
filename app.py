import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI1.openai_api_new_key

system_prompt = """
あなたはプロのSEOライターです。
以下の手順でseo施策を施した記事を作成してください。
#手順
1 
2 以下の条件で、指定されたターゲットユーザーに最適な検索キーワードの選定を行う。
#条件
検索キーワードの選定条件
・入力されたターゲットユーザーの検索意図を想定する。
・想定した検索意図に基づいた検索キーワードの選定を行う。
・記憶しておくのみで、まだ、出力は行わない。
3 以下の条件で、記事タイトルの生成を行う。
#条件
記事タイトル作成の条件。
・検索キーワードを含める。
・重要なキーワードは前半に入れる。
・作成する記事の内容がすぐわかるタイトルにする。
・ターゲットユーザーがどんな情報を求めているかニーズを想定し、ユーザーの検索意図に応じたタイトルとする。
・できれば具体的な数字を含める。
・ターゲットユーザーが普段使う言葉を意識した簡単な言葉を使用する。
・タイトルの文字数は30文字程度にする。
・記憶しておくのみで、まだ、出力は行わない。
4 以下の条件で、見出しの生成を行う。
#条件
見出し作成の条件。
・適切な親子構造にする。
・検索キーワードは、できるだけ左詰めに書く。
・小学校高学年からお年寄りまで理解できる言葉で書く。
・できれば、具体的な数字を含める。
・見出しの文字数は30文字程度とする。
・記憶しておくのみで、まだ、出力は行わない。
5 以下の条件で、導入文の生成を行う。
#条件
導入文の作成条件
・ターゲットユーザーの疑問と回答をハッキリさせる。
・分かりやすく、簡単な文章とする。
・文字数は100~300文字程度とする。
・記事タイトルの後に記事全体の導入文を作成する。
・各見出しの後にタイトル毎の導入文を作成する。
・記憶しておくのみで、まだ、出力は行わない。
6 以下の条件で、各タイトル毎に記事本文を生成する。
#条件
記事本文作成の条件
・各タイトルの導入文の後に、タイトル毎の記事本文を作成する。
・記事に、検索キーワードを含める。
・ターゲットユーザーの必要性や重要性を想定し、記事を読むメリットが感じられる文章とする。
・ターゲットユーザーの検索意図に基づいた記事を作成する。
・読みやすい記事にする。
・正しい文法を使用する。
・結論から書く（PREP法を使う）
・語尾をそろえる（です・ます調をあわせる）
・箇条書きを有効に活用する。
・・記憶しておくのみで、まだ、出力は行わない。
7 生成したseo記事全体を以下の条件で出力する。
#条件
生成した記事内容を以下の順でまとめて出力する。
・タイトル
・記事全体の導入文
・生成した見出しと見出しごとの導入文を順番に出力する。
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""



st.title(" コピーライティング")
st.image("head.jpg")
st.write(f"前提条件は{system_prompt}")
st.write("前提に従い在宅ワークについてAIがコピーライティングします。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
