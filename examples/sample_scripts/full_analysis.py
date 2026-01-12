"""
完整抖音分析示例 - 演示所有功能
"""

import sys
import os
sys.path.append('../../src')

import pandas as pd
import json
from datetime import datetime

# 导入项目模块
from analyzer.basic_analysis import analyze_comments
from analyzer.sentiment_analysis import SentimentAnalyzer
from analyzer.text_mining import TextMiner
from analyzer.visualization import DataVisualizer
from utils.logger import get_logger

def run_full_analysis(json_file):
    """运行完整分析流程"""
    
    # 初始化日志
    logger = get_logger()
    logger.info("开始完整抖音分析流程")
    
    print("🎬 抖音评论完整分析工具")
    print("=" * 60)
    
    # 步骤1：加载数据
    logger.log_step(1, "加载数据", f"文件: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['comments'])
    print(f"✓ 加载数据: {len(df)} 条评论")
    
    # 步骤2：基础分析
    logger.log_step(2, "基础分析")
    print("\n📊 基础统计分析:")
    print("-" * 40)
    
    if '点赞数' in df.columns:
        print(f"总点赞数: {df['点赞数'].sum():,}")
        print(f"平均点赞: {df['点赞数'].mean():.1f}")
    
    print(f"用户数量: {df['用户'].nunique()}")
    print(f"评论时间范围: {df['时间'].min()} 到 {df['时间'].max()}")
    
    # 步骤3：情感分析
    logger.log_step(3, "情感分析")
    print("\n💖 情感分析:")
    print("-" * 40)
    
    analyzer = SentimentAnalyzer()
    df, sentiment_counts = analyzer.analyze_comments(df)
    
    # 步骤4：文本挖掘
    logger.log_step(4, "文本挖掘")
    print("\n🔍 文本挖掘:")
    print("-" * 40)
    
    miner = TextMiner()
    word_result = miner.analyze_comments(df, top_n=15)
    
    # 发现热点话题
    hot_topics = miner.find_hot_topics(df, min_count=2)
    if hot_topics:
        print("\n🔥 热点话题:")
        for i, topic in enumerate(hot_topics[:3], 1):
            print(f"{i}. {topic['关键词']} (出现{topic['出现次数']}次)")
    
    # 步骤5：可视化
    logger.log_step(5, "可视化")
    print("\n📈 生成可视化图表:")
    print("-" * 40)
    
    visualizer = DataVisualizer()
    
    analysis_results = {
        'word_counts': word_result,
        'sentiment_counts': sentiment_counts
    }
    
    charts = visualizer.generate_report(df, analysis_results)
    print(f"生成图表: {len(charts)} 个")
    
    # 步骤6：保存结果
    logger.log_step(6, "保存结果")
    print("\n💾 保存分析结果:")
    print("-" * 40)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"full_analysis_{timestamp}.xlsx"
    
    # 准备多个工作表的数据
    sheets_data = {
        '原始数据': df,
        '热门评论': df.nlargest(10, '点赞数') if '点赞数' in df.columns else df.head(10),
        '情感分析': df[['用户', '内容', '情感分数', '情感分类']],
        '活跃用户': df['用户'].value_counts().reset_index()
    }
    
    # 保存为Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, sheet_df in sheets_data.items():
            sheet_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    
    print(f"✓ 分析结果已保存: {output_file}")
    
    # 步骤7：生成报告
    logger.log_step(7, "生成报告")
    print("\n📋 分析报告摘要:")
    print("-" * 40)
    
    report = f"""
抖音评论分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据文件: {json_file}

📊 数据概览
- 评论总数: {len(df):,} 条
- 用户数量: {df['用户'].nunique()} 人
- 时间范围: {df['时间'].min()} 到 {df['时间'].max()}

💖 情感分析
- 积极评论: {len(df[df['情感分类'] == '积极'])} 条
- 中性评论: {len(df[df['情感分类'] == '中性'])} 条
- 消极评论: {len(df[df['情感分类'] == '消极'])} 条

🔍 文本分析
- 总词汇量: {word_result.get('total_words', 0):,} 词
- 独特词汇: {word_result.get('unique_words', 0)} 个

📈 输出文件
1. Excel报告: {output_file}
2. 图表文件: {len(charts)} 个PNG图表

🎯 分析完成！
"""
    
    print(report)
    
    # 保存报告
    report_file = f"analysis_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"完整分析完成，报告已保存: {output_file}")
    
    return df, output_file, charts

def main():
    """主函数"""
    print("抖音评论完整分析示例")
    print("=" * 60)
    
    # 使用示例数据
    json_file = "../sample_data/sample_comments.json"
    
    if not os.path.exists(json_file):
        print(f"文件不存在: {json_file}")
        print("正在创建示例数据...")
        
        # 创建示例数据
        example_data = {
            "video_info": {
                "video_id": "sample_video_001",
                "title": "测试视频"
            },
            "comments": [
                {
                    "用户": "用户1",
                    "内容": "这个视频真的很棒，内容很有价值！",
                    "点赞数": 150,
                    "时间": "2024-01-01 10:00:00"
                },
                {
                    "用户": "用户2", 
                    "内容": "非常喜欢，已经分享给朋友了",
                    "点赞数": 80,
                    "时间": "2024-01-01 10:05:00"
                },
                {
                    "用户": "用户3",
                    "内容": "内容一般，没什么新意",
                    "点赞数": 20,
                    "时间": "2024-01-01 10:10:00"
                },
                {
                    "用户": "用户1",
                    "内容": "期待更多这样的好内容",
                    "点赞数": 60,
                    "时间": "2024-01-01 10:15:00"
                },
                {
                    "用户": "用户4",
                    "内容": "太差了，浪费时间",
                    "点赞数": 5,
                    "时间": "2024-01-01 10:20:00"
                }
            ]
        }
        
        # 保存示例数据
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(example_data, f, ensure_ascii=False, indent=2)
        
        print(f"示例数据已创建: {json_file}")
    
    # 运行完整分析
    try:
        df, output_file, charts = run_full_analysis(json_file)
        
        print("\n" + "=" * 60)
        print("🎉 分析完成！")
        print(f"✓ 数据文件: {json_file}")
        print(f"✓ 分析报告: {output_file}")
        print(f"✓ 生成图表: {len(charts)} 个")
        print("=" * 60)
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()