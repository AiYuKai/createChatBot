# 以下を「app.py」に書き込み
import streamlit as st
import streamlit_authenticator as stauth

# ユーザ情報。引数
names = ['John Smith', 'Rebecca Briggs']  # 
usernames = ['jsmith', 'rbriggs']  # 入力フォームに入力された値と合致するか確認される
passwords = ['123', '456']  # 入力フォームに入力された値と合致するか確認される

# パスワードをハッシュ化。 リスト等、イテラブルなオブジェクトである必要がある
hashed_passwords = stauth.Hasher(passwords).generate()

# cookie_expiry_daysでクッキーの有効期限を設定可能。認証情報の保持期間を設定でき値を0とするとアクセス毎に認証を要求する
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
