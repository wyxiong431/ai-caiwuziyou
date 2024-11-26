# package/__init__.py

# 列出所有需要自动导入的模块
__all__ = ['stock_api_real_time', 'stock_api_history']

# 自动导入所有模块
from . import stock_api_real_time
from . import stock_api_history
