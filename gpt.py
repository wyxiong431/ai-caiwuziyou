from openai import OpenAI
from stockapi.stock_api_history import *
from stockapi.stock_api_real_time import *
from stockapi.util import *
import httpx
import config

api_token = config.API_TOKEN
secret_key = config.SECRET_KEY

proxies = {
    "http://": 'http://127.0.0.1:7890',
    "https://": 'http://127.0.0.1:7890',
    "socks5://": 'socks5://127.0.0.1:7891',
}

http_client = httpx.Client(proxies=proxies)

client = OpenAI(api_key=api_token, http_client=http_client)
# client = OpenAI(api_key=api_token)

def ask_gpt(data, user_prompt):
    prompt = f'{data}'
    if not is_today():
        sys_prompt = '''
你是一个A股价值投资专家，擅长通过股票的历史数据预测下一交易日的股价走势，并提供投资建议。股票数据将包含在 `<data/>` 标签内。
# 任务步骤
1. 深入分析提供的提供的数据，找到数据趋势和规律，并分析走势。
2. 通过历史数据预测下一交易日的相关股价走势，包括开盘价、区间、收盘价。
3. 提供明确的买卖策略建议，包括：日内投资、短线投资、中线投资。
4. 注意中国股市设涨跌停，并且是T+1操作。

# 输出格式
请以清晰、简洁的文本形式输出结果。
            '''
    else:
        sys_prompt = '''
你是一个A股价值投资专家，擅长通过股票的历史数据结合今日已经产生的1分钟k线，提出今日的投资建议。股票数据将包含在 `<data/>` 标签内。
# 任务步骤
1. 深入分析提供的数据，找到数据趋势和规律，并分析今日走势。
2. 提供明确的买卖策略建议，包括今日是否博弈，博弈点，仓位，止损点。
3. 注意中国股市设涨跌停，并且是T+1操作，上午9点30开盘，11点30收盘，下午1点开盘，3点收盘。

# 输出格式
请以清晰、简洁的文本形式输出结果。
            '''
    # client.base_url='http://121.43.97.233:5000/api/v1'
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": f"<data>{prompt}</data>;{user_prompt}"}]
    )
    print(response)
    content = response.choices[0].message.content;
    return content


def create_data(code, start_date, user_bk):
    calculation_cycle = 100  # 100-日，101-周，102-月
    index_code = code

    end_date = get_end_date()  # 结束日期
    ma_periods = "5,10,20,30"  # MA 周期
    #kdj
    cycle = 9  # 默认周期
    cycle1 = 3  # 周期1
    cycle2 = 3  # 周期2
    #macd
    long_cycle = 26  # 长期周期
    short_cycle = 12  # 短期周期

    data = f"股票代码{code}\n";
    data += "\n 历史日线数据：\n"
    data += "\n".join(map(str,query_day_kline(index_code, start_date, end_date, calculation_cycle)))
    data += "\n 历史rsi数据：\n"
    data += "\n".join(map(str,query_rsi_data(index_code, start_date, end_date, calculation_cycle)))
    data += "\n 历史ma数据：\n"
    data += "\n".join(map(str,query_ma_data(index_code, start_date, end_date, ma_periods, calculation_cycle)))

    data += "\n 历史kdj数据：\n"
    data += "\n".join(map(str,query_kdj_data(index_code, start_date, end_date, calculation_cycle, cycle, cycle1, cycle2)))

    data += "\n 历史macd数据：\n"
    data += "\n".join(map(str,query_macd_data(index_code, start_date, end_date, calculation_cycle, long_cycle, short_cycle)))
    data += "\n 历史市场板块数据：\n"
    data += "\n".join(map(str,query_day_kline(user_bk, start_date, end_date)))

    if is_today():
        data += "\n 今日股票1分钟k线：\n"
        data += "\n".join(map(str, query_index_realtime_kline(index_code)))
        data += "\n 今日股票1分钟kdj：\n"
        data += "\n".join(map(str, query_realtime_kdj(index_code)))
        data += "\n 今日股票1分钟MACD：\n"
        data += "\n".join(map(str, query_realtime_macd(index_code)))

    return data

def caiwuziyou(code, user_prompt, user_bk):
    if is_today():
        start_date = "2024-11-01"  # 开始日期
    else:
        start_date = "2024-11-01"  # 开始日期
    data = create_data(code, start_date, user_bk)
    print(data)
    return ask_gpt(data, user_prompt)
