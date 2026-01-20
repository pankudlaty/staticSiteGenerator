from typing import Text
import unittest
from inline_md import split_nodes_delimiter

from textnode import TextNode, TextType


class TestInlineMd(unittest.TestCase):
    def test_bold_delimeter(self):
        node = TextNode("This is text with **bold** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_double_bold(self):
        node = TextNode("Test two **bold** words in **one** text.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("Test two ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words in ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold_long(self):
        node = TextNode("Test the **long bold word**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("Test the ", TextType.TEXT),
                TextNode("long bold word", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold_begining(self):
        node = TextNode("**Begin with bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("Begin with bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple(self):
        node = TextNode(
            "Test _multiple_ sections **of text** and `some code`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("multiple", TextType.ITALIC),
                TextNode(" sections ", TextType.TEXT),
                TextNode("of text", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
            ],
            new_nodes,
        )
