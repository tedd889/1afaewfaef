import itertools
import time
import matplotlib.pyplot as plt


class TreeNode:
    def __init__(self, item, count=1, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.node_link = None

    def increment(self, count):
        self.count += count


def create_tree(data_set, min_sup):
    item_count = {}
    for trans in data_set:
        for item in trans:
            item_count[item] = item_count.get(item, 0) + 1
    freq_items = {}
    for k in item_count:
        if item_count[k] >= min_sup:
            freq_items[k] = item_count[k]
    if len(freq_items) == 0:
        return None, None
    header_table = {}
    for k in freq_items:
        header_table[k] = [freq_items[k], None]
    ret_tree = TreeNode('Null Set', 0, None)
    for tran_set in data_set:
        local_id = {}
        for item in tran_set:
            if item in freq_items:
                local_id[item] = freq_items[item]
        if len(local_id) > 0:
            ordered_items = [v[0] for v in sorted(local_id.items(), key=lambda p: p[1], reverse=True)]
            update_tree(ordered_items, ret_tree, header_table)
    return ret_tree, header_table


def update_tree(items, in_tree, header_table):
    if items[0] in in_tree.children:
        in_tree.children[items[0]].increment(1)
    else:
        in_tree.children[items[0]] = TreeNode(items[0], 1, in_tree)
        if header_table[items[0]][1] is None:
            header_table[items[0]][1] = in_tree.children[items[0]]
        else:
            update_header(header_table[items[0]][1], in_tree.children[items[0]])
    if len(items) > 1:
        update_tree(items[1::], in_tree.children[items[0]], header_table)


def update_header(node_to_test, target_node):
    while node_to_test.node_link is not None:
        node_to_test = node_to_test.node_link
    node_to_test.node_link = target_node


def ascend_tree(leaf_node, prefix_path):
    if leaf_node.parent is not None:
        prefix_path.append(leaf_node.item)
        ascend_tree(leaf_node.parent, prefix_path)


def find_prefix_path(base_pat, header_table):
    tree_node = header_table[base_pat][1]
    cond_pats = {}
    while tree_node is not None:
        prefix_path = []
        ascend_tree(tree_node, prefix_path)
        if len(prefix_path) > 1:
            cond_pats[frozenset(prefix_path[1:])] = tree_node.count
        tree_node = tree_node.node_link
    return cond_pats


def mine_tree(in_tree, header_table, min_sup, pre_fix, freq_item_list):
    bigL = [v[0] for v in sorted(header_table.items(), key=lambda p: p[1][0])]
    for base_pat in bigL:
        new_freq_set = pre_fix.copy()
        new_freq_set.add(base_pat)
        freq_item_list.append(new_freq_set)
        cond_patt_bases = find_prefix_path(base_pat, header_table)
        my_cond_tree, my_head = create_tree(cond_patt_bases, min_sup)
        if my_head is not None:
            mine_tree(my_cond_tree, my_head, min_sup, new_freq_set, freq_item_list)


# 简单数据集示例
def load_simple_data():
    simp_dat = [['r', 'z', 'h', 'j', 'p'],
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                ['z'],
                ['r', 'x', 'n', 'o', 's'],
                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simp_dat


# 时间复杂度可视化
data_sizes = [10, 20, 30, 40, 50]
times = []

for size in data_sizes:
    simple_data = load_simple_data()[:size]
    start_time = time.time()
    min_sup = 3
    init_set = [frozenset(trans) for trans in simple_data]
    my_fp_tree, my_header_tab = create_tree(init_set, min_sup)
    freq_items = []
    mine_tree(my_fp_tree, my_header_tab, min_sup, set([]), freq_items)
    end_time = time.time()
    times.append(end_time - start_time)

plt.plot(data_sizes, times)
plt.xlabel('Data Size')
plt.ylabel('Time (s)')
plt.title('FP - Growth Algorithm Time Complexity')
plt.show()

