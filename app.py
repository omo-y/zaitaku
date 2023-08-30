import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI1.openai_api_new_key

system_prompt = """
このスレッドの全ての質問に対して以下のルールに厳格に従って答えてください。
1. タロットカードの大アルカナをランダムに選択してください
2. さらに、正位置と逆位置もランダムに選択してください。 
3. 質問に対して、1 と 2 でランダムに選ばれた内容を踏まえて回答してください。
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
st.image("06_fortunetelling.png")
st.write(f"前提条件は以下、
         {system_prompt}")
st.write("前提に従い在宅ワークについてAIがコピーライティングします。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
