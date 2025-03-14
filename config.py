# 动态配置参数
SCRIPT_CONFIG = {
    "买家购买决策分析": {
        "module": "buyer_decision",
        "allowed_columns": ["deepseek-r1", "doubao-1.5-pro-32k","doubao-pro-32k"],
        "output_fields": ['顾客情绪', '一级原因', '二级原因', '具体原因', '客服亮点','建议客服接待策略'],
        "analysis_data": ['顾客情绪', '一级原因', '二级原因', '客服亮点']
    },
    "有效性回复分析": {
        "module": "reply_analysis",
        "allowed_columns": ["doubao-pro-32k", "doubao-1.5-pro-32k","deepseek-r1"],
        "output_fields": ['客户是否针对同一问题重复提问', '一级场景', '二级场景', '具体原因', '客服状态','建议客服接待策略'],
        "analysis_data": ['客户是否针对同一问题重复提问', '一级场景', '二级场景', '客服状态']
    },
    "退货退款分析": {
        "module": "refund_analysis",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['退款状态', '一级场景', '二级场景', '具体原因', '客服是否挽留','建议客服接待策略'],
        "analysis_data": ['退款状态', '一级场景', '二级场景', '客服是否挽留']
    },
    "非满分析": {
        "module": "unsatisfied_analysis",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['销售阶段', '一级场景', '二级场景', '具体原因', '是否是客服的原因','建议客服接待策略'],
        "analysis_data": ['销售阶段', '一级场景', '二级场景', '是否是客服的原因']
    },
    "买家流失分析": {
        "module": "buyer_lost",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['未购原因', '具体原因', '细分原因', '原因总结', '是否是客服的原因','建议客服接待策略'],
        "analysis_data": ['未购原因', '具体原因', '细分原因', '是否是客服的原因']
    },
    "竞争对比分析":{
        "module": "challenger",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['竞争品牌', '一级标签', '二级标签', '具体原因', '客服解决力','建议客服接待策略'],
        "analysis_data": ['竞争品牌', '一级标签', '二级标签', '客服解决力'] 
    },
    "客服商品推荐分析":{
        "module": "recommand",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['顾客情绪', '一级场景', '二级场景', '具体原因', '客服话术','建议采纳话术'],
        "analysis_data": ['顾客情绪', '一级场景', '二级场景', '客服话术'] 
    }
}
