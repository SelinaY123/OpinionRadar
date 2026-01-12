"""
基础测试 - 测试核心功能
"""

import sys
import os
sys.path.append('../src')

import unittest
import pandas as pd
import json
from analyzer.basic_analysis import analyze_comments
from analyzer.sentiment_analysis import SentimentAnalyzer
from analyzer.text_mining import TextMiner

class TestBasicFunctions(unittest.TestCase):
    """测试基础功能"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建测试数据
        self.test_data = {
            "video_info": {"video_id": "test"},
            "comments": [
                {"用户": "张三", "内容": "很好", "点赞数": 100},
                {"用户": "李四", "内容": "不错", "点赞数": 80},
                {"用户": "王五", "内容": "一般", "点赞数": 50},
                {"用户": "张三", "内容": "继续加油", "点赞数": 120}
            ]
        }
        
        # 保存为临时文件
        self.test_file = "test_comments.json"
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False)
    
    def tearDown(self):
        """测试后的清理工作"""
        # 删除临时文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_analyze_comments(self):
        """测试基础分析功能"""
        df = analyze_comments(self.test_file)
        
        # 检查DataFrame形状
        self.assertEqual(len(df), 4)
        self.assertGreaterEqual(len(df.columns), 2)
        
        # 检查列名
        self.assertIn('用户', df.columns)
        self.assertIn('内容', df.columns)
    
    def test_sentiment_analyzer(self):
        """测试情感分析"""
        df = pd.DataFrame(self.test_data['comments'])
        
        analyzer = SentimentAnalyzer()
        df_result, counts = analyzer.analyze_comments(df)
        
        # 检查是否添加了情感列
        self.assertIn('情感分数', df_result.columns)
        self.assertIn('情感分类', df_result.columns)
        
        # 检查情感分类
        self.assertIn(df_result['情感分类'].iloc[0], ['积极', '中性', '消极'])
    
    def test_text_mining(self):
        """测试文本挖掘"""
        df = pd.DataFrame(self.test_data['comments'])
        
        miner = TextMiner()
        result = miner.analyze_comments(df, top_n=5)
        
        # 检查返回结果
        self.assertIn('top_words', result)
        self.assertIn('total_words', result)
        
        # 检查高频词列表
        self.assertIsInstance(result['top_words'], list)

def run_tests():
    """运行所有测试"""
    print("运行测试...")
    print("=" * 50)
    
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicFunctions)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print("\n" + "=" * 50)
    print(f"测试结果: {len(result.failures)} 失败, {len(result.errors)} 错误")
    
    if result.wasSuccessful():
        print("✓ 所有测试通过！")
    else:
        print("✗ 有测试失败")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()