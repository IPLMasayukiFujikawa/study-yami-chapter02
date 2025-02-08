# import os
import openai


def main():
    # # 環境変数からAPIキーを取得
    # コンストラクタで指定不要なら取得不要
    # api_key = os.getenv("OPENAI_API_KEY")

    # OpenAI クライアントの作成
    # パラメータとして指定する必要があるかどうか？
    # OPENAI_API_KEY に正しいキーが指定されていればOKか？
    # client = openai.OpenAI(api_key=api_key)
    client = openai.OpenAI()

    # API呼び出し用のメッセージ
    # contentに質問文字列を設定する。
    messages = [
        {"role": "user", "content": "東京の天気はどうですか？"}
    ]

    # OpenAI APIを使ってテキスト生成
    # 簡単な返答を求める（消費したくない）なら、トークン数は10〜50ぐらい
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=50  # 生成するトークン数（単語数ではなくトークン数）
    )

    # 結果を表示
    print(response.choices[0].message.content.strip())


if __name__ == '__main__':
    main()
