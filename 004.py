import graphviz
from collections import defaultdict


# 统计每个元素项的支持度
def count_support(transactions):
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[item] += 1
    return item_count


# 筛选频繁项并排序
def filter_and_sort_frequent_items(item_count, min_support):
    frequent_items = {item: count for item, count in item_count.items() if count >= min_support}
    sorted_frequent_items = sorted(frequent_items, key=frequent_items.get, reverse=True)
    return sorted_frequent_items


# 重构事务，只保留频繁项并按序排列
def reconstruct_transactions(transactions, sorted_frequent_items):
    new_transactions = []
    for transaction in transactions:
        filtered_transaction = [item for item in transaction if item in sorted_frequent_items]
        sorted_transaction = sorted(filtered_transaction, key=lambda x: sorted_frequent_items.index(x))
        new_transactions.append(sorted_transaction)
    return new_transactions


# 定义节点类
class TreeNode:
    def __init__(self, item, count=0):
        self.item = item
        self.count = count
        self.children = {}
        self.parent = None
        self.link = None


# 构建FP - tree和项头表
def build_fp_tree_and_header_table(transactions, sorted_frequent_items):
    root = TreeNode('null')
    header_table = defaultdict(list)
    for transaction in transactions:
        current_node = root
        for item in transaction:
            if item not in current_node.children:
                new_node = TreeNode(item, 1)
                new_node.parent = current_node
                current_node.children[item] = new_node
                header_table[item].append(new_node)
                if len(header_table[item]) > 1:
                    prev_node = header_table[item][-2]
                    prev_node.link = new_node
            else:
                current_node.children[item].count += 1
            current_node = current_node.children[item]
    return root, header_table


# 挖掘条件模式基
def find_conditional_pattern_bases(header_table, item):
    conditional_pattern_bases = []
    node = header_table[item][0]
    while node:
        prefix_path = []
        current = node.parent
        while current.item != 'null':
            prefix_path.append(current.item)
            current = current.parent
        prefix_path.reverse()
        if prefix_path:
            conditional_pattern_bases.append((prefix_path, node.count))
        node = node.link
    return conditional_pattern_bases


# 递归挖掘频繁项集
def mine_frequent_itemsets(header_table, sorted_frequent_items, min_support, prefix=frozenset()):
    frequent_itemsets = []

    for item in reversed(sorted_frequent_items):
        new_prefix = prefix | frozenset([item])
        support_count = sum(node.count for node in header_table[item])
        frequent_itemsets.append((new_prefix, support_count))

        conditional_pattern_bases = find_conditional_pattern_bases(header_table, item)

        # 正确展开带重复事务
        expanded_paths = []
        for path, count in conditional_pattern_bases:
            for _ in range(count):
                expanded_paths.append(path)

        if not expanded_paths:
            continue

        item_count = count_support(expanded_paths)
        new_sorted_frequent_items = filter_and_sort_frequent_items(item_count, min_support)

        if new_sorted_frequent_items:
            new_transactions = reconstruct_transactions(expanded_paths, new_sorted_frequent_items)
            new_root, new_header_table = build_fp_tree_and_header_table(new_transactions, new_sorted_frequent_items)

            # 只可视化条件FP树
            conditional_fp_tree_dot = visualize_fp_tree(new_root)
            conditional_fp_tree_dot.render(f'conditional_fp_tree_{item}', view=True)

            sub_frequent_itemsets = mine_frequent_itemsets(new_header_table, new_sorted_frequent_items,
                                                           min_support, new_prefix)
            frequent_itemsets.extend(sub_frequent_itemsets)

    return frequent_itemsets


# 可视化FP - tree
def visualize_fp_tree(root):
    dot = graphviz.Digraph(comment='FP-tree', format='png')
    dot.attr(dpi='300')  # 增加图像质量

    def add_nodes_edges(node):
        # 为每个节点创建一个唯一的标识符
        node_id = f"{node.item}_{node.count}"
        dot.node(node_id, label=f"{node.item}:{node.count}")
        if node.parent:
            parent_id = f"{node.parent.item}_{node.parent.count}"
            dot.edge(parent_id, node_id)  # 为父子节点之间添加边
        for child in node.children.values():
            add_nodes_edges(child)  # 递归处理每个子节点
        if node.link:  # 如果存在链接，添加链接
            link_id = f"{node.link.item}_{node.link.count}"
            dot.edge(node_id, link_id, color='red', style='dashed')  # 用红色虚线表示链接

    add_nodes_edges(root)  # 从根节点开始构建图
    return dot


# 事务数据
transactions = [
    ['r', 'z', 'h', 'j', 'p'],
    ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    ['z'],
    ['r', 'x', 'n', 'o', 's'],
    ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']
]

# 设置最小支持度
min_support = 3

# 步骤1：统计支持度
item_count = count_support(transactions)
print("各元素项支持度统计:")
for item, count in item_count.items():
    print(f"{item}: {count}")

# 步骤2：筛选并排序频繁项
sorted_frequent_items = filter_and_sort_frequent_items(item_count, min_support)
print("\n排序后的频繁项:")
print(sorted_frequent_items)

# 步骤3：重构事务
new_transactions = reconstruct_transactions(transactions, sorted_frequent_items)
print("\n重构后的事务:")
for transaction in new_transactions:
    print(transaction)

# 步骤4：构建FP - tree和项头表
root, header_table = build_fp_tree_and_header_table(new_transactions, sorted_frequent_items)

# 可视化FP - tree
fp_tree_dot = visualize_fp_tree(root)
fp_tree_dot.render('fp_tree', view=True)

# 挖掘频繁项集
frequent_itemsets = mine_frequent_itemsets(header_table, sorted_frequent_items, min_support)

print("\n频繁项集:")
for itemset, support in frequent_itemsets:
    print(f"{itemset}: {support}")
