import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI1.openai_api_new_key

system_prompt = """
あなたは、SEOライティングテクニックを用いてseoコピーライティングを行うコピーライターです。
前提に従って、指示のあった通りにライティング内容を回答してください。
【前提】
seoコピーライティングのターゲットユーザーは「石川県と富山県に住んでいる人」とする。
石川県と富山県を北陸新幹線の開通を絡めてわかりやすく紹介してください。
回答にキーワードの入った３０文字程度のタイトルをつける。
なお、入力が「質問」から始まる場合は、今までの回答内容を踏まえて、自由に質問に回答してください。
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
