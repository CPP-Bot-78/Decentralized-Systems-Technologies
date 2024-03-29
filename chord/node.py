import pprint

class Node():
    # Μέγεθος fingers table
    m = 0
    # Μέγεθος δακτύλιου
    r_size = 2 ** m

    # Κατασκευάζει αντικείμενα Node
    def __init__(self, node_id, m):
        self.node_id = node_id
        self.predecessor = self
        self.successor = self
        self.fingers_table = [self]*m
        self.data = {}
    
    # Τυπώνει αντικείμενα Node
    def __str__(self):
        return str(self.node_id)
    
    # Εμφανίζει το fingers table του κόμβου
    def print_fingers_table(self):
        print(f'ID: {self.node_id}\nΕπόμενος: {self.successor.node_id}\nΠροηγούμενος: {self.predecessor.node_id}')
        print(f'Δεδομένα: ')
        pprint.pprint(self.data, depth=5)
        print(f'Fingers Table: ')
        for i in range(self.m):
            print(f'{(self.node_id + 2 ** i) % self.r_size} : {self.fingers_table[i].node_id}')

    # Βάζει τον κόμβο στο δίκτυο
    def join(self, node):
        suc = node.find_successor(self.node_id)
        pre = suc.predecessor
        
        self.find_node_place(pre, suc)
        self.update_fingers_table()

        # Παίρνει τα keys από το successor
        self.data = {key: self.successor.data[key] for key in sorted(
            self.successor.data.keys()) if key <= self.node_id}

        for key in sorted(self.data.keys()):
            if key in self.successor.data:
                del self.successor.data[key]

    # Αφαίρεση κόμβου από το δίκτυο
    def leave(self):
        # Διόρθωση successor, predecessor
        self.predecessor.successor = self.successor
        self.predecessor.fingers_table[0] = self.successor
        self.successor.predecessor = self.predecessor
        # Δίνει το key στον successor
        for key in sorted(self.data.keys()):
            self.successor.data[key] = self.data[key]

    # Βρίσκει τη θέση του κόμβου
    def find_node_place(self, pre, suc):
        pre.fingers_table[0] = self
        pre.successor = self
        suc.predecessor = self
        self.fingers_table[0] = suc
        self.successor = suc
        self.predecessor = pre


    # Ανανεώνει τα fingers του κόμβου
    def update_fingers_table(self, node_left = None, leave = False):
        for i in range(1, len(self.fingers_table)):
            temp_node = self.find_successor((self.node_id + 2 ** i) % self.r_size)
            if leave:
                if node_left != temp_node:
                    self.fingers_table[i] = temp_node
                else: 
                    self.fingers_table[i] = self.find_successor((temp_node.node_id + 2 ** i) % self.r_size)
            else:
                self.fingers_table[i] = temp_node


    # Βρίσκει τον κόμβο που είναι πιο κοντά στο key
    def closest_preceding_node(self, node, h_key):
        for i in range(len(node.fingers_table)-1, 0, -1):
            if self.distance(node.fingers_table[i-1].node_id, h_key) < self.distance(node.fingers_table[i].node_id, h_key):
                return node.fingers_table[i-1]

        return node.fingers_table[-1]

    # Υπολογισμός απόστασης μεταξύ 2 κόμβων στο δίκτυο
    def distance(self, n1, n2):
        if n1 <= n2: return n2 - n1
        else: return self.r_size - n1 + n2

    # Βρίσκει τον κόμβο που έχει την ευθύνη για το key
    def find_successor(self, key):
        if self.node_id == key:
            return self
        if self.distance(self.node_id, key) <= self.distance(self.successor.node_id, key):
            # print('jump')
            return self.successor
        else:
            # print('jump')
            return self.closest_preceding_node(self, key).find_successor(key)

