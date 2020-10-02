docs = ["the cat is under the table",
        "the dog is under the table",
        "cats and dogs smell roses",
        "Carla eats an apple"]

# 创建索引
indexs = {}
for i, doc in enumerate(docs):
    # 遍历文档中的每个单词
    for word in doc.split():
        # 创建一个列表，其中包含所有包含指定单词的文档的索引
        if word not in indexs:
            indexs[word] = [i]
        else:
            indexs[word].append(i)
# 创建索引后，查询只需执行简单的字典查找。
# 例如，要返回所有包含单词table的文档，只需要查询索引，并获取相应的文档。
results = indexs["table"]
result_documents = [docs[i] for i in results]

print(f"result_documents: { result_documents }")
