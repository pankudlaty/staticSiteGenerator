from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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
    elif block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(
        line.startswith(f"{index}. ") for index, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
