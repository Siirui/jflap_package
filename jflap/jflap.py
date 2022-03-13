import os.path

class state(object):
    def __init__(self, name, label="", initial=False, final=False):
        self.name = name
        self.label = label
        self.initial = False
        self.final = False
    def set_name(self, name):
        self.name = name
    def set_label(self, label=""):
        self.label = label
    def set_initial(self, initial=False):
        set.initial = initial
    def set_final(self, final=False):
        set.final = final

class Jflap(object):
    def __init__(self, file_name):
        self.file_name = file_name + ".jff"
        self.states = []
        self.sigma = []
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
    def add_state(self, name, label="", initial=False, final=False):
        new_state = state(name, label, initial, final)
        self.states.append(new_state)
        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
            #print(lines)
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            #print(lines)
            for line in lines:
                if "<!--The list of states.-->" in line: #append new state
                    #print("This is target line:\n" + line)
                    new_line = line + "\t\t<state id=\"" + str(len(self.states)-1) + "\" name=\"" + name + "\">&#13;"
                    new_line = new_line + "\n\t\t\t<x>0.0</x>&#13;"
                    new_line = new_line + "\n\t\t\t<y>0.0</y>&#13;"
                    new_line = new_line + "\n\t\t\t<label>" + label + "</label>&#13;"
                    if initial is True:
                        new_line = new_line + "\n\t\t\t<initial/>&#13;"
                    if final is True:
                        new_line = new_line + "\n\t\t\t<final/>&#13;"
                    new_line = new_line + "\n\t\t</state>&#13;\n"
                    w.writelines(new_line)
                else:
                    #print("This is normal line:\n" + line)
                    w.write(line)
    def add_transition(self, from_id, to_id, symbol):
        if symbol != "\sigma":
            if symbol not in self.sigma:
                self.sigma.append(symbol)
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
                        for sym in self.sigma:
                            new_line = new_line + "\t\t<transition>&#13;"
                            new_line = new_line + "\n\t\t\t<from>" + str(from_id) + "</from>&#13;"
                            new_line = new_line + "\n\t\t\t<to>" + str(to_id) + "</to>&#13;"
                            new_line = new_line + "\n\t\t\t<read>" + str(sym) + "</read>&#13;"
                            new_line = new_line + "\n\t\t</transition>&#13;\n"
                        w.write(new_line)
                else:
                    w.write(line)
    def change_state(self, id, initial=-1, final=-1):
        with open(os.path.join(os.getcwd(), self.file_name), mode="r+", encoding="utf-8") as r:
            lines = r.readlines()
            # print(lines)
        target_line = "<state id=\"" + str(id) + "\""
        with open(os.path.join(os.getcwd(), self.file_name), mode="w", encoding="utf-8") as w:
            for i in range(len(lines)):
                line = lines[i]
                if target_line in line:  # modify the state
                    new_line =


test = Jflap("test")
test.create_file(os.getcwd())
test.add_state("q0","0,0", initial=True)
test.add_state("q1","1,2", final=True)
test.add_transition(0, 1, '0')
test.add_transition(0, 1, '2')
test.add_transition(0, 1, '1')
test.add_transition(1, 0, "\sigma")

#print (test.file_name)

