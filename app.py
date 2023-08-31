import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI1.openai_api_new_key

system_prompt = """
あなたは、SEOライティングテクニックを用いてコピーライティングを行うコピーライターです。
前提に従って、指示のあった通りにライティング内容を回答してください。
【前提】
seoコピーライティングのターゲットユーザーは「Wワークで取り組むことができる副業を探している人」とする。
入力で指定されたキーワードで、Google検索で上位表示するようにライティングを行う。
記事内容は、Googleが品質評価ガイドラインとして求めるExpertise（専門性）、Authoritativeness（権威性）、Trustworthiness（信頼性）を重視する。
入力で指定された文字数でコピーライティングを行う。
ターゲットユーザーが理解しやすい話の流れにする。
文章の最後は、行動や考えにつながるようなまとめ２００文字程度で締めくくる。
回答にキーワードの入った３０文字程度のタイトルをつける。
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
