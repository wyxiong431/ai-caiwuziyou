import requests
import json


token = '18255e67301d178a9bb17661933c55a0895154078885110d'

#获取1分钟k线
def query_index_realtime_kline(index_code, return_all=1):
    """
    查询指数每分钟实时K线数据

    :param index_code: 指数代码，000001（上证指数）、399001（深证成指）、399006（创业板指）
    :param return_all: 是否返回全部数据，1-返回全部数据，0-仅返回最近一条
    :return: JSON 响应数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/base/index/mink"
    params = {
        "token": token,
        "code": index_code,
        "all": str(return_all)
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果发生 HTTP 错误，抛出异常
        response_json = response.json()

        if response_json.get("code") != 20000:
            return {"error": response_json.get("msg", "Unknown error")}

        data = response_json.get("data", [])
        parsed_data = []
        for entry in data:
            parsed_data.append({
                "时间": entry.get("time", "N/A")[11:],
                "开": entry.get("open", "N/A"),
                "最高价": entry.get("high", "N/A"),
                "最低价": entry.get("low", "N/A"),
                "收": entry.get("close", "N/A"),
                "成交量": entry.get("volume", "N/A"),
                "成交额": entry.get("amount", "N/A"),
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def query_realtime_transaction_volume(code, return_all=1):
    """
    查询分时成交量数据并解析返回数据

    :param code: 股票代码，如 601088
    :param return_all: 是否返回全部数据，1-返回全部数据，0-仅返回最近一条
    :return: 解析后的分时成交量数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/base/min"
    params = {
        "token": token,
        "code": code,
        "all": str(return_all),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果发生 HTTP 错误，抛出异常
        response_json = response.json()

        if response_json.get("code") != 20000:
            return {"error": response_json.get("msg", "Unknown error")}

        data = response_json.get("data", [])
        parsed_data = []
        for entry in data:
            parsed_data.append({
                "时间": entry.get("time", "N/A"),
                "价格": entry.get("price", "N/A"),
                "手数": entry.get("shoushu", "N/A"),
                "单数": entry.get("danShu", "N/A"),
                "成交额": round(float(entry.get("shoushu", "N/A")) * float(entry.get("price", "N/A"))),
                "涨跌": entry.get("bsbz", "N/A"),
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def query_realtime_kdj(code):
    """
    查询分时成交量数据并解析返回数据

    :param code: 股票代码，如 601088
    :param return_all: 是否返回全部数据，1-返回全部数据，0-仅返回最近一条
    :return: 解析后的分时成交量数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/base/minKdj"
    params = {
        "code": code,
        "token": token,
        "cycle": str(9),
        "cycle1": str(3),
        "cycle2": str(3),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果发生 HTTP 错误，抛出异常
        response_json = response.json()

        if response_json.get("code") != 20000:
            return {"error": response_json.get("msg", "Unknown error")}

        data = response_json.get("data", {})
        if not data:
            return {"error": "No data available"}

        # 解析数据
        parsed_data = []
        dates = data.get("date", [])
        k_values = data.get("k", [])
        d_values = data.get("d", [])
        j_values = data.get("j", [])

        for i in range(len(dates)):
            parsed_data.append({
                "时间": dates[i][11:],
                "K": k_values[i] if i < len(k_values) else "N/A",
                "D": d_values[i] if i < len(d_values) else "N/A",
                "J": j_values[i] if i < len(j_values) else "N/A",
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def query_realtime_macd(code, long_cycle=26, short_cycle=12):
    """
    查询日、周、月线 MACD 数据

    :param code: 股票代码、板块代码或概念代码，如 601088
    :param start_date: 开始日期，格式 YYYY-MM-DD
    :param end_date: 结束日期，格式 YYYY-MM-DD
    :param calculation_cycle: 周期，100-日，101-周，102-月
    :param long_cycle: 长期周期，默认 26
    :param short_cycle: 短期周期，默认 12
    :return: 按日期解析的 MACD 数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/base/minMacd"
    params = {
        "code": code,
        # "token": token,
        "longCycle": str(long_cycle),
        "shortCycle": str(short_cycle),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果发生 HTTP 错误，抛出异常
        response_json = response.json()

        if response_json.get("code") != 20000:
            return {"error": response_json.get("msg", "Unknown error")}

        data = response_json.get("data", {})
        if not data:
            return {"error": "No data available"}

        # 解析数据
        parsed_data = []
        dates = data.get("date", [])
        dea_values = data.get("dea", [])
        dif_values = data.get("dif", [])
        macd_values = data.get("macd", [])

        for i in range(len(dates)):
            parsed_data.append({
                "时间": dates[i][11:],
                "DEA": round(dea_values[i],4) if i < len(dea_values) else "N/A",
                "DIFF": round(dif_values[i],4) if i < len(dif_values) else "N/A",
                "MACD": round(macd_values[i],4) if i < len(macd_values) else "N/A",
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def query_realtime_bk(code):
    # SSE 流式传输接口 URL
    url = f"https://77.push2.eastmoney.com/api/qt/stock/trends2/sse?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f17&fields2=f51,f52,f53,f54,f55,f56,f57,f58&mpi=1000&ut=fa5fd1943c7b386f172d6893dbfba10b&secid=90.{code}&ndays=1&iscr=0&iscca=0"
    # 启动请求，获取 SSE 流式数据
    with requests.get(url, stream=True)as response:# 确保请求成功
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    # Extract the JSON part of the string
                    json_part = line_str.split('data: ', 1)[1]

                    # Load the JSON data
                    data = json.loads(json_part)

                    # Parse and convert the trends to JSON array
                    trends_raw = data['data']['trends']
                    trends_parsed = [
                        {
                            "时间": trend.split(",")[0][11:],
                            "开盘": float(trend.split(",")[1]),
                            "最高": float(trend.split(",")[2]),
                            "最低": float(trend.split(",")[3]),
                            "收盘": float(trend.split(",")[4]),
                            "成交量": int(trend.split(",")[5]),
                            "成交额": float(trend.split(",")[6])
                            # "评价价": float(trend.split(",")[7])
                        }
                        for trend in trends_raw
                    ]
                    return trends_parsed
                    break
        else:
            print(f"错误{response.status_code}")

