def markdown_to_blocks(markdown):
    blocks = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        section = section.strip()
        blocks.append(section)
    return blocks
