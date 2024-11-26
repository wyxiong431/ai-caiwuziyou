from flask import Flask, render_template, request
from markdown import markdown
from gpt import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result_md = ""
    if request.method == "POST":
        user_input = request.form.get("user_input", "002777")
        user_prompt = request.form.get("user_prompt", "")
        user_bk = request.form.get("user_bk", "BK0737")
        # 在这里处理输入并生成 Markdown 格式的输出
        result_md = markdown(caiwuziyou(user_input, user_prompt, user_bk))

    return render_template("index.html", result_md=result_md)

if __name__ == "__main__":
    app.run(ssl_context=("certificate.crt", "privatekey.key"), debug=True, port=8888)
