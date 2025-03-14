import pandas as pd
import json

def process_data(df, json_column):
    """非满场景数据分析处理函数"""
    def extract_json(json_str):
        try:
            data = eval(json_str)
            return (
                data.get("销售阶段", ""),
                data.get("一级场景", ""),
                data.get("二级场景", ""),
                data.get("具体原因", ""),
                data.get("是否是客服的原因",""),
                data.get("建议客服接待策略", "")
            )
        except:
            return (None,)*6

    df[["销售阶段", "一级场景", "二级场景","具体原因","是否是客服的原因", "建议客服接待策略"]] = \
        df[json_column].apply(lambda x: pd.Series(extract_json(x)))
    
    return df

