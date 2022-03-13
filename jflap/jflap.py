import os.path

NOT_FIND_NAME = -1
MULTI_NAME = -2
NOT_FIND_ID = -3
REMAINED = -1

class state(object):
    def __init__(self, name, id, label="", initial=False, final=False):
        self.name = name
        self.label = label
        self.id = id
        self.initial = False
        self.final = False
    def set_name(self, name):
        self.name = name
    def set_label(self, label=""):
        self.label = label
    def set_initial(self, initial=False):
        self.initial = initial
    def set_final(self, final=False):
        self.final = final
    def set_id(self, id):
        self.id = id

class Jflap(object):
    def __init__(self, file_name):
        self.file_name = file_name + ".jff"
        self.states = {}
        self.sigma = set()
        self.max_id = 0
    def create_file(self, path):
        with open(os.path.join(path, self.file_name), mode="w", encoding="utf-8") as w:
            #print(os.path.join(path, self.file_name))
            content = ""
            content += "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><!--Created with JFLAP 7.1.--><structure>&#13;"
            content += "\n\t<type>fa</type>&#13;"
            content += "\n\t<automaton>&#13;"
            content += "\n\t\t<!--The list of states.-->&#13;"
            content += "\n\t\t<!--The list of transitions.-->&#13;"
            content += "\n\t</automaton>&#13;"
            content += "\n</structure>"
            #print(content)
            os.chdir(path)
            w.write(content)

    def name_to_id(self, name):
        id = -1
        for state in self.states:
            if state.name == name and id != -1:
                id = state.id
            elif state.name == name and id == -1:
                return MULTI_NAME
        return NOT_FIND_NAME

    def add_state(self, name, label="", initial=False, final=False):
        id = -1 #represent has no id
        for i in range(0, self.max_id):
            if i not in self.states:
                id = i
                break
        if id == -1:
            id = self.max_id
            self.max_id += 1
        new_state = state(name, id, label, initial, final)
        self.states[new_state.id]=new_state

        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
            #print(lines)
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            #print(lines)
            for line in lines:
                if "<!--The list of states.-->" in line: #append new state
                    #print("This is target line:\n" + line)
                    new_line = line + "\t\t<state id=\"" + str(id) + "\" name=\"" + str(name) + "\">&#13;"
                    new_line = new_line + "\n\t\t\t<x>0.0</x>&#13;"
                    new_line = new_line + "\n\t\t\t<y>0.0</y>&#13;"
                    new_line = new_line + "\n\t\t\t<label>" + label + "</label>&#13;"
                    if initial is True:
                        new_line = new_line + "\n\t\t\t<initial/>&#13;"
                    else:
                        new_line = new_line + "\n"
                    if final is True:
                        new_line = new_line + "\n\t\t\t<final/>&#13;"
                    else:
                        new_line = new_line + "\n"
                    new_line = new_line + "\n\t\t</state>&#13;\n"
                    w.writelines(new_line)
                else:
                    #print("This is normal line:\n" + line)
                    w.write(line)

    def create_sigma(self, symbols):
        for symbol in symbols:
            self.sigma.add(symbol)

    def add_transition(self, from_id, to_id, symbol):
        if from_id not in self.states:
            print("There is not id=%d in states", from_id)
            return
        if to_id not in self.states:
            print("There is not id=%d in states", to_id)
            return

        if symbol != "\sigma":
            if symbol not in self.sigma:
                self.sigma.add(symbol)
        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
            #print(lines)
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            #print(lines)
            for line in lines:
                if "<!--The list of transitions.-->" in line:  # add new transition
                    new_line = line
                    if symbol != "\sigma":
                        new_line = new_line + "\t\t<transition>&#13;"
                        new_line = new_line + "\n\t\t\t<from>" + str(from_id) + "</from>&#13;"
                        new_line = new_line + "\n\t\t\t<to>" + str(to_id) + "</to>&#13;"
                        new_line = new_line + "\n\t\t\t<read>" + str(symbol) + "</read>&#13;"
                        new_line = new_line + "\n\t\t</transition>&#13;\n"
                        w.write(new_line)
                    else:
                        new_line = line
                        notation = "<!--This is sigma transition.-->"
                        for sym in self.sigma:
                            new_line = new_line + "\t\t<transition>&#13;"
                            new_line = new_line + "\n\t\t\t<from>" + str(from_id) + "</from>&#13;" + notation
                            new_line = new_line + "\n\t\t\t<to>" + str(to_id) + "</to>&#13;" + notation
                            new_line = new_line + "\n\t\t\t<read>" + str(sym) + "</read>&#13;" + notation
                            new_line = new_line + "\n\t\t</transition>&#13;" + notation + "\n"
                        w.write(new_line)
                else:
                    w.write(line)

    def add_transition_by_name(self, from_name, to_name, symbol):
        from_id = self.name_to_id(from_name)
        if from_id == NOT_FIND_NAME:
            print("Can't find %c in states!", from_name)
            return
        elif from_id == MULTI_NAME:
            print("There are multiple %c in states", from_name)
            return

        to_id = self.name_to_id(to_name)
        if to_id == NOT_FIND_NAME:
            print("Can't find %c in states!", to_name)
            return
        elif to_id == MULTI_NAME:
            print("There are multiple %c in states", to_name)
            return
        self.add_transition(from_id, to_id, symbol)

    def del_state(self, id):
        if id not in self.states:
            print("There is not id=%d in states", id)
            return
        else:
            self.states.pop(id)
        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            i = 0
            target_line_state = "<state id=\"" + str(id) + "\""
            target_line_from = "\t\t\t<from>" + str(id) + "</from>"
            target_line_to = "\t\t\t<to>" + str(id) + "</to>"
            while i < len(lines):
                if target_line_state in lines[i]:
                    i += 6
                elif i + 1 < len(lines) and target_line_from in lines[i + 1]:
                    i += 4
                elif i + 2 < len(lines) and target_line_to in lines[i + 2]:
                    i += 4
                else:
                    w.write(lines[i])
                i += 1

    def del_state_by_name(self, name):
        id = self.name_to_id(name)
        if id == NOT_FIND_NAME:
            print ("Can't find %c in states!", name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %c in states", name)
            return
        self.del_state(id)

    def del_transition(self, from_id, to_id, pre_symbol):
        if from_id not in self.states:
            print("There is not id=%d in states", from_id)
            return
        if to_id not in self.states:
            print("There is not id=%d in states", to_id)
            return

        if from_id not in self.states or to_id not in self.states:
            return
        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            i = 0
            target_line_from = "\t\t\t<from>" + str(from_id) + "</from>"
            target_line_to = "\t\t\t<to>" + str(to_id) + "</to>"
            target_line_symbol = "\t\t\t<read>" + str(pre_symbol) + "</read>"
            notation = "<!--This is sigma transition.-->"
            while i < len(lines):
                if pre_symbol != '\sigma' and notation not in lines[i]:
                    if i + 3 < len(lines) and target_line_from in lines[i + 1] and target_line_to in lines[i + 2] and target_line_symbol in lines[i + 3]:
                        i += 4
                    else:
                        w.write(lines[i])
                elif pre_symbol == '\sigma' and i + 1 < len(lines) and notation in lines[i + 1]:
                    if i + 3 < len(lines) and target_line_from in lines[i + 1] and target_line_to in lines[i + 2]:
                        i += 4
                    else:
                        w.write(lines[i])
                else:
                    w.write(lines[i])
                i += 1

    def del_transition_by_name(self, from_name, to_name, pre_symbol):
        from_id = self.name_to_id(from_name)
        if from_id == NOT_FIND_NAME:
            print("Can't find %c in states!", from_name)
            return
        elif from_id == MULTI_NAME:
            print("There are multiple %c in states", from_name)
            return

        to_id = self.name_to_id(to_name)
        if to_id == NOT_FIND_NAME:
            print("Can't find %c in states!", to_name)
            return
        elif to_id == MULTI_NAME:
            print("There are multiple %c in states", to_name)
            return

        self.del_transition(from_id, to_id, pre_symbol)

    def change_state(self, id, initial=REMAINED, final=REMAINED):
        if id not in self.states:
            print("There is not id=%d in states", id)
            return

        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
        target_line = "<state id=\"" + str(id) + "\""
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            i = 0
            while i < len(lines):
                line = lines[i]
                #print(line)
                if target_line in line:  # modify the state
                    if initial is True:
                        lines[i + 4] = "\t\t\t<initial/>&#13;"
                    elif initial is False:
                        lines[i + 4] = "\n"
                    if final is True:
                        lines[i + 5] = "\t\t\t<final/>&#13;"
                    elif final is False:
                        lines[i + 5] = "\n"
                    for j in range(0, 7):
                        w.write(lines[i])
                        i += 1
                else:
                    w.write(line)
                    #print(line)
                    i += 1

    def change_state_by_name(self, name, initial=REMAINED, final=REMAINED):
        id = self.name_to_id(name)
        if id == NOT_FIND_NAME:
            print("Can't find %c in states!", name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %c in states", name)
            return

        self.change_state(id, initial, final)

    def change_state_name(self, id, name=""):
        if id not in self.states:
            print("There is not id=%d in states", id)
            return

        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
        target_line = "<state id=\"" + str(id) + "\""
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            i = 0
            while i < len(lines):
                line = lines[i]
                if target_line in line:  # modify the name of the state
                    line = "\t\t<state id=\"" + str(id) + "\" name=\"" + name + "\">&#13;\n"
                    w.write(line)
                else:
                    w.write(line)
                i += 1

    def change_state_name_by_name(self, pre_name, new_name):
        id = self.name_to_id(pre_name)
        if id == NOT_FIND_NAME:
            print("Can't find %c in states!", pre_name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %c in states", pre_name)
            return

        self.change_state_name(id, new_name)

    def change_state_label(self, id, label=""):
        if id not in self.states:
            print("There is not id=%d in states", id)
            return

        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
        target_line = "<state id=\"" + str(id) + "\""
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            i = 0
            while i < len(lines):
                line = lines[i]
                if target_line in line:  # modify the name of the state
                    lines[i + 3] = "\n\t\t\t<label>" + label + "</label>&#13;\n"
                    for j in range(0, 7):
                        w.write(lines[i])
                        i += 1
                else:
                    w.write(line)
                    #print(line)
                    i += 1

    def change_state_label_by_name(self, name, label=""):
        id = self.name_to_id(name)
        if id == NOT_FIND_NAME:
            print("Can't find %c in states!", name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %c in states", name)
            return

        self.change_state_label(id, label)

    def change_transition(self, from_id, to_id, pre_symbol, new_symbol): # realize delete first
        '''with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            target_line_from = "\t\t\t<from>" + str(from_id) + "</from>"
            target_line_to = "\t\t\t<to>" + str(to_id) + "</to>"
            target_line_symbol = "\t\t\t<read>" + str(pre_symbol) + "</read>"
            i = 2
            while i < len(lines):
                if target_line_from in lines[i - 2] and target_line_to in lines[i - 1] and target_line_symbol in lines[i]:
                    lines[i] = "\t\t\t<read>" + str(new_symbol) + "</read>&#13;\n"
                w.write(lines[i])
                i += 1
        '''
        self.del_transition(from_id, to_id, pre_symbol)
        self.add_transition(from_id, to_id, new_symbol)

    def change_transition_by_name(self, from_name, to_name, pre_symbol, new_symbol):
        from_id = self.name_to_id(from_name)
        if from_id == NOT_FIND_NAME:
            print("Can't find %c in states!", from_name)
            return
        elif from_id == MULTI_NAME:
            print("There are multiple %c in states", from_name)
            return

        to_id = self.name_to_id(to_name)
        if to_id == NOT_FIND_NAME:
            print("Can't find %c in states!", to_name)
            return
        elif to_id == MULTI_NAME:
            print("There are multiple %c in states", to_name)
            return

        self.change_transition(from_id, to_id, pre_symbol, new_symbol)
'''
test = Jflap("test")
test.create_file(os.getcwd())
test.add_state("q0","0,0", initial=True)
test.add_state("q1","1,2", final=True)
test.add_state("q2", "ready to be deleted", final=True, initial=True)
test.create_sigma(['0', '1', '2', '3'])
test.add_transition(0, 1, '0')
test.add_transition(1, 0, '2')
test.add_transition(0, 1, '1')
test.add_transition(1, 2, "\sigma")
#test.add_transition(1, 0, "\sigma")

test.change_state(0, initial=False)
test.change_state(1, final=False)

test.change_state_name(0, "Zero")

test.change_state_label(1, "I am state 1")
#test.del_state(2)
test.change_transition(0, 1, '0', '3')
#test.change_transition(1, 0, "2", '\sigma')
#test.del_transition(1, 0, '\sigma')
#print (test.file_name)
'''

test = Jflap("test")
test.create_file(os.getcwd())
for i in range(0, 12):
    test.add_state(name = i)
test.change_state(0, initial=True)
test.change_state(11, final=True)
sigma = range(0, 10)
test.create_sigma(sigma)
for i in range (1, 11):
    test.add_transition(0, i, i)
    test.add_transition(i, i, "\sigma")
    test.add_transition(i, 11, i)


