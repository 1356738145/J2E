import pandas as pd
import ast

def process_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """处理JSON格式的竞争数据"""
    
    def parse_json(json_str):
        """解析JSON字符串并提取关键字段"""
        try:
            data = ast.literal_eval(json_str)
            return {
                '竞争品牌': data.get('竞争品牌', ''),
                '一级标签': data.get('一级标签', ''),
                '二级标签': data.get('二级标签', ''),
                '具体原因': data.get('具体原因', ''),
                '客服解决力': data.get('客服解决力', ''),
                '建议客服接待策略': data.get('建议客服接待策略', '')
            }
        except:
            return {
                '竞争品牌': '',
                '一级标签': '',
                '二级标签': '',
                '具体原因': '',
                '客服解决力': '',
                '建议客服接待策略': ''
            }

    # 解析JSON列并扩展为多个新列
    json_data = df[column].apply(parse_json).apply(pd.Series)
    df = pd.concat([df, json_data], axis=1)
    return df
