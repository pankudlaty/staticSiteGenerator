import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_link_tag(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        correct = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), correct)

    def test_tag(self):
        node = LeafNode("p", "This is a paragraph of text")
        correct = "<p>This is a paragraph of text</p>"
        self.assertEqual(node.to_html(), correct)

    def test_div_with_props(self):
        node = LeafNode("div", "Some text", {"id": "card", "title": "some title"})
        correct = '<div id="card" title="some title">Some text</div>'
        self.assertEqual(node.to_html(), correct)
