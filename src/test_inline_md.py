import unittest
from inline_md import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
)

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


class TestExtraction(unittest.TestCase):
    def test_img_extract(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_link_extract(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_img_split_only_text(self):
        node = TextNode("This is only text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("This is only text", TextType.TEXT)], new_nodes)

    def test_img_split_one(self):
        node = TextNode(
            "This is image ![some img](https://img.com) node.", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is image ", TextType.TEXT),
                TextNode("some img", TextType.IMAGE, "https://img.com"),
                TextNode(" node.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_img_split_multi(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_img_split_beginning(self):
        node = TextNode(
            "![image](https://image.com) node starting with img", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://image.com"),
                TextNode(" node starting with img", TextType.TEXT),
            ],
            new_nodes,
        )
