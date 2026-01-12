"""
抖音评论情感分析
使用基于词典的情感分析方法
"""

import pandas as pd
import jieba
import os

class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self, sentiment_dict_path=None):
        """初始化情感分析器"""
        # 基础情感词典
        self.positive_words = {
            '好', '棒', '赞', '优秀', '漂亮', '美', '可爱', '喜欢', '爱',
            '棒棒', '厉害', '强大', '精彩', '完美', '超赞', '太棒了',
            '支持', '加油', '棒棒哒', '美美哒', '喜欢喜欢', '赞赞赞'
        }
        
        self.negative_words = {
            '差', '烂', '垃圾', '差劲', '恶心', '讨厌', '无聊', '难看',
            '失望', '无语', '不行', '不好', '糟糕', '差评', '差差差',
            '恶评', '差劲', '太差了', '不好看', '没意思', '不喜欢'
        }
        
        # 程度副词权重
        self.intensity_words = {
            '非常': 1.5, '极其': 1.5, '十分': 1.5, '超级': 1.5, '特别': 1.5,
            '很': 1.3, '挺': 1.2, '比较': 1.1,
            '有点': 0.8, '稍微': 0.8, '略微': 0.8
        }
        
        # 否定词
        self.negation_words = {'不', '没', '无', '非', '莫', '勿', '未'}
    
    def analyze_sentence(self, text):
        """分析单个句子的情感"""
        if not isinstance(text, str):
            return 0
        
        # 分词
        words = list(jieba.cut(text))
        
        score = 0
        negation = False
        
        for i, word in enumerate(words):
            # 检查是否是否定词
            if word in self.negation_words:
                negation = True
                continue
            
            # 检查是否是程度副词
            intensity = self.intensity_words.get(word, 1.0)
            
            # 检查是否是情感词
            if word in self.positive_words:
                word_score = 1
            elif word in self.negative_words:
                word_score = -1
            else:
                continue
            
            # 应用否定词反转
            if negation:
                word_score = -word_score
                negation = False
            
            # 应用程度副词加权
            score += word_score * intensity
        
        # 归一化到[-1, 1]
        if len(words) > 0:
            score = max(-1, min(1, score / len(words)))
        
        return score
    
    def analyze_comments(self, df, text_column='内容'):
        """分析整个DataFrame的评论"""
        print("开始情感分析...")
        
        # 计算情感分数
        df['情感分数'] = df[text_column].apply(self.analyze_sentence)
        
        # 分类情感
        df['情感分类'] = df['情感分数'].apply(self.classify_sentiment)
        
        # 统计情感分布
        sentiment_counts = df['情感分类'].value_counts()
        
        print("情感分析完成！")
        print("\n情感分布:")
        for sentiment, count in sentiment_counts.items():
            print(f"  {sentiment}: {count} 条 ({count/len(df)*100:.1f}%)")
        
        return df, sentiment_counts
    
    def classify_sentiment(self, score):
        """根据分数分类情感"""
        if score > 0.1:
            return '积极'
        elif score < -0.1:
            return '消极'
        else:
            return '中性'
    
    def get_sentiment_summary(self, df):
        """获取情感分析摘要"""
        summary = {
            '积极评论数': len(df[df['情感分类'] == '积极']),
            '消极评论数': len(df[df['情感分类'] == '消极']),
            '中性评论数': len(df[df['情感分类'] == '中性']),
            '平均情感分数': df['情感分数'].mean(),
            '情感方差': df['情感分数'].var()
        }
        
        return summary

def main():
    """测试情感分析"""
    # 创建测试数据
    test_data = [
        "这个视频太棒了，我非常喜欢！",
        "内容一般般，没什么意思",
        "太差了，浪费时间",
        "还不错，可以看看",
        "超级无聊，不建议观看",
        "赞赞赞，值得推荐！"
    ]
    
    df = pd.DataFrame({'内容': test_data})
    
    # 进行情感分析
    analyzer = SentimentAnalyzer()
    df_result, counts = analyzer.analyze_comments(df)
    
    print("\n详细结果:")
    print(df_result[['内容', '情感分数', '情感分类']])
    
    print("\n情感摘要:")
    summary = analyzer.get_sentiment_summary(df_result)
    for key, value in summary.items():
        print(f"  {key}: {value:.2f}")

if __name__ == "__main__":
    main()