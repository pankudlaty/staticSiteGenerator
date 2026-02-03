import unittest
from block_md import block_to_block_type, markdown_to_blocks, BlockType


class TestBlockMd(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_unordered_list(self):
        block = "- This is a list\n- with items"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_heading(self):
        block = "## Heading example"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_blocktype_code(self):
        block = "```\nSome code\nsome more code```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_to_blocktype_quote(self):
        block = "> Some quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_to_blocktype_ordered_list(self):
        block = "1. Item one\n2. Item two"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_to_blocktype_paragraph(self):
        block = "Some paragaraph with inline **bold** markdown"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()
