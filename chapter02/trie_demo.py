# 1. 创建TrieNode类， 构建内置字典结构
class TrieNode:
    def __init__(self):
        self.nodes = dict()  # 构建字典
        self.is_leaf = False

    # 2. 添加insert函数，插入一个字到字典树中
    def insert(self, word: str):
        curr = self
        for char in word:
            if char not in curr.nodes:
                curr.nodes[char] = TrieNode()
            curr = curr.nodes[char]
        curr.is_leaf = True

    # 3. 添加insert_many函数，插入一列表的字到字典树中
    def insert_many(self, words: list):
        for word in words:
            self.insert(word)

    # 4. 添加search函数，在字典树里面查询一个字
    def search(self, word: str):
        curr = self
        for char in word:
            if char not in curr.nodes:
                return False
            curr = curr.nodes[char]
        return curr.is_leaf
