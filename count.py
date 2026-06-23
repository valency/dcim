import sys
from pathlib import Path

def count_recursive_files(sub_dir):
    """
    保留原脚本逻辑：递归计算一个目录下所有有效文件的总数
    """
    total_files = 0
    ignored_system_files = {'thumbs.db', 'desktop.ini', 'ehthumbs.db', 'ntuser.dat'}
    
    # 递归遍历子目录下的所有内容
    for path in sub_dir.rglob('*'):
        if not path.is_file():
            continue
            
        # 忽略隐藏文件
        if path.name.startswith('.'):
            continue
            
        # 忽略特定系统文件
        if path.name.lower() in ignored_system_files:
            continue

        total_files += 1
    
    return total_files

def scan_first_level_subdirs(target_dir):
    root_path = Path(target_dir)
    
    if not root_path.exists():
        print(f"错误：路径 '{target_dir}' 不存在。")
        return

    print(f"\n--- 扫描报告: {root_path.absolute()} ---")
    print(f"{'子目录名称':<30} | {'文件总数':<10}")
    print("-" * 45)

    # 获取所有一级项目
    sub_items = sorted(list(root_path.iterdir()))
    
    has_subdir = False
    for item in sub_items:
        # 只处理一级子目录
        if item.is_dir():
            has_subdir = True
            count = count_recursive_files(item)
            print(f"{item.name:<30} | {count:>6} 个")

    if not has_subdir:
        print("未发现任何一级子目录。")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir_to_scan = sys.argv[1]
    else:
        dir_to_scan = "."
        print("提示: 未指定目录，正在扫描当前目录下的子目录。")

    scan_first_level_subdirs(dir_to_scan)