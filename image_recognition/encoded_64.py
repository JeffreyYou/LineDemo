import base64
import os
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f

def read_img(image_path):
    """

    :param image_path:
    :return:
    """
    print("Reading Image:", image_path)
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "请读取这张图片"
                      "先判断它是不是一张证券交易的截图，如果不是，描述下它是什么然后结束，如果是交易截图则说'这是一张交易截图'并且按照以下格式回答问题"
                      "显示时间____"
                      "网页标题为_____，是一家____公司。"
                      "如果屏幕中有横幅则说：屏幕的横幅中提到了“_____”这意味着_____"
                      "中间的部分显示了股票交易的详细信息，包括：_____"
                      "订单号码：____"
                      "状态：_____"
                      "股票名称与代码：_____"
                      "买卖类型:_____"
                      "成交数量:_____"
                      "成交单价:_____"
                      "成交日期:_____"
                      "结算日期:_____"
                      "合计金额:_____"
                      "手数料（手续费）：_____"
                      "成交时间：_____"
                      "如果底部有煮食，则说：底部有一个注释:_____"
                      "如果底部有网址，则说：页面底部有_____的网址：_____"

            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    res = response.json()['choices'][0]['message']['content']
    print(res)
    print('\n')



if __name__ == "__main__":
    path = '/Users/derafael/Desktop/2lab3/mixed_data'
    #lst = findAllFile(path)
    for img in findAllFile(path):
        print(img)
        read_img(path + '/' + img)