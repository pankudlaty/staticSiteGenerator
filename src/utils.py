import os, shutil


def copy_static_files(source_path, dst_path):
    if not os.path.exists(dst_path):
        raise FileNotFoundError(f"Destination directory not found:{dst_path}")
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source directory not found{source_path}")
    shutil.rmtree(dst_path)
    os.mkdir(dst_path)
    _copy_recursive(source_path, dst_path)


def _copy_recursive(source_path, dst_path):
    dir_content = os.listdir(source_path)
    for item in dir_content:
        src_item_path = os.path.join(source_path, item)
        dst_item_path = os.path.join(dst_path, item)
        if os.path.isfile(src_item_path):
            print(f"Coping file: {src_item_path} to: {dst_item_path}")
            shutil.copy(src_item_path, dst_item_path)
        else:
            os.mkdir(dst_item_path)
            _copy_recursive(src_item_path, dst_item_path)
