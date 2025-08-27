import os
import re
import shutil


def migrate_typora_images(md_file_path, target_image_folder):
    """
    迁移单个Markdown文件中的图片到目标文件夹并更新路径

    参数:
    md_file_path: Markdown文件路径
    target_image_folder: 目标图片文件夹路径
    """
    # 创建目标文件夹（如果不存在）
    os.makedirs(target_image_folder, exist_ok=True)

    # 读取Markdown内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配Typora中的图片语法：![alt](path "title")
    image_pattern = r'!\[(.*?)\]\((.*?)( ".*?")?\)'
    images = re.findall(image_pattern, content)

    if not images:
        print(f"{os.path.basename(md_file_path)}: 未找到图片")
        return

    # 处理每张图片
    for alt, img_path, title in images:
        # 忽略网络图片（以http开头）
        if img_path.startswith(('http://', 'https://')):
            continue

        # 获取原始图片的绝对路径
        if not os.path.isabs(img_path):
            img_abs_path = os.path.join(os.path.dirname(md_file_path), img_path)
        else:
            img_abs_path = img_path

        # 检查图片是否存在
        if not os.path.exists(img_abs_path):
            print(f"警告：图片不存在 - {img_abs_path}")
            continue

        # 复制图片到目标文件夹
        img_filename = os.path.basename(img_abs_path)
        target_path = os.path.join(target_image_folder, img_filename)

        # 避免重复复制
        if not os.path.exists(target_path):
            shutil.copy2(img_abs_path, target_path)
            print(f"已复制：{img_filename} -> {target_image_folder}")

        # 计算新的相对路径（相对于Markdown文件）
        new_rel_path = os.path.relpath(target_path, os.path.dirname(md_file_path))
        # 替换Windows反斜杠为正斜杠
        new_rel_path = new_rel_path.replace('\\', '/')

        # 更新Markdown中的图片路径
        old_pattern = f'![{alt}]({re.escape(img_path)}'
        if title:
            old_pattern += f'{title}'
        old_pattern += ')'

        new_pattern = f'![{alt}]({new_rel_path}{title})'
        content = content.replace(old_pattern, new_pattern)

    # 保存更新后的Markdown文件
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"处理完成：{os.path.basename(md_file_path)}，图片已迁移到：{target_image_folder}\n")


def batch_migrate_folder(md_root_folder, base_image_folder):
    """
    批量处理文件夹中所有Markdown文件
    为每个MD文件创建对应的图片子文件夹（如 git.md -> images/git）

    参数:
    md_root_folder: 存放所有Markdown文件的根文件夹
    base_image_folder: 图片根文件夹（所有子文件夹将创建在此目录下）
    """
    # 遍历根文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(md_root_folder):
        for file in files:
            # 只处理.md文件
            if file.lower().endswith('.md'):
                # 获取MD文件的完整路径
                md_file_path = os.path.join(root, file)

                # 生成对应的图片文件夹名称（去除.md后缀）
                md_filename = os.path.splitext(file)[0]
                target_image_folder = os.path.join(base_image_folder, md_filename)

                # 处理当前MD文件
                migrate_typora_images(md_file_path, target_image_folder)


# 使用示例
if __name__ == "__main__":
    # 存放所有Markdown文件的根文件夹
    md_root = r"D:\学习经验\study_document"
    # 图片根文件夹（所有子文件夹将创建在此目录下）
    base_image_dir = r"D:\学习经验\study_document\images"

    # 开始批量处理
    batch_migrate_folder(md_root, base_image_dir)
    print("所有文件处理完成！")
