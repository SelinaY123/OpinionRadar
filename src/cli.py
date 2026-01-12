"""
抖音分析命令行工具 - 增强版
支持完整分析流程
"""

import argparse
import sys
import os
import json
from datetime import datetime

def show_banner():
    """显示程序横幅"""
    banner = """
    ╔══════════════════════════════════════════════════╗
    ║         🎬 抖音评论分析工具 v1.0                ║
    ║        Douyin Comment Analyzer                   ║
    ╚══════════════════════════════════════════════════╝
    """
    print(banner)

def generate_crawler_script():
    """生成爬虫脚本"""
    from src.crawler.browser_crawler import main as crawler_main
    crawler_main()

def basic_analysis(filepath):
    """基础分析"""
    from src.analyzer.basic_analysis import analyze_comments
    return analyze_comments(filepath)

def full_analysis(filepath):
    """完整分析"""
    # 动态导入，避免循环依赖
    import pandas as pd
    from src.analyzer.sentiment_analysis import SentimentAnalyzer
    from src.analyzer.text_mining import TextMiner
    from src.analyzer.visualization import DataVisualizer
    from src.utils.logger import get_logger
    
    # 初始化日志
    logger = get_logger()
    logger.info(f"开始完整分析: {filepath}")
    
    print("🎬 开始完整抖音分析流程...")
    print("=" * 60)
    
    # 加载数据
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['comments'])
    print(f"✓ 加载 {len(df)} 条评论")
    
    # 情感分析
    print("\n💖 情感分析...")
    analyzer = SentimentAnalyzer()
    df, sentiment_counts = analyzer.analyze_comments(df)
    
    # 文本挖掘
    print("\n🔍 文本挖掘...")
    miner = TextMiner()
    word_result = miner.analyze_comments(df, top_n=15)
    
    # 可视化
    print("\n📈 生成可视化图表...")
    visualizer = DataVisualizer()
    analysis_results = {'word_counts': word_result}
    charts = visualizer.generate_report(df, analysis_results)
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"full_analysis_{timestamp}.xlsx"
    
    sheets_data = {
        '原始数据': df,
        '热门评论': df.nlargest(10, '点赞数') if '点赞数' in df.columns else df.head(10),
        '情感分析': df[['用户', '内容', '情感分数', '情感分类']],
        '文本分析': pd.DataFrame(word_result.get('top_words', []), columns=['词汇', '频次'])
    }
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, sheet_df in sheets_data.items():
            sheet_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    
    print(f"\n✅ 分析完成!")
    print(f"📊 报告文件: {output_file}")
    print(f"📈 图表数量: {len(charts)} 个")
    
    return output_file

def test_modules():
    """测试所有模块"""
    print("🧪 测试项目模块...")
    
    tests = []
    
    try:
        from tests.test_basic import run_tests
        success = run_tests()
        tests.append(("基础功能测试", "通过" if success else "失败"))
    except Exception as e:
        tests.append(("基础功能测试", f"错误: {e}"))
    
    # 显示测试结果
    print("\n📋 测试结果:")
    print("-" * 40)
    for test_name, result in tests:
        print(f"{test_name:20s}: {result}")
    
    return all("通过" in r for _, r in tests)

def setup_project():
    """项目设置和初始化"""
    print("🔧 项目初始化...")
    
    # 创建必要的目录
    directories = ['output', 'output/charts', 'output/data', 'logs']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 创建目录: {directory}")
    
    # 检查依赖
    print("\n📦 检查依赖...")
    try:
        import pandas
        print(f"✓ pandas {pandas.__version__}")
    except ImportError:
        print("✗ pandas 未安装")
    
    try:
        import jieba
        print(f"✓ jieba {jieba.__version__}")
    except ImportError:
        print("✗ jieba 未安装")
    
    print("\n✅ 项目初始化完成")

def main():
    """主函数"""
    show_banner()
    
    parser = argparse.ArgumentParser(
        description='抖音评论爬取与分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s crawl                    # 生成爬虫脚本
  %(prog)s analyze data.json        # 分析数据
  %(prog)s full data.json           # 完整分析
  %(prog)s test                     # 运行测试
  %(prog)s setup                    # 项目初始化
        """
    )
    
    # 添加子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 爬取命令
    crawl_parser = subparsers.add_parser('crawl', help='生成爬虫脚本')
    crawl_parser.add_argument('--type', choices=['browser', 'api'], default='browser',
                            help='爬虫类型（默认：browser）')
    
    # 基础分析命令
    analyze_parser = subparsers.add_parser('analyze', help='基础分析评论数据')
    analyze_parser.add_argument('file', help='数据文件路径（JSON格式）')
    analyze_parser.add_argument('--output', '-o', help='输出文件名')
    
    # 完整分析命令
    full_parser = subparsers.add_parser('full', help='完整分析（包含情感分析和可视化）')
    full_parser.add_argument('file', help='数据文件路径（JSON格式）')
    full_parser.add_argument('--output', '-o', help='输出文件名')
    
    # 测试命令
    test_parser = subparsers.add_parser('test', help='测试所有功能模块')
    
    # 设置命令
    setup_parser = subparsers.add_parser('setup', help='项目初始化和设置')
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    # 解析参数
    args = parser.parse_args()
    
    # 执行命令
    if args.command == 'crawl':
        generate_crawler_script()
        
    elif args.command == 'analyze':
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        basic_analysis(args.file)
        
    elif args.command == 'full':
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        full_analysis(args.file)
        
    elif args.command == 'test':
        test_modules()
        
    elif args.command == 'setup':
        setup_project()
        
    else:
        print(f"❌ 未知命令: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main()