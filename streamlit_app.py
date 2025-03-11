import streamlit as st
import pandas as pd
import json
from io import BytesIO

st.title('智能客服数据分析平台')

# 脚本选择器
script_choice = st.radio("选择分析模式", 
                       ("买家购买决策分析", "有效性回复分析", "退货退款分析", "非满分析"),
                       help="请根据数据内容选择分析类型")

# 动态配置参数
script_config = {
    "买家购买决策分析": {
        "module": "buyer_decision",
        "allowed_columns": ["deepseek-r1", "doubao-1.5-pro-32k","doubao-pro-32k"],
        "output_fields": ['顾客情绪', '一级原因', '二级原因', '具体原因', '客服亮点','建议客服接待策略']
    },
    "有效性回复分析": {
        "module": "reply_analysis",
        "allowed_columns": ["doubao-pro-32k", "doubao-1.5-pro-32k","deepseek-r1"],
        "output_fields": ['客户是否针对同一问题重复提问', '一级场景', '二级场景', '具体原因', '客服状态','建议客服接待策略']
    },
    "退货退款分析": {
        "module": "refund_analysis",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['退款状态', '一级场景', '二级场景', '具体原因', '客服是否挽留','建议客服接待策略']
    },
    "非满分析": {
        "module": "unsatisfied_analysis",
        "allowed_columns": ["doubao-pro-32k","doubao-1.5-pro-32k", "deepseek-r1"],
        "output_fields": ['销售阶段', '一级场景', '二级场景', '具体原因', '是否是客服的原因','建议客服接待策略']
    },
}
config = script_config[script_choice]
allowed_columns = config['allowed_columns']


# 动态导入处理模块
module = __import__(f"processing_modules.{config['module']}", fromlist=["process_data"])
process_data = module.process_data

# 文件上传组件
uploaded_file = st.file_uploader("上传数据文件", type=['csv', 'xlsx'], 
                               help=f"当前模式需要以下任一数据列: {', '.join(config['allowed_columns'])}")

if uploaded_file:
    # 读取数据并检测可用列
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
        # 自动识别可用数据列
        existing_columns = [col for col in allowed_columns if col in df.columns]
        if not existing_columns:
            st.error("文件需要包含以下任一数据列: " + " 或 ".join(allowed_columns))
            st.stop()
        current_column = existing_columns[0]
    except Exception as e:
        st.error(f"文件解析失败: {str(e)}")
        st.info(f"支持格式要求：\n1. CSV文件需使用UTF-8编码\n2. Excel文件需使用.xlsx格式\n3. 必须包含以下任一数据列: {', '.join(allowed_columns)}")
        st.stop()
    
    # 执行数据处理（传递当前使用的列）
    df = process_data(df, current_column)
    
    # 清理空值数据
    if df[current_column].isnull().any():
        invalid_count = df[current_column].isnull().sum()
        st.warning(f"发现{invalid_count}条无效数据，已自动过滤")
        df = df.dropna(subset=[current_column])
        
    # 可配置数据预览
    st.subheader('处理后的数据预览')
    # 动态调整预览行数
    preview_rows = st.slider('选择预览行数', 
                           min_value=1, 
                           max_value=min(50, len(df)), 
                           value=10,
                           help="可滑动选择1-50行进行数据预览")
    
    # 显示带分页的数据表格
    st.dataframe(df.head(preview_rows))
    
    # 显示数据统计信息
    st.info(f"数据总行数: {len(df)} 条 | 有效数据: {df[current_column].count()} 条 | 当前预览: {preview_rows} 行")
    
    # 创建内存中的Excel文件
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 动态选择输出列
        output_columns = ['contents', 'industry'] + config['output_fields']
        
        # 确保列名存在且数据不为空
        valid_columns = [col for col in output_columns if col in df.columns]
        if valid_columns:
            df[valid_columns].to_excel(writer, index=False, sheet_name='分析数据')
        else:
            # 创建空工作表作为保护机制
            pd.DataFrame(['无有效数据']).to_excel(writer, sheet_name='空数据', index=False)
    
    # 添加下载按钮
    st.download_button(
        label="下载Excel文件",
        data=output.getvalue(),
        file_name='processed_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
