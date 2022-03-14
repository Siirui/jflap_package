import os.path

NOT_FIND_NAME = -1
MULTI_NAME = -2
NOT_FIND_ID = -3
NOT_DETERMINED = -1
REMAINED = -1


class State(object):
    def __init__(self, name, id, label="", initial=False, final=False):
        self.name = name
        self.label = label
        self.id = id
        self.initial = initial
        self.final = final

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
        """
        Create a new file with default template.
        :param path: The path where the file was created.
        :return: NULL
        """
        try:
            with open(os.path.join(path, self.file_name), mode="w", encoding="utf-8") as w:
                # print(os.path.join(path, self.file_name))
                content = ""
                content += "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><!--Created with JFLAP 7.1.--><structure>&#13;"
                content += "\n\t<type>fa</type>&#13;"
                content += "\n\t<automaton>&#13;"
                content += "\n\t\t<!--The list of states.-->&#13;"
                content += "\n\t\t<!--The list of transitions.-->&#13;"
                content += "\n\t</automaton>&#13;"
                content += "\n</structure>"
                # print(content)
                os.chdir(path)
                w.write(content)
                print("Successfully create file %s" % (os.path.join(path, self.file_name)))
        except IOError:
            print("Unsuccessfully create file %s" % (os.path.join(path, self.file_name)))

    def name_to_id(self, name):
        """
        Find the corresponded id to the name in states.
        :param name: State's name
        :return: If successfully find the id, the return the id; If there is no
        states named with param_name then return NOT_FIND_NAME; If there is multiple states' names same then return MULTI_NAME
        """
        id = NOT_DETERMINED
        for idx in self.states:
            # print(self.states[idx].name, name)
            if self.states[idx].name == name and id == NOT_DETERMINED:
                id = self.states[idx].id
            elif self.states[idx].name == name and id != NOT_DETERMINED:
                return MULTI_NAME
        if id == NOT_DETERMINED:
            return NOT_FIND_NAME
        else:
            return id

    def add_state(self, name, label="", initial=False, final=False):
        """
        Add a new state to FA
        :param name: The name of the state
        :param label: The label of the state
        :param initial: If initial is True then the state is initial one
        :param final: If final is True then the state is the accepting state
        :return:NULL
        """
        id = NOT_DETERMINED  # Represent has no id
        for idx in range(0, self.max_id):
            if idx not in self.states:
                id = idx
                break
        if id == NOT_DETERMINED:
            id = self.max_id
            self.max_id += 1
        new_state = State(name, id, label, initial, final)
        # print("state %d with name %s" % (id, name))
        self.states[new_state.id] = new_state
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                lines = r.readlines()
                # print(lines)
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                # print(lines)
                for line in lines:
                    if "<!--The list of states.-->" in line:  # append new state
                        # print("This is target line:\n" + line)
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
                        # print("This is normal line:\n" + line)
                        w.write(line)
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))
        print("State %s has been successfully added!" % name)

    def create_sigma(self, symbols):
        """
        Create the alphabet of FA
        :param symbols: Alphabet
        :return: NULL
        """
        for symbol in symbols:
            self.sigma.add(symbol)
        print("Successfully build the alphabet!")

    def add_transition(self, from_id, to_id, symbols):
        """
        Add a transition from start state to end state with symbol.
        :param from_id: The id of the start state
        :param to_id: The id of  the end state
        :param symbols: The symbols of this transition
        :return: NULL
        """
        if from_id not in self.states:
            print("There is no id=%d in states" % from_id)
            return
        if to_id not in self.states:
            print("There is no id=%d in states" % to_id)
            return
        for symbol in symbols:
            if symbol != "/sigma":
                if symbol not in self.sigma:
                    self.sigma.add(symbol)
            try:
                with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                    lines = r.readlines()
                    # print(lines)
            except IOError:
                print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))
            try:
                with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                    # print(lines)
                    for line in lines:
                        if "<!--The list of transitions.-->" in line:  # add new transition
                            new_line = line
                            if symbol != "/sigma":
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
            except IOError:
                print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

            print("Successfully add a transition from %s to %s with symbol %s" % (self.states[from_id].name, self.states[to_id].name, symbol))

    def add_transition_by_name(self, from_name, to_name, symbols):
        """
        Add transition from start state to end state with symbol by using name to index
        :param from_name: The name of start state
        :param to_name: The name of end state
        :param symbols: The symbols of this transition
        :return:NULL
        """

        from_id = self.name_to_id(from_name)
        if from_id == NOT_FIND_NAME:
            print("Can't find %s in states!" % from_name)
            return
        elif from_id == MULTI_NAME:
            print("There are multiple %s in states" % from_name)
            return

        to_id = self.name_to_id(to_name)
        if to_id == NOT_FIND_NAME:
            print("Can't find %s in states!" % to_name)
            return
        elif to_id == MULTI_NAME:
            print("There are multiple %s in states" % to_name)
            return

        # print("!!!",from_id, to_id)
        self.add_transition(from_id, to_id, symbols)

    def del_state(self, id):
        """
        Delete a state from FA.
        :param id: The id of the state
        :return: NULL
        """

        if id not in self.states:
            print("There is not id=%d in states" % id)
            return
        else:
            self.states.pop(id)
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                lines = r.readlines()
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                idx = 0
                target_line_state = "<state id=\"" + str(id) + "\""
                target_line_from = "\t\t\t<from>" + str(id) + "</from>"
                target_line_to = "\t\t\t<to>" + str(id) + "</to>"
                while idx < len(lines):
                    if target_line_state in lines[idx]:
                        idx += 6
                    elif idx + 1 < len(lines) and target_line_from in lines[idx + 1]:
                        idx += 4
                    elif idx + 2 < len(lines) and target_line_to in lines[idx + 2]:
                        idx += 4
                    else:
                        w.write(lines[idx])
                    idx += 1
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))
        print("Successfully delete state %d!" % id)

    def del_state_by_name(self, name):
        """
        Delete the state from FA by using name to index
        :param name: The name of the state
        :return: NULL
        """
        id = self.name_to_id(name)
        if id == NOT_FIND_NAME:
            print("Can't find %s in states!" % name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %s in states" % name)
            return
        self.del_state(id)

    def del_transition(self, from_id, to_id, pre_symbols, all=False):
        """
        Delete the transition from start state to end state with pre_symbol.
        :param all: If all is True, then delete all the transition from start state to end state.
        :param from_id: The id of the start state.
        :param to_id: The id of the end state.
        :param pre_symbols: The symbols of this transition.
        :return: NULL
        """
        if from_id not in self.states:
            print("There is not id=%d in states" % from_id)
            return
        if to_id not in self.states:
            print("There is not id=%d in states" % to_id)
            return

        if from_id not in self.states or to_id not in self.states:
            return
        idx_symbol = 0
        while idx_symbol < len(pre_symbols) or all is True:
            pre_symbol = ""
            if (idx_symbol < len(pre_symbols)):
                pre_symbol = pre_symbols[idx_symbol]
                idx_symbol += 1
            try:
                with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                    lines = r.readlines()
            except IOError:
                print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

            try:
                with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                    idx = 0
                    target_line_from = "\t\t\t<from>" + str(from_id) + "</from>"
                    target_line_to = "\t\t\t<to>" + str(to_id) + "</to>"
                    target_line_symbol = "\t\t\t<read>" + str(pre_symbol) + "</read>"
                    notation = "<!--This is sigma transition.-->"
                    while idx < len(lines):
                        if all is True:
                            if idx + 2 < len(lines) and target_line_from in lines[idx + 1] and target_line_to in lines[idx + 2]:
                                idx += 4
                            else:
                                w.write(lines[idx])
                        elif pre_symbol != '/sigma' and notation not in lines[idx]:
                            if idx + 3 < len(lines) and target_line_from in lines[idx + 1] and target_line_to in lines[idx + 2] and target_line_symbol in lines[idx + 3]:
                                idx += 4
                            else:
                                w.write(lines[idx])
                        elif pre_symbol == '/sigma' and idx + 1 < len(lines) and notation in lines[idx + 1]:
                            if idx + 3 < len(lines) and target_line_from in lines[idx + 1] and target_line_to in lines[idx + 2]:
                                idx += 4
                            else:
                                w.write(lines[idx])
                        else:
                            w.write(lines[idx])
                        idx += 1
            except IOError:
                print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))
            if all is True:
                print("Successfully delete all the transitions from state %d to state %d" % (from_id, to_id))
            else:
                print("Successfully delete the transition from state %d to state %d with symbol %s" % (from_id, to_id, pre_symbol))
            if all is True:
                break

    def del_transition_by_name(self, from_name, to_name, pre_symbols, all=False):
        """
        Delete the transition from start state to end state by using name to index.
        :param all: If all is True, then delete all the transition from start state to end state.
        :param from_name: The name of start state.
        :param to_name: The name of end state.
        :param pre_symbols: The symbols of transitions.
        :return: NULL
        """
        from_id = self.name_to_id(from_name)
        if from_id == NOT_FIND_NAME:
            print("Can't find %s in states!" % from_name)
            return
        elif from_id == MULTI_NAME:
            print("There are multiple %s in states" % from_name)
            return

        to_id = self.name_to_id(to_name)
        if to_id == NOT_FIND_NAME:
            print("Can't find %s in states!" % to_name)
            return
        elif to_id == MULTI_NAME:
            print("There are multiple %s in states" % to_name)
            return

        self.del_transition(from_id, to_id, pre_symbols, all)

    def change_state(self, id, initial=REMAINED, final=REMAINED):
        """
        Change the state whether be initial or be final or neither.
        :param id: The id of the state.
        :param initial: The state's initial condition
        :param final: The state's final condition
        :return: NULL
        """
        if id not in self.states:
            print("There is not id=%d in states" % id)
            return
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                lines = r.readlines()
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))
        if initial is not REMAINED:
            self.states[id].initial = initial
        if final is not REMAINED:
            self.states[id].final = final
        target_line = "<state id=\"" + str(id) + "\""
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                idx = 0
                while idx < len(lines):
                    line = lines[idx]
                    # print(line)
                    if target_line in line:  # modify the state
                        if initial is True:
                            lines[idx + 4] = "\t\t\t<initial/>&#13;"
                        elif initial is False:
                            lines[idx + 4] = "\n"
                        if final is True:
                            lines[idx + 5] = "\t\t\t<final/>&#13;"
                        elif final is False:
                            lines[idx + 5] = "\n"
                        for j in range(0, 7):
                            w.write(lines[idx])
                            idx += 1
                    else:
                        w.write(line)
                        # print(line)
                        idx += 1
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

    def change_state_by_name(self, name, initial=REMAINED, final=REMAINED):
        """
        Change the state's condition by using name to index.
        :param name: The name of the state.
        :param initial: The state's initial condition.
        :param final: The state's final condition.
        :return: NULL
        """
        id = self.name_to_id(name)
        if id == NOT_FIND_NAME:
            print("Can't find %s in states!" % name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %s in states" % name)
            return

        self.change_state(id, initial, final)

    def change_state_name(self, id, name=""):
        """
        Change the name of the state.
        :param id: The id of the state.
        :param name: The new name of the state.
        :return: NULL
        """
        if id not in self.states:
            print("There is not id=%d in states" % id)
            return
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                lines = r.readlines()
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

        old_name = self.states[id].name
        self.states[id].name = name
        target_line = "<state id=\"" + str(id) + "\""
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                idx = 0
                while idx < len(lines):
                    line = lines[idx]
                    if target_line in line:  # modify the name of the state
                        line = "\t\t<state id=\"" + str(id) + "\" name=\"" + name + "\">&#13;\n"
                        w.write(line)
                    else:
                        w.write(line)
                    idx += 1
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

        print("Successfully change the state %d from name '%s' to name '%s'!" % (id, old_name, name))

    def change_state_name_by_name(self, pre_name, new_name):
        """
        Change the name of the state by using name to index.
        :param pre_name: The old name of the state.
        :param new_name: The new name of the state.
        :return:
        """
        id = self.name_to_id(pre_name)
        if id == NOT_FIND_NAME:
            print("Can't find %s in states!" % pre_name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %s in states" % pre_name)
            return

        self.change_state_name(id, new_name)

    def change_state_label(self, id, label=""):
        """
        Change the label of the state.
        :param id: The id of the state.
        :param label: The new label of the state.
        :return: NULL
        """
        if id not in self.states:
            print("There is not id=%d in states" % id)
            return
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
                lines = r.readlines()
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))

        old_label = self.states[id].label
        target_line = "<state id=\"" + str(id) + "\""
        try:
            with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
                idx = 0
                while idx < len(lines):
                    line = lines[idx]
                    if target_line in line:  # modify the name of the state
                        lines[idx + 3] = "\n\t\t\t<label>" + label + "</label>&#13;\n"
                        for j in range(0, 7):
                            w.write(lines[idx])
                            idx += 1
                    else:
                        w.write(line)
                        # print(line)
                        idx += 1
        except IOError:
            print("Unsuccessfully open file %s" % (os.path.join(os.getcwd(), self.file_name)))
        print("Successfully change the state %d's label from \"%s\" to \"%s\" !" % (id, old_label, label))

    def change_state_label_by_name(self, name, label=""):
        """
        Change the label of the state by using name to index.
        :param name: The name of the state.
        :param label: The new label of the state.
        :return:
        """
        id = self.name_to_id(name)
        if id == NOT_FIND_NAME:
            print("Can't find %s in states!", name)
            return
        elif id == MULTI_NAME:
            print("There are multiple %s in states", name)
            return

        self.change_state_label(id, label)

    def change_transition(self, from_id, to_id, pre_symbols, new_symbols, all=False):  # realize delete first
        """
        Change the transition from start state to end state with new symbol.
        :param all: If all is True, then change all the transition from start state to end state.
        :param from_id: The id of start state.
        :param to_id: The id of end state.
        :param pre_symbols: The old symbols of transitions.
        :param new_symbols: The new symbols of transitions.
        :return:
        """

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
        self.del_transition(from_id, to_id, pre_symbols, all)
        self.add_transition(from_id, to_id, new_symbols)
        print("Successfully change the transition from state %d to state %d with symbol %s" % (from_id, to_id, new_symbols))

    def change_transition_by_name(self, from_name, to_name, pre_symbols, new_symbols, all=False):
        """
        CChange the transition from start state to end state with new symbol by using name to index.
        :param all: If all is True, then delete all the transition from start state to end state.
        :param from_name: The name of start state.
        :param to_name: The name of end state.
        :param pre_symbols: The old symbols of transition.
        :param new_symbols: The new symbols of transition.
        :return: NULL
        """
        from_id = self.name_to_id(from_name)
        if from_id == NOT_FIND_NAME:
            print("Can't find %s in states!" % from_name)
            return
        elif from_id == MULTI_NAME:
            print("There are multiple %s in states" % from_name)
            return

        to_id = self.name_to_id(to_name)
        if to_id == NOT_FIND_NAME:
            print("Can't find %s in states!" % to_name)
            return
        elif to_id == MULTI_NAME:
            print("There are multiple %s in states" % to_name)
            return

        self.change_transition(from_id, to_id, pre_symbols, new_symbols, all)


