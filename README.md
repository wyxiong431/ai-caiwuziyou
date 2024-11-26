# 该项目仅用于学习，不构成投资建议 
-------

## 运行
1. 安装requirements.txt
2. 运行app.py
3. 访问8888端口

*** 注意 ***

1. 如果不用ssl，请去掉app中ssl_context=("certificate.crt", "privatekey.key")，如果要使用，自己生成相关文件，放在根目录
2. config.py中配置openai的key和stockapi的token
3. 因为openai需要科学上网，请在gpt.py中配置代理