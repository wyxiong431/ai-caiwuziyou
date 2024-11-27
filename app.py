from flask import Flask, render_template, request, jsonify
from markdown import markdown
from gpt import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """
    渲染 index.html 主页面。
    """
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    处理预测请求并返回 JSON 数据。
    """
    try:
        # 获取前端传来的 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({"error": "请求数据不能为空"}), 400

        # 提取数据，设置默认值
        user_input = data.get("user_input", "002777")
        user_prompt = data.get("user_prompt", "")
        user_bk = data.get("user_bk", "BK0737")

        # 调用函数生成预测结果
        prediction = markdown(caiwuziyou(user_input, user_prompt, user_bk))

        # 返回预测结果
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(ssl_context=("certificate.crt", "privatekey.key"), debug=True, port=8888, host="0.0.0.0")
