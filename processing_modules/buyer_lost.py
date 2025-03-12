import pandas as pd
import ast

def process_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """处理JSON格式的买家流失数据"""
    
    def parse_json(json_str):
        """解析JSON字符串并提取关键字段"""
        try:
            data = ast.literal_eval(json_str)
            return {
                '未购原因': data.get('未购原因', ''),
                '具体原因': data.get('具体原因', ''),
                '细分原因': data.get('细分原因', ''),
                '原因总结': data.get('原因总结', ''),
                '是否是客服的原因': data.get('是否是客服的原因', False),
                '建议客服接待策略': data.get('建议客服接待策略', '')
            }
        except:
            return {
                '未购原因': '',
                '具体原因': '',
                '细分原因': '',
                '原因总结': '',
                '是否是客服的原因': False,
                '建议客服接待策略': ''
            }

    # 解析JSON列并扩展为多个新列
    json_data = df[column].apply(parse_json).apply(pd.Series)
    df = pd.concat([df, json_data], axis=1)
    return df
