from block_md import (BlockType, markdown_to_blocks, block_to_block_type)
from htmlnode import ParentNode
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        
        

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        line = block.split("\n", 1)[0]
        prefix = line.split(" ",1)[0]
        heading_text = line.split(" ",1)[1]
        return ParentNode(f"h{len(prefix)}",text_to_children(heading_text.strip()))
    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line[1:].strip())
        quote_text = " ".join(cleaned_lines)
        return ParentNode("blockquote",text_to_children(quote_text.strip()))

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

    

