import pandas as pd
import ast

def process_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """处理JSON格式的客服推荐分析数据"""
    
    def parse_json(json_str):
        """解析JSON字符串并提取关键字段"""
        try:
            data = ast.literal_eval(json_str)
            return {
                '顾客情绪': data.get('顾客情绪', ''),
                '一级场景': data.get('一级场景', ''),
                '二级场景': data.get('二级场景', ''),
                '具体原因': data.get('具体原因', ''),
                '客服话术': data.get('客服话术', ''),
                '建议采纳话术': data.get('建议采纳话术', '')
            }
        except:
            return {
                '顾客情绪': '',
                '一级场景': '',
                '二级场景': '',
                '具体原因': '',
                '客服话术': '',
                '建议采纳话术': ''
            }

    # 解析JSON列并扩展为多个新列
    json_data = df[column].apply(parse_json).apply(pd.Series)
    df = pd.concat([df, json_data], axis=1)
    return df
