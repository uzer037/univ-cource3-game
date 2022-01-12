import json
from time import sleep
import keyboard as kb
import tkinter as tk

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

    def export(self):
        global currNode, tbox
        if currNode != None:
            currNode.pre = tbox.get(1.0, tk.END)

        with open(self.path, encoding='utf-8', mode='w') as f:
            txt = json.dumps(self.nodes, default=Node.toDict, ensure_ascii=False)
            while '\n\n' in txt:
                txt.replace('\n\n','\n')
            f.write(txt)
            print("Exported successfuly")

    def get(self, tag):
        for n in self.nodes:
            if n.tag == tag:
                return n
        return None

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

def tagCallback(tag):
    global s, currNode, nnb, tbox, pre
    n = s.get(tag.get())
    if n != None:
        currNode = n
        nnb.config(text='Обновить')
        tbox.config(state='normal')
        tbox.delete(1.0, "end")
        tbox.insert(1.0, currNode.pre)
        redrawVariants()
    else:
        if(currNode != None):
            currNode.pre = tbox.get(1.0, tk.END)
            currNode = None
        tbox.config(state='normal')
        tbox.delete("1.0", "end")
        tbox.insert(1.0, "")
        nnb.config(text='Создать')
        tbox.config(state='disabled')
        redrawVariants()

def vartagCallback(tbox, n):
    currNode.ch[n]["tag"] = tbox.get()

def varnameCallback(tbox, n):
    currNode.ch[n]["name"] = tbox.get()

def delVariant(n):
    global currNode
    if currNode != None:
        del currNode.ch[n]
        redrawVariants()

def addVariant():
    global currNode
    if currNode != None:
        currNode.ch.append(Node.Choise("").toDict())
        redrawVariants()

def redrawVariants():
    global s, currNode, vframe
    for w in vframe.winfo_children():
        w.destroy()
    if currNode != None:
        n = 0
        for v in currNode.ch:
            tmps = tk.StringVar()
            tmps.set(v["tag"])
            tmps.trace("w", lambda name, index, mode, tmps=tmps, n=n: vartagCallback(tmps, n))
            tmpf = tk.Frame(vframe)
            tk.Entry(tmpf, width=9, textvariable=tmps).pack(side=tk.LEFT)
            tmpf.pack()

            tmp2s = tk.StringVar()
            tmp2s.set(v["name"])
            tmp2s.trace("w", lambda name, index, mode, tmps=tmp2s, n=n: varnameCallback(tmps, n))
            tk.Entry(tmpf, width=50, textvariable=tmp2s).pack(side=tk.LEFT)
            tmpf.pack()
            tk.Button(tmpf, text="x", command=lambda n=n: delVariant(n)).pack()

            n += 1
        tk.Button(vframe, text="+", command=lambda: addVariant()).pack(anchor=tk.SW)

def updNode():
    global s, tag, currNode
    if tag.get() != "":
        if currNode != None:
            s.export()
        else:
            currNode = Node({"tag": str(tag.get()),"pre": "","ch": []})
            s.nodes.append(currNode)
            redrawVariants()
            tagCallback(tag)

def main():
    global printDelay, s, currNode, nnb, tbox, pre, vframe, tag
    s = Serializer('data.json')

    currNode = None
    nodes = s.load()
    s.export()
    root = tk.Tk()
    root.geometry("800x300")
    root.bind('<Control-s>', lambda event: s.export())
    body = tk.Frame(root)
    body.pack()

    vframe = tk.Frame(body)

    tag = tk.StringVar()
    tag.trace("w", lambda name, index, mode, tag=tag: tagCallback(tag))
    #   layout
    idroot = tk.Frame(body)
    idroot.pack()

    tagInp = tk.Entry(idroot, width=10, textvariable=tag)
    tagInp.pack(side = tk.LEFT)

    nnb = tk.Button(idroot, text="New Node")
    nnb.pack()

    tbox = tk.Text(body, height=8, width=300)
    tbox.pack()

    vframe.pack(anchor=tk.W)
    root.bind('<Control-d>', lambda event: addVariant())
    root.bind('<Control-f>', lambda event: tagInp.focus())

    nnb.config(text='Создать', command=updNode)
    tbox["state"]=tk.DISABLED
    root.lift()
    root.call('wm', 'attributes', '.', '-topmost', True)
    root.mainloop()

if __name__ == '__main__':
    main()
