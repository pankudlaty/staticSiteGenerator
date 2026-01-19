import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TextTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("Some link", TextType.LINK, "https://some.link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Some link")
        self.assertEqual(html_node.props, {"href": "https://some.link"})

    def test_image(self):
        node = TextNode("Some image", TextType.IMAGE, "https://image.img")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://image.img", "alt": "Some image"}
        )


if __name__ == "__main__":
    unittest.main()
