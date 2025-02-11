# import os
import openai
import json
import requests


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

def get_area_code(area_name):
    """指定されたエリア名称からエリアコードを取得・返却する。

    Args:
        area_name エリア名称（e.g. 神奈川県）

    Returns:
        str: 予報区コード
    """

    # 気象庁 予報区コードの一覧
    url = "https://www.jma.go.jp/bosai/common/const/area.json"
    response = requests.get(url)
    data = json.loads(response.text)

    # 取得データより引数で指定されたコードを探索
    for code, info in data["offices"].items():
        if info["name"] == area_name:
            return code
    return None   # Not found


def get_current_weather(location):
    """指定されたエリア名称からエリアコードを取得・返却する。

    Args:
        location エリア名称（e.g. 神奈川県）

    Returns:
        str: 予報区コード
    """

    # 気象庁の予報区コードを調べる。
    area_code = get_area_code(location)

    overview = ""
    if area_code is None:
        # return json.dumps({"error": "location not found"})
        overview = "その地域の予報は分かりませんでした。"
    else:
        # 情報取得
        url = f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{area_code}.json"
        response = requests.get(url)
        data = json.loads(response.text)
        overview = data["text"]

    # return json.dumps({"location": location, "overview": overview})
    return overview


def get_current_weather_info(client):
    """Function callingを使用して指定エリアの天気を返却する。

    Args:
        client (OpenAI): OpenAIクラスインスタンス

    Returns:
        str: 回答文字列
    """
    
    # Debug
    # location = "熊本県"
    # area_code = get_area_code(location)
    # print(location, area_code)
    # overview = get_current_weather(location)
    # print(overview)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. 神奈川県",
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    messages = [
        {"role": "user", "content": "熊本県の天気は？"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,    # 以前は functions であったもの（functionsは非推奨）
    )

    # print(response.to_json(indent=2))

    # レスポンスに tool_calls という要素があり、
    # 「get_current_weatherを、こんな引数で実行したい」という内容のが書かれている。
    # LLMが、この質問を答えるには、get_current_weatherを
    # 「{“location”: “熊本県”}」という引数で実行する必要がある。と判断している。

    # 会話履歴を追加する。
    response_message = response.choices[0].message
    messages.append(response_message.to_dict())

    # 利用可能な関数群
    available_functions = {
        "get_current_weather": get_current_weather,
    }

    # 関数群に対するループ
    for tool_call in response_message.tool_calls:
        # 関数を実行
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            location=function_args.get("location"),
        )
        # print(function_response)

        # 関数の実行結果を会話履歴としてmessagesに追加
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )

    # print(json.dumps(messages, ensure_ascii=False, indent=2))
    second_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    # print(second_response.to_json(indent=2))

    return second_response.to_json(indent=2)


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

    # # 指定画像の説明を返却する。
    # res_desc_of_img = get_description_of_image(client)
    # print(res_desc_of_img)

    # # 指定画像（ローカル）の説明を返却する。
    # res_desc_of_localimg = get_description_of_localimage(client)
    # print(res_desc_of_localimg)

    # 指定エリアの天気予報を返却する。
    res_current_weather = get_current_weather_info(client)
    print(res_current_weather)


if __name__ == '__main__':
    main()
