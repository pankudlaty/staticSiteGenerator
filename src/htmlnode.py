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
