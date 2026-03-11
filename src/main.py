from block_md import generate_page_recursive
from utils import copy_static_files
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"


def main():
    if len(sys.argv) != 2:
        basepath = "/"
    basepath = sys.argv[1]
    copy_static_files(dir_path_static, dir_path_docs)
    generate_page_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
