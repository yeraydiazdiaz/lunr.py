from typing import Dict, List
from typing_extensions import TypedDict

from lunr.token_set import TokenSet
from lunr.exceptions import BaseLunrException


class UncheckedNode(TypedDict):
    parent: TokenSet
    char: str
    child: TokenSet


class TokenSetBuilder:
    def __init__(self) -> None:
        self.previous_word = ""
        self.root = TokenSet()
        self.unchecked_nodes: List[UncheckedNode] = []
        self.minimized_nodes: Dict[str, TokenSet] = {}

    def insert(self, word: str):
        if word < self.previous_word:
            raise BaseLunrException("Out of order word insertion")

        common_prefix = 0
        for i in range(min(len(word), len(self.previous_word))):
            if word[i] != self.previous_word[i]:
                break

            common_prefix += 1

        self.minimize(common_prefix)

        node = (
            self.root if not self.unchecked_nodes else self.unchecked_nodes[-1]["child"]
        )

        for i in range(common_prefix, len(word)):
            next_node = TokenSet()
            char = word[i]

            node.edges[char] = next_node

            self.unchecked_nodes.append(
                {"parent": node, "char": char, "child": next_node}
            )

            node = next_node

        node.final = True
        self.previous_word = word

    def finish(self):
        self.minimize(0)

    def minimize(self, down_to: int):
        for i in range(len(self.unchecked_nodes) - 1, down_to - 1, -1):
            node = self.unchecked_nodes[i]
            child_key = str(node["child"])

            if child_key in self.minimized_nodes:
                node["parent"].edges[node["char"]] = self.minimized_nodes[child_key]
            else:
                node["child"]._string = child_key
                self.minimized_nodes[child_key] = node["child"]

            self.unchecked_nodes.pop()
