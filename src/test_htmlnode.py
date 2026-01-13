import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
