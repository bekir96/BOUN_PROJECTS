'''
    'Node' class contains its children and whether it is the last word, and it does 
    this with two fields, 'children', 'is_end_of_word'
'''
class Node:
    def __init__(self) -> None:
        self.children = [None] * 37
        self.is_end_of_word = False


'''
    The 'Trie' class uses the 'Node' class created above as the field and holds the 
    'search', 'insert' functions and the 'traverse_node' helper function that allows 
    us to traverse all children of a node.
'''
class Trie:
    def __init__(self) -> None:
        self.root = Node()
        self.list_search = list()


    '''
    The 'insert' function allows to insert strings into the 'Trie' class.
    '''
    def insert(self, s) -> None:
        temp_node = self.root
        for char in s:
            if char.isdigit():  # Controls that char is digit or not
                index = ord(char) - 48
            elif char == 'ü':   # Controls that char is 'ü' or not
                index = ord(char) - 216
            else:               # Controls that char is else or not
                index = ord(char) - 87

            if not temp_node.children[index]:
                temp_node.children[index] = Node()

            temp_node = temp_node.children[index]

        temp_node.is_end_of_word = True


    '''
    The 'search' function allows to serach strings in the 'Trie' class.
    '''
    def search(self, s) -> bool:
        self.list_search = list()
        temp_node = self.root
        str_for_set = ""

        for char in s:
            if char == '*':
                self.traverse_node(root=temp_node, str_for_set=str_for_set)
            else:
                if char.isdigit():  # Controls that char is digit or not
                    index = ord(char) - 48
                elif char == 'ü':   # Controls that char is 'ü' or not
                    index = ord(char) - 216
                else:               # Controls that char is else or not
                    index = ord(char) - 87

                if not temp_node.children[index]:
                    return False

                str_for_set+=char
                temp_node = temp_node.children[index]

        if temp_node.is_end_of_word == True:
            self.list_search.append(str_for_set)
        
        if self.list_search == list():
            return False
        else:
            return True


    '''
    The 'traverse_node' helper function that allows  us to traverse all 
    children of a node.
    '''
    def traverse_node(self, root, str_for_set) -> None:
        temp = str_for_set
        for enum, node in enumerate(root.children):
            str_for_set = temp
            if node:
                if enum < 10:       # Controls that enum lower than 10 or not
                    char = chr(enum + 48)
                elif enum == 36:    # Controls that enum is 36 or not 
                    char = chr(enum + 216)
                else:               # Controls that enum is else or not 
                    char = chr(enum + 87)
                
                str_for_set+=char
                if node.is_end_of_word == True:
                    self.list_search.append(str_for_set)
            
                self.traverse_node(root=node, str_for_set=str_for_set)
