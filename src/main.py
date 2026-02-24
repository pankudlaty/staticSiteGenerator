from block_md import generate_page
from utils import copy_static_files

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    copy_static_files(dir_path_static, dir_path_public)
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
