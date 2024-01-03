import pprint

"""
#  DONE
#  ?
#  TODO
"""


class Node:
    """Pastry Node\n
    :param str node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """

    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = node_id
        self.nodes_num = 2**m
        # self.neighborhood_set = []
        # self.predecessor = self
        # self.successor = self
        self.leaf_set = {"left": [], "right": []}
        # self.right_leaf = []
        # self.left_leaf = []
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def print_routing_table(self):
        print(f"ID: {self.node_id}")
        print(f"Επόμενος: {self.routing_table[0].node_id}")
        # print(f"Προηγούμενος: {self.predecessor.node_id}")
        """print('Right Leaf:') Idk if i should use list or dict ftm
        for _ in self.leaf_set:
            print(self.leaf_set['right'])
        print('Left Leaf:')
        for _ in self.leaf_set:
            print(self.leaf_set['left'])"""
        print(f"Δεδομένα: ")
        pprint.pprint(self.data, depth=5)
        print(f"Routing Table: ")
        for i in range(self.node_id):
            print(
                f"{(self.node_id + 2 ** i) % self.nodes_num} : {self.routing_table[i].node_id}"
            )

    def lcp(self, key):
        """Calculate the Longest Common Prefix (LCP) between the node's id and the key"""
        lcp = ""
        if len(key) > len(self.node_id):
            for i in range(len(self.node_id)):
                if key[i] == self.node_id[i]:
                    lcp += lcp.join(key[i])
        else:
            for i in range(len(key)):
                if key[i] == self.node_id[i]:
                    lcp += lcp.join(key[i])
        if lcp != "":
            return lcp
        else:
            return -1

    def join(self, node_id):  # ?
        """Βάζει τον κόμβο στο δίκτυο.
        Η τιμή του κόμβου είναι ήδη hashed"""
        self.find_node_place(self.node_id)
        self.update_routing_table(self.node_id)
        self.update_leaf_set(self.node_id)

    def leave(self):  # ?
        """Αφαιρεί τον κόμβο"""

        pass

    def find_node_place(self, node_id):  # ?
        """Βρίσκει τη θέση του κόμβου.
        Ελέγχει ένα εκ των 2 φύλλων του leaf_set ανάλογα αν το n.
        Αν δε βρει κάτι πηγαίνει στο routing table"""
        lcp = self.lcp(node_id)
        max_lcp = lcp
        # global node_list
        node_list = []
        if int(node_id) < int(self.node_id):
            for node in self.leaf_set["left"]:
                lcp = node.lcp(node_id)
                print(f"left {lcp}")
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(node.node_id)
        elif int(node_id) > int(self.node_id):
            for node in self.leaf_set["right"]:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(node.node_id)
        if lcp == -1 or lcp == "" or lcp is None:
            for node in self.routing_table:
                lcp = node.lcp(node_id)
                if lcp == -1 or lcp == "" or lcp is None:
                    continue
                elif int(lcp) >= int(max_lcp):
                    max_lcp = lcp
                    node_list.append(node.node_id)
        node_list.append(self.node_id)
        node_list.sort()

        return node_list.index(node_id)

    def lookup(self, key):  # probably wrong file
        """Perform tree traversal search to find the node responsible for the given key"""
        current_node = self
        while True:
            # Calculate the LCP between the current node and the key
            lcp = current_node.lcp(key)
            # Check if the key matches the current node's identifier
            if lcp == len(current_node.node_id) and lcp == len(key):
                return current_node  # Found the responsible node
            # Check if the LCP points to a node in the routing table
            if lcp < len(current_node.node_id):
                next_hop = current_node.routing_table[lcp][
                    int(current_node.node_id[lcp], 16)
                ]
                if next_hop:
                    current_node = next_hop
                else:
                    return current_node  # No more specific route in the routing table
            # Check the leaf set for a closer node
            elif lcp < len(key):
                if int(key[lcp], 16) < int(current_node.node_id[lcp], 16):
                    current_node = current_node.leaf_set["left"]
                else:
                    current_node = current_node.leaf_set["right"]
            # No specific route found, return the current node
            else:
                return current_node

    def update_routing_table(self, node_id, action):
        """Ανανεώνει το routing table για τον κόμβο"""
        if action == "INSERT":
            # if node_id in self.routing_table:
            node_place = self.find_node_place(node_id)
            if self.routing_table[node_place] is not None:
                self.routing_table.insert(node_place, node_id)
            else:
                self.routing_table[node_place] = node_id
        elif action == "DELETE":
            for i in self.routing_table:
                if i == node_id:
                    i = None
        else:
            print("ERROR")

    def update_leaf_set(self, node_id, action):
        """Ανανεώνει το leaf set για τον κόμβο"""
        if int(node_id) >= int(self.node_id):
            leaf = "right"
        else:
            leaf = "left"
        if action == "INSERT":
            node_place = self.find_node_place(node_id)
            if self.leaf_set[leaf] is not None:
                self.leaf_set[leaf].insert(node_place, node_id)
            else:
                self.leaf_set[leaf][node_place] = node_id
        elif action == "DELETE":
            for i in self.leaf_set[leaf]:
                if i == node_id:
                    i = None
        else:
            print("ERROR")

    # def update_neighbourhood_set(self, node_id):
    #     """Ανανεώνει τις λίστες για τους γείτονες"""
    #     for neighbor in self.neighborhood_set:
    #         neighbor.update_routing_table(node_id)

    def closest_preceding_node(self, node, h_key):
        """Βρίσκει τον κόμβο που είναι πιο κοντά στο key"""
        pass

    def distance(self, n1, n2):
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο"""
        if n1 <= n2:
            return n2 - n1
        else:
            return self.nodes_num - n1 + n2

    def find_successor(self, key):
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key"""
        pass
