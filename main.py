import json
from time import sleep
import keyboard as kb

class Node:
    def __init__(self, data):
        self.__dict__ = data

    def setPreText(self, s):
        self.pre = s

    class Choise:
        def __init__(self, nextTag):
            self.tag = nextTag
            self.name = ''
            self.pre = ''

        def toDict(self):
            return self.__dict__

    def toDict(self, el=None):
        if isinstance(el, Node) or el == None:
            return self.__dict__
        else:
            raise TypeError("Unexpected type {0}".format(el.__class__.__name__))

class Serializer:
    def __init__(self, path):
        self.path = path;
        self.nodes = []

    def load(self):
        tmp = ""
        self.nodes = []
        with open(self.path, encoding='utf-8') as f:
            data = json.load(f)
            for d in data:
                self.nodes.append(Node(d))

        return self.nodes

    def export(self, nodes):
        with open(self.path, encoding='utf-8', mode='w') as f:
            f.write(json.dumps(nodes, default=Node.toDict, ensure_ascii=False))

    def get(self, tag):
        for n in self.nodes:
            if n.tag == tag:
                return n
        raise ReferenceError("No node with {0} tag found".format(tag))

defPrintDelay = 0.005
printDelay = 0.005

def wait(t):
    if not kb.is_pressed("shift"):
        sleep(t)


def sprint(s, end='\n'):
    global printDelay, defPrintDelay
    i = 0
    while i < len(s):
        if s[i] == '<':
            j = 0
            while i+j < len(s) and s[i+j] != '>':
                j += 1
            if s[i+j] == '>':
                tag = s[i+1:i+j]
                if '=' in tag:
                    tname, val = tag.split('=')
                else:
                    tname = tag
                    val = None
                #Tag management
                if tname == 'd':
                    printDelay = float(val)
                elif tname == '/d':
                    printDelay = float(defPrintDelay)
                elif tname == 'br':
                    print('\n', end='', flush=True)
                elif tname == 'p':
                    wait(float(val))
                #
            i += j
        else:
            wait(printDelay)
            print(s[i], end='', flush=True)
        i += 1
    print('', end=end)


def main():
    global printDelay
    s = Serializer('data.json')

    nodes = s.load()
    tag = '0:0'
    while(tag[0] != 'E'):
        n = s.get(tag)
        if n.pre != None:
            sprint(n.pre)
        if n.ch != None:
            inp = 'h'
            while not inp.isdigit() or int(inp) <= 0 or int(inp) > len(n.ch):
                i = 0
                for c in n.ch:
                    i += 1
                    wait(printDelay)
                    sprint(str(i) + ") " + c["name"])
                inp = input('\n> ')
                if inp.isdigit() and int(inp) > 0 and int(inp) <= len(n.ch):
                    tag = n.ch[int(inp)-1]["tag"]
    if(tag[0] == 'E'):
        n = s.get(tag)
        if(n != None):
            sprint(n.pre)

    print('Поздравляем! Игра окончена.')
    input()

if __name__ == '__main__':
    main()
