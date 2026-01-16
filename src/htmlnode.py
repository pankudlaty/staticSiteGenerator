class HTMLNode:

    def __init__(self, tag=None, value=None, childern=None, props=None):
        self.tag = tag
        self.value = value
        self.childern = childern
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        formatted_str = ""
        for key, value in self.props.items():
            formatted_str += f' {key}="{value}"'
        return formatted_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children:{self.childern}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return f"{self.value}"
        if self.props is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        elif self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, childern, props=None):
        super().__init__(tag, None, childern, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.childern is None:
            raise ValueError("invalid HTML: no childern")
        html_tag = ""
        for child in self.childern:
            html_tag += child.to_html()
        return f"<{self.tag}>{html_tag}</{self.tag}>"
