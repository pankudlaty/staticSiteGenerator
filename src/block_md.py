import os
from pathlib import Path
from enum import Enum
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextType, TextNode
from inline_md import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        section = section.strip()
        blocks.append(section)
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    elif (
        block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))
        and len(lines) == 1
    ):
        return BlockType.HEADING
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    elif all(
        line.startswith(f"{index}. ") for index, line in enumerate(lines, start=1)
    ):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    childern = []
    for block in blocks:
        html_node = block_to_html_node(block)
        childern.append(html_node)
    return ParentNode("div", childern, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    title = ""
    for block in blocks:
        if block.startswith("# "):
            title = block.strip("# ")
            title = title.strip()
    if title == "":
        raise Exception("Title markdown not found")
    return title


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path, "r")
    md_content = md_file.read()
    md_file.close()
    template = open(template_path, "r")
    template_content = template.read()
    template.close()
    node = markdown_to_html_node(md_content)
    html = node.to_html()
    title = extract_title(md_content)
    generated_page = template_content.replace("{{ Title }}", title)
    generated_page = generated_page.replace("{{ Content }}", html)
    generated_page = generated_page.replace('href="/', f'href="{basepath}')
    generated_page = generated_page.replace('src="/', f'src="{basepath}')
    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)
    page = open(dest_path, "w")
    page.write(generated_page)
    page.close()


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_content = os.listdir(dir_path_content)
    for item in dir_content:
        src_item_path = os.path.join(dir_path_content, item)
        dst_item_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_item_path):
            if src_item_path.endswith(".md"):
                dst_item_path = Path(dst_item_path)
                dst_item_path = dst_item_path.with_suffix(".html")
                generate_page(src_item_path, template_path, dst_item_path, basepath)
            else:
                continue
        else:
            generate_page_recursive(
                src_item_path, template_path, dst_item_path, basepath
            )
