"""
抖音评论可视化 - 简化版
生成各种分析图表
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import os

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

class DataVisualizer:
    """数据可视化器"""
    
    def __init__(self, output_dir='output/charts'):
        """初始化可视化器"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置图表风格
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def save_chart(self, fig, filename):
        """保存图表"""
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {filepath}")
        plt.close(fig)
    
    def plot_top_comments(self, df, top_n=10):
        """绘制热门评论图"""
        if '点赞数' not in df.columns:
            print("没有点赞数数据，无法绘制热门评论图")
            return None
        
        # 获取点赞最多的评论
        top_df = df.nlargest(top_n, '点赞数')[['用户', '点赞数', '内容']].copy()
        
        # 简化内容显示
        top_df['内容简写'] = top_df['内容'].apply(
            lambda x: x[:20] + '...' if len(x) > 20 else x
        )
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 柱状图
        bars = ax1.barh(
            range(len(top_df)), 
            top_df['点赞数'].values,
            color='skyblue'
        )
        ax1.set_yticks(range(len(top_df)))
        ax1.set_yticklabels(top_df['用户'].values)
        ax1.invert_yaxis()
        ax1.set_xlabel('点赞数')
        ax1.set_title(f'热门评论TOP{top_n}（按点赞数）')
        
        # 添加数值标签
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2,
                   f' {int(width)}', ha='left', va='center')
        
        # 饼图
        ax2.pie(
            top_df['点赞数'].values,
            labels=top_df['用户'].values,
            autopct='%1.1f%%',
            startangle=90
        )
        ax2.set_title('点赞数分布')
        
        plt.suptitle('热门评论分析')
        plt.tight_layout()
        
        # 保存图表
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'top_comments_{timestamp}.png'
        self.save_chart(fig, filename)
        
        return fig
    
    def plot_active_users(self, df, top_n=10):
        """绘制活跃用户图"""
        if '用户' not in df.columns:
            print("没有用户数据，无法绘制活跃用户图")
            return None
        
        # 统计用户评论数
        user_counts = df['用户'].value_counts().head(top_n)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 柱状图
        bars = ax1.bar(
            range(len(user_counts)), 
            user_counts.values,
            color='lightgreen'
        )
        ax1.set_xticks(range(len(user_counts)))
        ax1.set_xticklabels(user_counts.index, rotation=45, ha='right')
        ax1.set_ylabel('评论数')
        ax1.set_title(f'活跃用户TOP{top_n}（按评论数）')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        # 折线图（累计评论占比）
        cumulative_ratio = user_counts.cumsum() / user_counts.sum()
        
        ax2.plot(
            range(len(cumulative_ratio)), 
            cumulative_ratio.values,
            marker='o',
            linestyle='-',
            color='orange'
        )
        ax2.set_xticks(range(len(cumulative_ratio)))
        ax2.set_xticklabels(user_counts.index, rotation=45, ha='right')
        ax2.set_ylabel('累计评论占比')
        ax2.set_title('活跃用户累计贡献')
        ax2.grid(True, alpha=0.3)
        
        # 添加百分比标签
        for i, ratio in enumerate(cumulative_ratio.values):
            ax2.text(i, ratio, f'{ratio:.1%}', ha='center', va='bottom')
        
        plt.suptitle('用户活跃度分析')
        plt.tight_layout()
        
        # 保存图表
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'active_users_{timestamp}.png'
        self.save_chart(fig, filename)
        
        return fig
    
    def plot_sentiment_distribution(self, df):
        """绘制情感分布图"""
        if '情感分类' not in df.columns:
            print("没有情感分析数据，无法绘制情感分布图")
            return None
        
        sentiment_counts = df['情感分类'].value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        colors = ['#4CAF50', '#FFC107', '#F44336']  # 绿黄红
        
        # 饼图
        wedges, texts, autotexts = ax1.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        ax1.set_title('情感分布比例')
        
        # 美化百分比文字
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        # 柱状图
        bars = ax2.bar(
            range(len(sentiment_counts)),
            sentiment_counts.values,
            color=colors
        )
        ax2.set_xticks(range(len(sentiment_counts)))
        ax2.set_xticklabels(sentiment_counts.index)
        ax2.set_ylabel('评论数')
        ax2.set_title('情感分布数量')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        plt.suptitle('评论情感分析')
        plt.tight_layout()
        
        # 保存图表
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'sentiment_{timestamp}.png'
        self.save_chart(fig, filename)
        
        return fig
    
    def plot_word_frequency(self, word_counts, top_n=20):
        """绘制词频图"""
        if not word_counts or 'top_words' not in word_counts:
            print("没有词频数据，无法绘制词频图")
            return None
        
        top_words = word_counts['top_words'][:top_n]
        
        words = [word for word, _ in top_words]
        counts = [count for _, count in top_words]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 水平柱状图
        bars = ax.barh(range(len(words)), counts, color='steelblue')
        
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)
        ax.invert_yaxis()  # 最高的在最上面
        ax.set_xlabel('出现次数')
        ax.set_title(f'高频词汇TOP{top_n}')
        
        # 添加数值标签
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count, bar.get_y() + bar.get_height()/2,
                   f' {count}', ha='left', va='center')
        
        plt.tight_layout()
        
        # 保存图表
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'word_frequency_{timestamp}.png'
        self.save_chart(fig, filename)
        
        return fig
    
    def generate_report(self, df, analysis_results=None):
        """生成完整报告"""
        print("生成可视化报告...")
        
        charts = []
        
        # 1. 热门评论图
        if '点赞数' in df.columns:
            fig1 = self.plot_top_comments(df)
            if fig1:
                charts.append('top_comments.png')
        
        # 2. 活跃用户图
        if '用户' in df.columns:
            fig2 = self.plot_active_users(df)
            if fig2:
                charts.append('active_users.png')
        
        # 3. 情感分布图
        if '情感分类' in df.columns:
            fig3 = self.plot_sentiment_distribution(df)
            if fig3:
                charts.append('sentiment.png')
        
        # 4. 词频图
        if analysis_results and 'word_counts' in analysis_results:
            fig4 = self.plot_word_frequency(analysis_results['word_counts'])
            if fig4:
                charts.append('word_frequency.png')
        
        print(f"生成 {len(charts)} 个图表")
        
        return charts

def main():
    """测试可视化功能"""
    # 创建测试数据
    test_data = pd.DataFrame({
        '用户': ['用户A', '用户B', '用户C', '用户A', '用户B', '用户D'] * 5,
        '点赞数': [100, 80, 60, 90, 70, 50] * 5,
        '内容': ['很好的视频', '不错不错', '继续加油', '喜欢喜欢', '很棒', '支持'] * 5,
        '情感分类': ['积极', '积极', '中性', '积极', '积极', '积极'] * 5
    })
    
    # 测试可视化
    visualizer = DataVisualizer()
    
    print("测试可视化功能...")
    print("=" * 50)
    
    # 生成各种图表
    visualizer.plot_top_comments(test_data)
    visualizer.plot_active_users(test_data)
    visualizer.plot_sentiment_distribution(test_data)
    
    print("可视化测试完成！")

if __name__ == "__main__":
    main()