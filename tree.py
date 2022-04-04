ROOT = -1


def find_nodes(tree):
    internal_nodes = 0

    node = 0

    while node != -1:
        if node + 1 < len(tree):
            internal_nodes += 1
        if node + 2 < len(tree):
            node = node + 2
        else:
            node = -1
    return internal_nodes


def find_internal_nodes_num(tree):
    try:
        root_index = tree.index(ROOT)
    except ValueError as err:
        # Tree without root
        return

    nodes_number = 0

    list_one = tree[slice(root_index)]
    list_two = tree[slice(root_index + 1, len(tree))]

    nodes_number = find_nodes(list_one) + find_nodes(list_two)

    return nodes_number


if __name__ == "__main__":
    my_tree = [4, 4, 1, 5, -1, 4, 5]
    my_tree2 = [4, 4, 1, 5, -1, 4, 5, 1, 4, 7, 8, 34, 8, 9]
    my_tree3 = [4, 4, 1, 5, 5, 7, 5, -1, 4, 5, 7]

    assert find_internal_nodes_num([1, 5, 6, 7]) == None
    assert find_internal_nodes_num(my_tree) == 3
    assert find_internal_nodes_num(my_tree2) == 6
    assert find_internal_nodes_num(my_tree3) == 4
