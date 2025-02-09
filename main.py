# import os
import openai


def get_wheather(client):
    """東京の天気を回答として返却する。

    Args:
        client (OpenAI): OpenAIクラスインスタンス

    Returns:
        str: 回答文字列
    """
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
    return response.choices[0].message.content.strip()


def get_charactors(client):
    """質問の登場人物を返却する。

    Args:
        client (OpenAI): OpenAIクラスインスタンス

    Returns:
        str: 回答文字列
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": '人物一覧を次のJSON形式で出力してください。¥n{"people"}: ["aaa", "bbb¥]}',
            },
            {
                "role": "user",
                "content": "昔々あるところにおじいさんとおばあさんがいました。"
            },
        ],
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


def get_description_of_image(client):
    """指定画像の説明を返却する。

    Args:
        client (OpenAI): OpenAIクラスインスタンス

    Returns:
        str: 回答文字列
    """
    image_url = "https://as2.ftcdn.net/v2/jpg/01/11/12/43/1000_F_111124309_EDL2btGKhiqXBFW2H8tXQuqDdl4JJPyO.jpg"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "画像を説明してください。"},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            },
        ],
    )

    return response.choices[0].message.content


# def get_description_of_localimage(client):
#     """指定画像（ローカル）の説明を返却する。

#     Args:
#         client (OpenAI): OpenAIクラスインスタンス

#     Returns:
#         str: 回答文字列
#     """
#     # ローカル画像ファイルのパス
#     image_path = "/Users/m.fujikawa/Pictures/202411_ウォーキング/IMG_1137.png"

#     # 画像ファイルを開いてリクエストに添付
#     with open(image_path, "rb") as image_file:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "画像を説明してください。"},
#                         {"type": "image_file", "image_file": image_file},
#                     ],
#                 },
#             ],
#         )

#     return response.choices[0].message.content


def main():
    """メインエントリポイント
    """
    # OpenAI クライアントの作成
    # 環境変数 OPENAI_API_KEY にキーを指定しておくこと。
    client = openai.OpenAI()

    # # 東京の天気を返却する。
    # res_wheather = get_wheather(client)
    # print(res_wheather)

    # # 登場人物を返却する。
    # res_charactors = get_charactors(client)
    # print(res_charactors)

    # 指定画像の説明を返却する。
    res_desc_of_img = get_description_of_image(client)
    print(res_desc_of_img)

    # # 指定画像（ローカル）の説明を返却する。
    # res_desc_of_localimg = get_description_of_localimage(client)
    # print(res_desc_of_localimg)


if __name__ == '__main__':
    main()
