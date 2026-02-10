from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
            # return new_nodes
        split_nodes = []
        current_text = old_node.text
        for i in range(len(matches)):
            splited = current_text.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
            if len(splited) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if splited[0] != "":
                split_nodes.append(TextNode(splited[0], TextType.TEXT))
            split_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
            current_text = splited[-1]
        if current_text != "":
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
            # return new_nodes
        split_nodes = []
        current_text = old_node.text
        for i in range(len(matches)):
            splited = current_text.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
            if len(splited) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if splited[0] != "":
                split_nodes.append(TextNode(splited[0], TextType.TEXT))
            split_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))
            current_text = splited[-1]
        if current_text != "":
            split_nodes.append(TextNode(current_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    extracted_img = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_img


def extract_markdown_links(text):
    extracted_links = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_node s
