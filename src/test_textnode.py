import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Example text node", TextType.CODE)
        node2 = TextNode("Example text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)

    def test_text_type_not_eq(self):
        node = TextNode("Example text node", TextType.CODE)
        node2 = TextNode("Example text node", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_is_not_link(self):
        node = TextNode("This is example link", TextType.IMAGE)
        self.assertIsNone(node.url)

    def test_is_link(self):
        node = TextNode("Example link", TextType.LINK, "https://www.example.com")
        self.assertIsNotNone(node.url)


if __name__ == "__main__":
    unittest.main()
