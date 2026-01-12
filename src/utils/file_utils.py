"""
文件操作工具 - 简化版
"""

import os
import json
import pandas as pd
import yaml
from datetime import datetime

class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def ensure_directory(directory):
        """确保目录存在"""
        os.makedirs(directory, exist_ok=True)
        return directory
    
    @staticmethod
    def save_json(data, filepath, indent=2):
        """保存为JSON文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            print(f"JSON文件已保存: {filepath}")
            return True
        except Exception as e:
            print(f"保存JSON文件失败: {e}")
            return False
    
    @staticmethod
    def load_json(filepath):
        """加载JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"加载JSON文件失败: {e}")
            return None
    
    @staticmethod
    def save_excel(df, filepath, sheet_name='数据'):
        """保存为Excel文件"""
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 保存到Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"Excel文件已保存: {filepath}")
            return True
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
            return False
    
    @staticmethod
    def save_multiple_sheets(data_dict, filepath):
        """保存多个工作表到Excel"""
        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in data_dict.items():
                    # 限制工作表名称长度
                    safe_sheet_name = sheet_name[:31]
                    df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
            
            print(f"多工作表Excel文件已保存: {filepath}")
            return True
        except Exception as e:
            print(f"保存多工作表Excel失败: {e}")
            return False
    
    @staticmethod
    def load_config(config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    @staticmethod
    def generate_filename(base_name, extension='json'):
        """生成带时间戳的文件名"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"
    
    @staticmethod
    def get_file_info(filepath):
        """获取文件信息"""
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        return {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'created_time': datetime.fromtimestamp(stat.st_ctime),
            'modified_time': datetime.fromtimestamp(stat.st_mtime)
        }

def test_file_utils():
    """测试文件工具"""
    print("测试文件工具...")
    
    utils = FileUtils()
    
    # 测试确保目录
    test_dir = utils.ensure_directory('test_output')
    print(f"创建目录: {test_dir}")
    
    # 测试保存JSON
    test_data = {'test': '数据', 'number': 123}
    json_path = os.path.join(test_dir, 'test.json')
    utils.save_json(test_data, json_path)
    
    # 测试加载JSON
    loaded_data = utils.load_json(json_path)
    print(f"加载的JSON数据: {loaded_data}")
    
    # 测试生成文件名
    filename = utils.generate_filename('test', 'xlsx')
    print(f"生成的文件名: {filename}")
    
    # 清理测试文件
    import shutil
    if os.path.exists('test_output'):
        shutil.rmtree('test_output')
        print("清理测试文件完成")

if __name__ == "__main__":
    test_file_utils()