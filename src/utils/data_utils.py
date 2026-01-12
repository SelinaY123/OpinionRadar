"""
数据处理工具 - 简化版
"""

import pandas as pd
import numpy as np
from datetime import datetime

class DataUtils:
    """数据处理工具类"""
    
    @staticmethod
    def clean_dataframe(df):
        """清理DataFrame数据"""
        df_clean = df.copy()
        
        # 移除完全空白的行
        df_clean = df_clean.dropna(how='all')
        
        # 处理缺失值
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':  # 字符串类型
                df_clean[col] = df_clean[col].fillna('')
            else:  # 数值类型
                df_clean[col] = df_clean[col].fillna(0)
        
        # 移除重复行（保留第一个）
        df_clean = df_clean.drop_duplicates()
        
        print(f"数据清理完成: {len(df)} -> {len(df_clean)} 行")
        
        return df_clean
    
    @staticmethod
    def calculate_statistics(df):
        """计算基本统计信息"""
        stats = {
            '总行数': len(df),
            '总列数': len(df.columns),
            '缺失值总数': df.isnull().sum().sum(),
            '重复行数': df.duplicated().sum()
        }
        
        # 数值列的统计
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            numeric_stats = df[numeric_cols].describe().to_dict()
            stats['数值统计'] = numeric_stats
        
        # 文本列的统计
        text_cols = df.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            text_stats = {}
            for col in text_cols:
                text_stats[col] = {
                    '唯一值数量': df[col].nunique(),
                    '最常出现值': df[col].mode().iloc[0] if not df[col].mode().empty else None
                }
            stats['文本统计'] = text_stats
        
        return stats
    
    @staticmethod
    def detect_outliers(df, column, method='iqr', threshold=1.5):
        """检测异常值"""
        if column not in df.columns:
            print(f"列 {column} 不存在")
            return None
        
        data = df[column].dropna()
        
        if method == 'iqr':
            # IQR方法
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        elif method == 'zscore':
            # Z-score方法
            mean = data.mean()
            std = data.std()
            
            z_scores = np.abs((df[column] - mean) / std)
            outliers = df[z_scores > threshold]
        
        else:
            print(f"不支持的异常值检测方法: {method}")
            return None
        
        return outliers
    
    @staticmethod
    def convert_time_columns(df, time_columns=None):
        """转换时间列格式"""
        df_converted = df.copy()
        
        if time_columns is None:
            # 自动检测时间列
            time_columns = []
            for col in df.columns:
                if '时间' in col or 'date' in col.lower() or 'time' in col.lower():
                    time_columns.append(col)
        
        for col in time_columns:
            if col in df_converted.columns:
                try:
                    df_converted[col] = pd.to_datetime(df_converted[col], errors='coerce')
                    print(f"转换时间列: {col}")
                except Exception as e:
                    print(f"转换时间列 {col} 失败: {e}")
        
        return df_converted
    
    @staticmethod
    def sample_data(df, n=5, random_state=42):
        """随机抽样数据"""
        if len(df) <= n:
            return df.copy()
        
        return df.sample(n=n, random_state=random_state)
    
    @staticmethod
    def create_summary_report(df, output_file='data_summary.txt'):
        """创建数据摘要报告"""
        import textwrap
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("数据摘要报告")
        report_lines.append("=" * 60)
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")
        report_lines.append("")
        
        # 基本信息
        report_lines.append("一、基本信息")
        report_lines.append("-" * 40)
        report_lines.append(f"总行数: {len(df)}")
        report_lines.append(f"总列数: {len(df.columns)}")
        report_lines.append(f"缺失值: {df.isnull().sum().sum()}")
        report_lines.append(f"内存使用: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        report_lines.append("")
        
        # 列信息
        report_lines.append("二、列信息")
        report_lines.append("-" * 40)
        for i, col in enumerate(df.columns, 1):
            dtype = str(df[col].dtype)
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            
            if df[col].dtype == 'object':
                sample_value = str(df[col].iloc[0])[:30] if len(df) > 0 else "N/A"
                report_lines.append(f"{i:2d}. {col:20s} | {dtype:10s} | 空值: {null_count:4d} | 唯一: {unique_count:4d} | 示例: {sample_value}")
            else:
                report_lines.append(f"{i:2d}. {col:20s} | {dtype:10s} | 空值: {null_count:4d} | 唯一: {unique_count:4d} | 范围: {df[col].min():.2f} ~ {df[col].max():.2f}")
        report_lines.append("")
        
        # 数值列统计
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            report_lines.append("三、数值列统计")
            report_lines.append("-" * 40)
            numeric_stats = df[numeric_cols].describe()
            for col in numeric_cols:
                report_lines.append(f"{col}:")
                report_lines.append(f"  平均值: {df[col].mean():.2f}")
                report_lines.append(f"  中位数: {df[col].median():.2f}")
                report_lines.append(f"  标准差: {df[col].std():.2f}")
                report_lines.append(f"  最小值: {df[col].min():.2f}")
                report_lines.append(f"  最大值: {df[col].max():.2f}")
            report_lines.append("")
        
        # 保存报告
        report_text = '\n'.join(report_lines)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"数据摘要报告已保存: {output_file}")
        except Exception as e:
            print(f"保存报告失败: {e}")
        
        # 同时在控制台输出
        print(report_text)
        
        return report_text

def test_data_utils():
    """测试数据处理工具"""
    print("测试数据处理工具...")
    
    # 创建测试数据
    test_data = {
        '用户': ['张三', '李四', '王五', np.nan, '张三'],
        '点赞数': [100, 200, 300, 400, 100],
        '评论': ['很好', '', '不错', '一般', '很好'],
        '时间': ['2024-01-01', '2024-01-02', '2024-01-03', None, '2024-01-01']
    }
    
    df = pd.DataFrame(test_data)
    
    utils = DataUtils()
    
    print("原始数据:")
    print(df)
    print()
    
    # 清理数据
    df_clean = utils.clean_dataframe(df)
    print("清理后数据:")
    print(df_clean)
    print()
    
    # 计算统计信息
    stats = utils.calculate_statistics(df_clean)
    print("基本统计信息:")
    for key, value in stats.items():
        if key not in ['数值统计', '文本统计']:
            print(f"{key}: {value}")
    
    # 创建摘要报告
    utils.create_summary_report(df_clean, 'test_summary.txt')
    
    # 清理测试文件
    import os
    if os.path.exists('test_summary.txt'):
        os.remove('test_summary.txt')
        print("清理测试文件完成")

if __name__ == "__main__":
    test_data_utils()