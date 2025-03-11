import pandas as pd

def process_data(df, json_column):
    """退货退款分析脚本"""
    def extract_json(json_str):
        try:
            data = eval(json_str)
            return (
                data.get("退款状态", ""),
                data.get("一级场景", ""),
                data.get("二级场景", ""),
                data.get("具体原因", ""),
                data.get("客服是否挽留", ""),
                data.get("建议客服接待策略", "")
            )
        except:
            return (None,)*6

    df[["退款状态", "一级场景", "二级场景", "具体原因", "客服是否挽留", "建议客服接待策略"]] = \
        df[json_column].apply(lambda x: pd.Series(extract_json(x)))
    
    return df
