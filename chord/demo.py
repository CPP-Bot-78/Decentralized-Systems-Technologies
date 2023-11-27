from node import Node
from network import Network
from random import sample


m_user = int(input('Παράμετρoς m: '))
Node.m = m_user
Node.r_size = 2 ** m_user
print(f'Το δίκτυο έχει χωρητικότητα για {Node.r_size} κόμβους')
num_nodes = int(input('Πλήθος κόμβων: '))
while num_nodes > 2 ** m_user:
    print('Μη έγκυρο πλήθος κόμβων')
    num_nodes = int(input('Πλήθος κόμβων: '))

# Γεννήτρια x τυχαίων/unique id από 0 έως το μέγιστο επιτρεπτό
node_ids = sample(range(Node.r_size), num_nodes)

# Κατασκευή του δικτύου
s_network = Network(m_user, node_ids)

# Κατασκευή των κόμβων που θα εισαχθούν στο δίκτυο
for node_id in node_ids: 
    node = Node(node_id, m_user)
    s_network.nodes.append(node)

# Προσθήκη των κόμβων στο δίκτυο
for node in s_network.nodes:
    node.join(s_network.first_node)
    print(f'Κόμβος {node.node_id} προστέθηκε στο δίκτυο')

# Προσθήκη δεδομένων στους κόμβους του δικτύου
n_data = int(input(f'Πλήθος δεδομένων: '))
while n_data > 2 ** m_user:
    print('Μη έγκυρο πλήθος δεδομένων')
    n_data = int(input('Πλήθος δεδομένων: '))

s_network.add_data(n_data)

s_network.update_fingers_tables()

s_network.visualize_chord()

while True:
    print('1 -> Προσθήκη κόμβου')
    print('2 -> Αφαίρεση κόμβου')
    print('3 -> Αναζήτηση δεδομένων')
    print('4 -> Πληροφορίες κόμβων')
    print('5 -> Προβολή γράφου')
    choice = int(input('# -> '))
    if choice == 1: 
        node_id = int(input('ID Κόμβου: '))
        if node_id in node_ids:
            print('Υπάρχει ήδη κόμβος με αυτό το ID!')
        elif node_id > s_network.r_size:
            print(f'Το ID πρέπει να είναι από 0 έως {s_network.r_size}!')
        else:
            s_network.add_node(node_id)
            node_ids.append(node_id)
            s_network.print_network()
    elif choice == 2: 
        node_id = int(input('ID Κόμβου: '))
        if node_id not in node_ids:
            print('Δεν υπάρχει κόμβος με αυτό το ID!')
        else:
            node_ids.remove(node_id)
            s_network.remove_node(node_id)
            s_network.print_network()
    elif choice == 3: 
        query = input('Πανεπιστήμιο: ')
        num_awards = int(input('# Βραβεία: '))
        s_network.lookup(query, num_awards)
    elif choice == 4: 
        s_network.print_network()
    elif choice == 5:
        s_network.visualize_chord()
    elif choice == 6:
        s_network.update_fingers_tables()
    else: 
        print('Τερματισμός')
        break
