# 以下を「app.py」に書き込み
import streamlit as st
import streamlit_authenticator as stauth
import openai

# APIキーの設定
# streamlit community cloudの「secrets」からopenAI API keyを取得 ←公開したくない情報をシークレットに格納することができる
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# modelの設定
model="gpt-3.5-turbo-1106"

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

# チャットボットとやりとりする関数
def communicate() -> openai.types.chat.chat_completion.ChatCompletion:
    # ユーザの入力情報を格納
    messages = st.session_state["messages"]
    user_message = {"role": "user", "content": st.session_state["user_input"]}

    messages.append(user_message)

    # ChatGPTからの返答を取得
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
      temperature = 0,
      seed = 0
    )
    # openaiライブラリのバージョン変更に伴い、文字列としてresponseされてしまうため、扱いやすいようにdictとして格納する
    chat_completion_message = response.choices[0].message
    gpt_return_dict = {'role': chat_completion_message.role,'content': chat_completion_message.content}
    messages.append(gpt_return_dict)
    st.session_state["user_input"] = ""  # 入力欄を消去
    return messages

# ユーザーインターフェイスの構築
def main_page(userName):
    st.title("My AI Assistant")
    st.write("ChatGPT APIを使ったチャットボットです。")
    
    user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
    
    if st.session_state["messages"]:
        messages = st.session_state["messages"]
    
        for message in reversed(messages[1:]):  # 直近のメッセージを上に
            if message["role"]=="user":
              speaker = "🙂"
            elif message["role"]=="assistant":
              speaker="🤖"
    
            # 出力する
            st.write(speaker + ": " + message["content"])
# streamlitページの構築
password = st.text_input("パスワード", type="password")
stLoginpass = st.secrets.loginpass.login_pass
if password == stLoginpass:
    main_page()
else:
    st.error("アクセスが拒否されました。")
