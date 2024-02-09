import pprint
import sys
from filter_table import filter_table
from hash import hash_function


class Node:
    """Pastry Node.
    :param str node_id: Node's id
    :param int m: m-bit Keys and Nodes
    """

    nodes_cnt = 0

    def __init__(self, node_id, m=4):
        self.node_id = str(node_id)
        self.m = m
        self.nodes_num = m ** 2
        self.leaf_set = {"left": [], "right": []}
        self.routing_table = [[None] * self.nodes_num for _ in range(m)]
        self.data = {}
        Node.nodes_cnt += 1

    def __str__(self):
        return str(self.node_id)

    def __hash__(self):
        return hash_function(self.node_id)

    def print_routing_table(self):
        print(f"Routing Table for Node {self.node_id}:")
        for i, row in enumerate(self.routing_table):
            nodes = []
            for node in row:
                if isinstance(node, Node):
                    nodes.append(node.node_id)
            print(f"Row {i}: {nodes}")

    def print_leaf_sets(self):
        for leaf in ["left", "right"]:
            print(f"{leaf.capitalize()} Leaf:")
            for node in self.leaf_set[leaf]:
                print(node.node_id)
            print("--------------")

    def print_routing_table_and_leaf_set(self):
        print(f"ID: {self.node_id}")
        print(f"Κοντινότερος: {self.closest_preceding_node(self).node_id}")
        print(f"Δεδομένα: ")
        pprint.pprint(self.data, depth=5)
        self.print_routing_table()
        self.print_leaf_sets()

    def lcp(self, key):
        """Calculate the Longest Common Prefix (LCP) between the node's id and the key.
        :param str key: Node's id or data key
        :return: Least common prefix between self and key.
        :rtype: int"""
        key = str(key)
        node_id = str(self.node_id)
        lcp = ""
        if len(key) > len(node_id):
            for i in range(len(node_id)):
                for j in range(len(key)):
                    if key[j] == node_id[i]:
                        lcp += lcp.join(key[j])
                        break
        else:
            for i in range(len(key)):
                for j in range(len(node_id)):
                    if key[i] == node_id[j]:
                        lcp += lcp.join(key[i])
                        break
        if lcp != "":
            return int(lcp)
        else:
            return -1

    def join(self, node):
        """Βάζει τον κόμβο στο δίκτυο.
        Η τιμή του κόμβου είναι ήδη hashed
        :param Node node: Node that we want to insert/join
        :return: Nothing.
        :rtype: None
        """
        if node == self:  # Check if it is the same node
            pass
        else:
            self.update_routing_table(node, "INSERT")
            self.update_leaf_set(node, "INSERT")

    def leave(self):
        """Αφαιρεί τον κόμβο"""
        closest_node = self.closest_preceding_node(self)
        # closest_node.routing_table = self.routing_table ?
        closest_node.data = {
            **closest_node.data,
            **self.data,
        }  # add node's data to the closest node with dict unpacking

    def __eq__(self, other):
        return isinstance(other, Node) and self.node_id == other.node_id

    def update_routing_table(self, node, action):  # TODO FIX
        """Ανανεώνει το routing table για τον κόμβο
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None
        """
        if action == "INSERT":
            if Node.nodes_cnt == 1:
                self.routing_table[0][0] = [node]
            elif Node.nodes_cnt == 1:
                self.routing_table[1][0] = [node]
            elif Node.nodes_cnt < self.nodes_num:
                for row_index, row in enumerate(self.routing_table):
                    for row_node in row:  # find a not none Node
                        if isinstance(row_node, Node):
                            if node.lcp(row_node.node_id) != -1:
                                if None in row:
                                    node_index = row.index(None)
                                    self.routing_table[row_index][node_index] = node
                                    return
                                else:
                                    # new_row = sorted(row[:-1] + [node])
                                    # self.routing_table[row_index] = new_row
                                    self.add_in_full_routing_table(node)
                        else:
                            node_index = row.index(None)
                            self.routing_table[row_index][node_index] = node
                            return
            else:
                self.add_in_full_routing_table(node)

        elif action == "DELETE":
            for row_index, row in enumerate(self.routing_table):
                for i in range(len(row)):
                    n = row[i]
                    if isinstance(n, Node):
                        if node.node_id == n.node_id:
                            self.routing_table[row_index][i] = None
        else:
            print("ERROR")
    # def add_in_full_routing_table(self, node):

    def add_in_full_routing_table(self, node):
        """Προσθέτει τον κόμβο στην κατάλληλη θέση αν είναι γεμάτο το Routing Table.
                :return: Nothing.
                :rtype: None"""
        for row_index, row in enumerate(self.routing_table):
            if None in row:
                # Κανονικά δε θα έπρεπε να μπούμε εδώ μέσα μιας και η συνάρτηση
                # πρέπει να καλείται μόνο όταν ο πίνακας είναι γεμάτος.
                # Για αποφυγή λαθών συμπεριλαμβάνεται
                node_index = row.index(None)
                self.routing_table[row_index][node_index] = node
                break
            else:
                if row.count(None) == 0 and len(row) == self.m:
                    continue
                for row_node in row:
                    if node.lcp(row_node.node_id) != -1:
                        # Εισάγουμε ελέγχοντας την απόσταση
                        new_row = sorted(row[:-1] + [node], key=lambda x: x.node_id)
                        self.routing_table[row_index] = new_row
                        break
        # Τελικός έλεγχος αν μπήκε
        for row_index, row in enumerate(self.routing_table):
            if node not in row:
                break
            if row_index == len(self.routing_table)-1:
                # Δεν έχει μπει επειδή δεν υπάρχει lcp με κανέναν. Εισάγουμε ελέγχοντας την απόσταση
                new_row = sorted(row[:-1] + [node])
                self.routing_table[row_index] = new_row

    def closest_preceding_node(self, node):  # , h_key):  # TODO FIX Ή θα βρίσκει τον κοντινότερο ή θα επιστρέφει self
        """Βρίσκει τον κόμβο που είναι πιο κοντά στον κόμβο.
        :return: Closest Node to another.
        :rtype: Node"""
        min_distance = sys.maxsize  # max integer
        closest_node = node
        for leaf in ["left", "right"]:
            for n in self.leaf_set[leaf]:
                distance = self.distance(closest_node.node_id, n.node_id)
                if distance < min_distance:
                    min_distance = distance
                    closest_node = n
        if closest_node == node:
            clean_routing_table = filter_table(self.routing_table)
            for index, row in enumerate(clean_routing_table):
                for n in row:
                    if isinstance(n, Node):
                        distance = self.distance(node.node_id, n.node_id)
                        if distance < min_distance:
                            min_distance = distance
                            closest_node = n
        return closest_node

    def distance(self, n1, n2):
        """Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο"""
        n1 = int(n1)
        if isinstance(n2, Node):
            n2 = int(n2.node_id)
        else:
            n2 = int(n2)
        if n1 <= n2:
            return n2 - n1
        else:
            return self.nodes_num - n1 + n2

    def find_successor(self, key):  # TODO ?
        """Βρίσκει τον κόμβο που έχει την ευθύνη για το key
        :param str key: Hashed Key.
        :return: Closest node to key.
        :rtype: Node or None"""
        # if self.node_id == key:
        #     return self
        closest_node = self.closest_preceding_node(self)
        if isinstance(self, Node) and isinstance(closest_node, Node):
            if self.lcp(key) == -1:
                # it has not the same prefix, check routing table
                clean_routing_table = filter_table(self.routing_table)
                for n in clean_routing_table:
                    if isinstance(n, Node) and n.lcp(key) != -1:
                        return n.find_successor(key)
            elif self.lcp(key) < closest_node.lcp(key):
                # we pass the key to the closest node
                return closest_node.find_successor(key)
            elif self.lcp(key) >= closest_node.lcp(key):
                dist1 = self.distance(self.node_id, key)
                dist2 = self.distance(closest_node.node_id, key)
                if dist2 > dist1:
                    return closest_node
                else:
                    return self
        else:
            print("ERROR: Not a Node")
            return None  # Προσθέστε αυτήν τη γραμμή για να επιστρέφει None σε περίπτωση που υπάρξει κάποιο σφάλμα

    def update_leaf_set(self, node, action):  # TODO like Routing table methods
        """Ανανεώνει το leaf set για τον κόμβο.
        :param Node node: Node.
        :param str action: Either Insert or Delete. The action will be performed.
        :return: Nothing.
        :rtype: None"""
        node_place = self.closest_preceding_node(node)
        if self.lcp(node.node_id) == -1 or node_place is None:
            pass
        else:
            if int(node.node_id) >= int(self.node_id):
                leaf = "right"
            else:
                leaf = "left"
            # node_place = self.find_node_place(node)
            if action == "INSERT":
                # node_place = self.find_node_place(node)
                self.leaf_set[leaf].append(node)
                """if node_place.node_id == node.node_id or node_place.node_id == self.node_id:
                    least_dist = sys.maxsize  # max int
                    for n in self.leaf_set[leaf]:
                        dist = self.distance(node.node_id, n.node_id)
                        if dist < least_dist:
                            node_place = n
                    print(f"Node Place: {node_place}")  # Debug print
                    print(f"Leaf Set: {self.leaf_set}")  # Debug print

                    if node_place in self.leaf_set[leaf]:
                        nodes_index = self.leaf_set[leaf].index(node_place)
                        if self.leaf_set[leaf] is not None:
                            self.leaf_set[leaf].insert(nodes_index, node)
                        else:
                            self.leaf_set[leaf][nodes_index] = node
                    else:
                        print(f"Node Place not found in Leaf Set")"""
            elif action == "DELETE":
                print(f"Node Place: {node_place}")  # Debug print
                print(f"Leaf Set: {self.leaf_set}")  # Debug print
                self.leaf_set[leaf] = [x for x in self.leaf_set[leaf] if x != node]
            else:
                print("ERROR")
