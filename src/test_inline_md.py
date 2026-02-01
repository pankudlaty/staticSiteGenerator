import unittest
from inline_md import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_img_split_end(self):
        node = TextNode(
            "Image at the end. ![image](https://image.com/img.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("Image at the end. ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://image.com/img.png"),
            ],
            new_nodes,
        )

    def test_link_split_only_text(self):
        node = TextNode("This is only text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([TextNode("This is only text.", TextType.TEXT)], new_nodes)

    def test_link_split_one(self):
        node = TextNode(
            "This is a link [link](https://example.com/test) example.", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/test"),
                TextNode(" example.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_split_multiple(self):
        node = TextNode(
            "This are couple of links [link1](https://example.com) and another [link2](https://example.at).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This are couple of links ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.at"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_split_beginning(self):
        node = TextNode(
            "[link](https://example.com) link at the beginning of node", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" link at the beginning of node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_split_end(self):
        node = TextNode("Link at the end [link](https://example.com).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("Link at the end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTestToNode(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
