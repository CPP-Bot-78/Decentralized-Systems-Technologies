from node import Node
from csv_to_dict import create_education_dictionary
import hashlib

class Network():
    def __init__(self, m, node_ids):
        self.nodes = []
        self.m = m
        self.r_size = 2 ** m
        self.add_first_node(node_ids[0])
        self.first_node = self.nodes[0]
        node_ids.pop(0)
    
    # Δείχνει τα στοιχεία του δικτύου
    def __str__(self):
        return f'---------------\nΠλήθος: {len(self.nodes)} κόμβοι\nΧωρητικότητα: {self.r_size} κόμβοι\nΜέγεθος Fingers Table: {self.m}\nΠρώτος Κόμβος: {self.first_node.node_id}\n---------------'

    # Δείχνει τα fingers table και data όλων των κόμβων
    def print_network(self):
        print(self)
        for node in self.nodes:
            node.print_fingers_table()
            print('---------------')

    def add_first_node(self, node_id):
        node = Node(node_id, self.m)
        self.nodes.append(node)

    # Ανανεώνει το fingers table για όλους τους κόμβους του δικτύου
    def update_fingers_tables(self):
        self.first_node.update_fingers_table()
        curr = self.first_node.fingers_table[0]

        while curr != self.first_node:
            curr.update_fingers_table()
            curr = curr.fingers_table[0]

    # Κάνει hash στο key του κόμβου
    def hash_function(self, key):
        num_bits = Node.m

        # hashed bytes - transform key to hex and the to hashed bytes
        bt = hashlib.sha1(str.encode(key)).digest()

        # number of desired bytes for the id
        req_bytes = (num_bits + 7) // 8

        # transform bytes of the key to int
        # 'big' : the most significant byte is at the beginning of the byte array
        hashed_id = int.from_bytes(bt[:req_bytes], 'big')

        # wrap hash_id
        if num_bits % 8:
            hashed_id >>= 8 - num_bits % 8

        return hashed_id

    # Προσθέτει έναν κόμβο
    def add_node(self, node_id):
        new_node = Node(node_id, self.m)
        self.nodes.append(new_node)   
        node = self.nodes[-1]
        node.join(self.first_node)
        self.update_fingers_tables()

    # Αφαιρεί έναν κόμβο
    def remove_node(self, node_id):
        node = list(filter(lambda temp_node: temp_node.node_id ==
                               node_id, self.nodes))[0]
        node.leave()
        self.nodes.remove(node)
        self.update_fingers_tables()

    # Ψάχνει για το key στους κόμβους
    def lookup(self, data, threshold):
        h_key = self.hash_function(data)
        node = self.first_node
        node = node.find_successor(h_key)

        found_data = node.data.get(h_key, None)
        if found_data != None:
            found = False
            print(
                f'Βρέθηκε το key \'{data}\' στον κόμβο {node.node_id} με hash {h_key}')
            for scientists in found_data['value']:
                if scientists[1] >= threshold:
                    found = True
                    print(
                f'{scientists[0]}: {scientists[1]} βραβεία')
            if not found:
                print(f'Δεν υπάρχουν επιστήμονες με >= {threshold} βραβεία')
        else:
            print(f'Το \'{data}\' δεν υπάρχει σε κανένα κόμβο')

    # Βάζει τα δεδομένα στους κόμβους
    def add_data(self, n):
        my_dict = create_education_dictionary(n)
        for key, values in my_dict.items():
            node = self.first_node

            h_key = self.hash_function(key)
            print(
            f'Αποθήκευση του key \'{key}\' με hash {h_key} στον κόμβο {node.find_successor(h_key).node_id}')
            suc = node.find_successor(h_key)

            suc.data[h_key] = {'key': key, 'value': values}