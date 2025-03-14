import streamlit as st
import pandas as pd
import json
from io import BytesIO
from config import SCRIPT_CONFIG as script_config

st.title('智能客服数据分析平台')
# 动态生成分析模式选项
analysis_modes = list(script_config.keys())
script_choice = st.radio("选择分析模式",
                       analysis_modes,
                       help="请根据数据内容选择分析类型（配置来自config.py）")

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
    
    # 执行数据分析可视化
    from processing_modules.analyzer import analyze_and_plot
    if 'output_fields' in config and len(config['output_fields']) > 0:
        if 'analysis_data' in config:
            analyze_and_plot(df, config['analysis_data'])
        else:
            st.error(f"配置错误：当前分析模式'{script_choice}'缺少analysis_data配置项")
        
        # 显示生成的图片
        st.subheader('分析结果可视化')
        cols = st.columns(2)  # 创建两列布局
        for i, field in enumerate(config['analysis_data']):
            img_path = f"static/images/{field}_distribution.png"
            with cols[i % 2]:  # 交替放入两列
                st.image(img_path, 
                        use_container_width=True,
                        caption=f"{field}分布图")
        
        # 添加自定义CSS样式
        st.markdown("""
        <style>
        .stImage > img {
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("未配置output_fields，跳过分析步骤")
    
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
