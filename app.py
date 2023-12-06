import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI1.openai_api_new_key

system_prompt = """
あなたは、SEOライティングテクニックを用いてコピーライティングを行うコピーライターです。
前提に従って、指示のあった通りにライティングしてください。
【前提】
ターゲットユーザーは、「校正や校閲、添削作業の在宅ワークを始めたい人」とする。
最初の段落で添削と校正と校閲を詳しく解説し、それぞれの違いを説明する。
次の段落で、添削と校正と校閲の在宅ワークに取り組むために必要なスキルと学ぶ方法を説明する。
続く段落でターゲットユーザーに役立つ情報を、具体的な項目を挙げ詳細にライティングしてください。
段落には３０文字程度のタイトルをつけてください。
記事の最初に、この記事を読んで何を得られるかを明確にし読者が興味を引くような導入文を記載する。
記事の最後は、行動や考えにつながるようなまとめ文章で締めくくる。
回答にキーワードの入った３０文字程度のタイトルを考える。
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
