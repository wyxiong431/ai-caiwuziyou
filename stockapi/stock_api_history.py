import requests
import config

token = config.SECRET_KEY
def query_day_kline(code, start_date, end_date, calculation_cycle=100):
    """
    查询 A 股股票历史行情数据并解析返回数据

    :param code: 股票代码，如 600004；板块代码如 BK0733
    :param start_date: 开始日期，格式 YYYY-MM-DD
    :param end_date: 结束日期，格式 YYYY-MM-DD
    :param calculation_cycle: 周期，100-日，101-周，102-月
    :return: 解析后的历史行情数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/base/day"
    params = {
        "token": token,
        "code": code,
        "startDate": start_date,
        "endDate": end_date,
        "calculationCycle": str(calculation_cycle),
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
                "日期": entry.get("time", "N/A"),
                "开盘价": entry.get("open", "N/A"),
                "最高价": entry.get("high", "N/A"),
                "最低价": entry.get("low", "N/A"),
                "收盘价": entry.get("close", "N/A"),
                "成绩额": entry.get("amount", "N/A"),
                "换手率": entry.get("turnoverRatio", "N/A"),
                # "成交量": entry.get("volume", "N/A"),
                # "均价": entry.get("avgPrice", "N/A"),
                # "涨跌": entry.get("change", "N/A"),
                # "总股本": entry.get("totalShares", "N/A"),
                "涨跌幅": entry.get("changeRatio", "N/A"),
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def query_macd_data(code, start_date, end_date, calculation_cycle=100, long_cycle=26, short_cycle=12):
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
    url = "https://stockapi.com.cn/v1/quota/macd2"
    params = {
        "code": code,
        "token": token,
        "startDate": start_date,
        "endDate": end_date,
        "calculationCycle": str(calculation_cycle),
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
                "日期": dates[i],
                "DEA": dea_values[i] if i < len(dea_values) else "N/A",
                "DIFF": dif_values[i] if i < len(dif_values) else "N/A",
                "MACD": macd_values[i] if i < len(macd_values) else "N/A",
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def query_kdj_data(code, start_date, end_date, calculation_cycle=100, cycle=9, cycle1=3, cycle2=3):
    """
    查询日、周、月线 KDJ 数据

    :param code: 股票代码、板块代码或概念代码，如 601088
    :param start_date: 开始日期，格式 YYYY-MM-DD
    :param end_date: 结束日期，格式 YYYY-MM-DD
    :param calculation_cycle: 周期，100-日，101-周，102-月
    :param cycle: 默认周期，默认 9
    :param cycle1: 周期1，默认 3
    :param cycle2: 周期2，默认 3
    :return: 解析后的 KDJ 数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/quota/kdj2"
    params = {
        "code": code,
        "token": token,
        "startDate": start_date,
        "endDate": end_date,
        "calculationCycle": str(calculation_cycle),
        "cycle": str(cycle),
        "cycle1": str(cycle1),
        "cycle2": str(cycle2),
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
                "日期": dates[i],
                "K": k_values[i] if i < len(k_values) else "N/A",
                "D": d_values[i] if i < len(d_values) else "N/A",
                "J": j_values[i] if i < len(j_values) else "N/A",
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def query_rsi_data(code, start_date, end_date, calculation_cycle=100, cycle1=6, cycle2=12, cycle3=24):
    """
    查询日、周、月线 RSI 数据

    :param code: 股票代码、板块代码或概念代码，如 601088
    :param start_date: 开始日期，格式 YYYY-MM-DD
    :param end_date: 结束日期，格式 YYYY-MM-DD
    :param calculation_cycle: 周期，100-日，101-周，102-月
    :param cycle1: RSI 周期1，默认 6
    :param cycle2: RSI 周期2，默认 12
    :param cycle3: RSI 周期3，默认 24
    :return: 解析后的 RSI 数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/quota/rsi2"
    params = {
        "code": code,
        "token": token,
        "startDate": start_date,
        "endDate": end_date,
        "calculationCycle": str(calculation_cycle),
        "cycle1": str(cycle1),
        "cycle2": str(cycle2),
        "cycle3": str(cycle3),
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
        rsi1_values = data.get("rsi1", [])
        rsi2_values = data.get("rsi2", [])
        rsi3_values = data.get("rsi3", [])

        for i in range(len(dates)):
            parsed_data.append({
                "日期": dates[i],
                "RSI1": rsi1_values[i] if i < len(rsi1_values) else "N/A",
                "RSI2": rsi2_values[i] if i < len(rsi2_values) else "N/A",
                "RSI3": rsi3_values[i] if i < len(rsi3_values) else "N/A",
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    code = "002777"  # 股票代码，如中国神华
    start_date = "2024-11-09"  # 开始日期
    end_date = "2024-11-22"  # 结束日期
    calculation_cycle = 100  # 100-日，101-周，102-月
    cycle1 = 6  # 周期1
    cycle2 = 12  # 周期2
    cycle3 = 24  # 周期3

    result = query_rsi_data(code, start_date, end_date, calculation_cycle, cycle1, cycle2, cycle3)

    if "error" in result:
        print("Error:", result["error"])
    else:
        print("RSI 数据:")
        for entry in result:
            print(entry)

def query_ma_data(code, start_date, end_date, ma_periods="5,10,20,30", calculation_cycle=100):
    """
    查询日、周、月线 MA 均线数据

    :param code: 股票代码、板块代码或概念代码，如 601088
    :param start_date: 开始日期，格式 YYYY-MM-DD
    :param end_date: 结束日期，格式 YYYY-MM-DD
    :param ma_periods: MA 周期，多个周期用英文逗号分隔，如 "5,10,20"
    :param calculation_cycle: 周期，100-日，101-周，102-月
    :return: 解析后的 MA 数据或错误信息
    """
    url = "https://stockapi.com.cn/v1/quota/ma2"
    params = {
        "token": token,
        "code": code,
        "startDate": start_date,
        "endDate": end_date,
        "ma": ma_periods,
        "calculationCycle": str(calculation_cycle),
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
        dates = data.get("date", [])
        parsed_data = []
        ma_keys = [f"ma{period}" for period in map(str.strip, ma_periods.split(","))]

        for i, date in enumerate(dates):
            ma_values = {key: data.get(key, [])[i] if i < len(data.get(key, [])) else "N/A" for key in ma_keys}
            parsed_data.append({
                "日期": date,
                **ma_values
            })

        return parsed_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}



