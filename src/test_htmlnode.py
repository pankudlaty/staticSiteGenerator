import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        correct = ' href="https://www.google.com" target="_blank"'
        result = node.props_to_html()
        self.assertEqual(result, correct)

    def test_values(self):
        node = HTMLNode("div", "Some example text in div")

        self.assertEqual(node.tag, "div")

        self.assertEqual(node.value, "Some example text in div")

        self.assertEqual(node.childern, None)

        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "Test value", None, {"class": "example"})
        correct = "HTMLNode(p, Test value, children:None, {'class': 'example'})"
        self.assertEqual(node.__repr__(), correct)

    def test_parent_node(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildern(self):
        granchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [granchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
