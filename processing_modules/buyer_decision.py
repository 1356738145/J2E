import pandas as pd

def process_data(df, json_column):
    """处理买家购买决策逻辑"""
    def extract_json(json_str):
        try:
            data = eval(json_str)
            return (
                data.get('顾客情绪', None),
                data.get('一级原因', None),
                data.get('二级原因', None),
                data.get('具体原因', None),
                data.get('客服亮点', None),
                data.get('建议客服接待策略', None)
            )
        except:
            return (None,)*6

    df[['顾客情绪', '一级原因', '二级原因', '具体原因', '客服亮点','建议客服接待策略']] = \
        df[json_column].apply(lambda x: pd.Series(extract_json(x)))
    
    return df
