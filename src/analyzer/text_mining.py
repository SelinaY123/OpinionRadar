"""
抖音评论文本挖掘
提取关键词和热词分析
"""

import pandas as pd
import jieba
import jieba.analyse
from collections import Counter
import re

class TextMiner:
    """文本挖掘器"""
    
    def __init__(self, stopwords_file=None):
        """初始化文本挖掘器"""
        # 加载停用词
        self.stopwords = self.load_stopwords(stopwords_file)
        
        # 初始化结巴分词
        jieba.initialize()
    
    def load_stopwords(self, filepath):
        """加载停用词表"""
        stopwords = set()
        
        # 基础停用词
        base_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就',
            '不', '人', '都', '一', '一个', '上', '也', '很',
            '到', '说', '要', '去', '你', '会', '着', '没有',
            '看', '好', '自己', '这', '这个', '也'
        }
        
        stopwords.update(base_stopwords)
        
        # 从文件加载额外停用词
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            stopwords.add(word)
            except:
                print(f"警告：无法加载停用词文件 {filepath}")
        
        return stopwords
    
    def clean_text(self, text):
        """清理文本"""
        if not isinstance(text, str):
            return ""
        
        # 移除特殊字符和表情
        text = re.sub(r'[^\w\u4e00-\u9fff\s]', '', text)
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_keywords(self, text, top_n=10):
        """提取关键词"""
        if not text:
            return []
        
        # 使用TF-IDF提取关键词
        keywords = jieba.analyse.extract_tags(
            text, 
            topK=top_n,
            withWeight=True
        )
        
        return keywords
    
    def analyze_comments(self, df, text_column='内容', top_n=20):
        """分析评论的关键词"""
        print("开始文本挖掘...")
        
        # 合并所有评论
        all_text = ' '.join(df[text_column].dropna().astype(str))
        
        # 清理文本
        cleaned_text = self.clean_text(all_text)
        
        if not cleaned_text:
            print("没有有效文本进行分析")
            return {}
        
        # 分词
        words = []
        for text in df[text_column].dropna():
            seg_list = jieba.cut(str(text))
            for word in seg_list:
                word = word.strip()
                if (len(word) >= 2 and  # 至少2个字
                    word not in self.stopwords and
                    not word.isdigit()):
                    words.append(word)
        
        # 统计词频
        word_counts = Counter(words)
        
        # 获取前N个高频词
        top_words = word_counts.most_common(top_n)
        
        # 提取关键词
        print(f"\n前{top_n}个高频词:")
        for word, count in top_words:
            print(f"  {word}: {count}次")
        
        # 返回结果
        result = {
            'top_words': top_words,
            'total_words': len(words),
            'unique_words': len(word_counts),
            'all_word_counts': dict(word_counts)
        }
        
        return result
    
    def generate_wordcloud_data(self, df, text_column='内容'):
        """生成词云数据"""
        word_counts = self.analyze_comments(df, text_column, top_n=100)
        
        if 'all_word_counts' in word_counts:
            # 格式化为词云需要的格式
            wc_data = {}
            for word, count in word_counts['all_word_counts'].items():
                if count >= 2:  # 只包含出现2次以上的词
                    wc_data[word] = count
            
            return wc_data
        
        return {}
    
    def find_hot_topics(self, df, text_column='内容', min_count=5):
        """发现热点话题"""
        word_counts = self.analyze_comments(df, text_column, top_n=50)
        
        if 'top_words' not in word_counts:
            return []
        
        hot_topics = []
        for word, count in word_counts['top_words']:
            if count >= min_count:
                # 找到包含这个词的评论
                related_comments = df[df[text_column].str.contains(word, na=False)]
                
                topic = {
                    '关键词': word,
                    '出现次数': count,
                    '相关评论数': len(related_comments),
                    '示例评论': related_comments.head(3)[text_column].tolist()
                }
                
                hot_topics.append(topic)
        
        return hot_topics

def main():
    """测试文本挖掘"""
    # 创建测试数据
    test_data = [
        "这个视频太棒了，非常喜欢！",
        "内容很精彩，值得一看",
        "主播很可爱，关注了",
        "无聊的视频，没什么意思",
        "拍得真好，点赞支持",
        "一般般，可以看看",
        "超赞！已经分享给朋友了",
        "内容不错，继续加油"
    ]
    
    df = pd.DataFrame({'内容': test_data})
    
    # 进行文本挖掘
    miner = TextMiner()
    
    print("文本挖掘分析:")
    print("=" * 50)
    
    # 分析高频词
    result = miner.analyze_comments(df, top_n=10)
    
    # 发现热点话题
    print("\n热点话题发现:")
    hot_topics = miner.find_hot_topics(df, min_count=1)
    
    for i, topic in enumerate(hot_topics[:3], 1):
        print(f"\n话题{i}: {topic['关键词']}")
        print(f"  出现次数: {topic['出现次数']}")
        print(f"  相关评论: {topic['相关评论数']}条")
        print("  示例评论:")
        for comment in topic['示例评论']:
            print(f"    - {comment[:30]}...")

if __name__ == "__main__":
    main()