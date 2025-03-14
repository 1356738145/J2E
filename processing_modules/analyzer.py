import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font_path = 'font/SourceHanSansCN-VF.otf'  # 修正字体文件路径
font = FontProperties(fname=font_path)

import os

def analyze_and_plot(df, output_fields, output_dir='static/images'):
    """
    对指定字段进行频次统计并生成饼图
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历需要分析的字段
    for field in output_fields:
        if field not in df.columns:
            continue
            
        # 统计各值出现次数
        counts = df[field].value_counts()
        
        # 生成饼图
        plt.figure(figsize=(6, 6), dpi=120)  # 进一步增大画布尺寸和分辨率
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 24, 'fontproperties': font})
        plt.title(f'{field} Distribution', fontsize=32, fontproperties=font)
        plt.tight_layout()
        
        # 保存图片
        output_path = os.path.join(output_dir, f'{field}_distribution.png')
        plt.savefig(output_path, bbox_inches='tight', dpi=120)
        plt.close()
        print(f"生成图表保存至: {output_path}")
