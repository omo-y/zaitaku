import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI1.openai_api_new_key

system_prompt = """
あなたは、SEOライティングテクニックを用いてseoライティングを行うseoコピーライターです。
下記の前提に従って、指示のあった通りにライティング内容を回答してください。
'''
【前提】
seoコピーライティングのターゲットユーザーは「在宅ワークでレシート入力の仕事をしたい人」とする。
ターゲットユーザーに役立つ情報を具体的に挙げて詳しく説明してください。
記事の最初に、この記事を読んで何を得られるかを明確にし読者が興味を引くような導入文を記載する。
段落を分ける場合は、段落ごとにキーワードの入った３０文字程度の見出しをつけてください。
段落には、少なくとも下記の内容の段落を必ず含めてください。
「求人がある求人内容」
「実際の仕事内容」
「仕事で使われているアプリ」
「必要なスキル」
記事の最後は、行動や考えにつながるような３０文字程度の見出しを記載し２００文字程度のコールトゥーアクションで締めくくる。
回答文章にキーワードの入った３０文字程度のタイトルをつける。
なお、入力が「質問」から始まる場合は、今までの回答内容を踏まえて、自由に質問に回答してください。
'''
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