'''
test = Jflap("test")
test.create_file(os.getcwd())
test.add_state("q0","0,0", initial=True)
test.add_state("q1","1,2", final=True)
test.add_state("q2", "ready to be deleted", final=True, initial=True)
test.create_sigma(['0', '1', '2', '3', '4'])
test.add_transition(0, 1, ['0'])
test.add_transition(1, 0, ['2'])
test.add_transition(0, 1, ['1'])
test.add_transition(1, 2, ["/sigma"])
#test.add_transition(1, 0, "/sigma")

test.change_state(0, initial=False)
test.change_state(1, final=False)

test.change_state_label(1, "I am state 1")
#test.del_state(2)
#test.change_transition(0, 1, '0', '3')
#test.del_transition(0, 1, pre_symbols=[], all=True)
test.change_transition(0, 1, pre_symbols=[], new_symbols=['3', '4'], all=True)
#test.change_transition(1, 0, "2", '/sigma')
#test.del_transition(1, 0, '/sigma')
#print (test.file_name)
'''

'''
test = Jflap("test")
test.create_file(os.getcwd())
for i in range(0, 12):
    test.add_state(name=i)
test.change_state(0, initial=True)
test.change_state(11, final=True)
sigma = range(0, 10)
test.create_sigma(sigma)
for i in range(1, 11):
    test.add_transition(0, i, i)
    test.add_transition(i, i, "/sigma")
    test.add_transition(i, 11, i)
'''
'''
test = Jflap("2-14")
test.create_file(os.getcwd())
test.add_state("{q0}", initial=True)
test.add_state("{q0,q1}")
test.add_state("{q0,q2}", final=True)
test.create_sigma([0, 1])
test.add_transition_by_name("{q0}","{q0,q1}", 0)
test.add_transition_by_name("{q0,q1}", "{q0,q2}", 1)
test.add_transition_by_name("{q0,q1}", "{q0,q1}", 0)
test.add_transition_by_name("{q0}","{q0}", 1)
test.add_transition_by_name("{q0,q2}","{q0}", 1)
test.add_transition_by_name("{q0,q2}","{q0,q1}", 0)
'''