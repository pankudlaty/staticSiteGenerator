from utils import copy_static_files

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    copy_static_files(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
