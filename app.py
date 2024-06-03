# 以下を「app.py」に書き込み
import streamlit as st
import streamlit_authenticator as stauth
import openai

# APIキーの設定
# streamlit community cloudの「secrets」からopenAI API keyを取得 ←公開したくない情報をシークレットに格納することができる
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# modelの設定
model="gpt-3.5-turbo-1106"

#########################################################
# ユーザ情報。引数
names = ['John Smith', 'Rebecca Briggs']  # 
usernames = ['jsmith', 'rbriggs']  # 入力フォームに入力された値と合致するか確認される
passwords = ['123', '456']  # 入力フォームに入力された値と合致するか確認される

# パスワードをハッシュ化。 リスト等、イテラブルなオブジェクトである必要がある
hashed_passwords = stauth.Hasher(passwords).generate()

# cookie_expiry_daysでクッキーの有効期限を設定可能。認証情報の保持期間を設定でき値を0とするとアクセス毎に認証を要求する
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
#########################################################

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
########### mainチャットページ関数 ##########
def main_page(userName):
  st.write('ようこそ *%s*' % (userName))
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

########## ユーザーログインページ ##########
# ログインメソッドで入力フォームを配置
name, authentication_status, username = authenticator.login('Login', 'main')

# 返り値、authenticaton_statusの状態で処理を場合分け
if authentication_status:
    # logoutメソッドでaurhenciationの値をNoneにする
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
