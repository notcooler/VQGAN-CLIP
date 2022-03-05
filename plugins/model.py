
class Model:
    def __init__(self, name_, linkYAML_, linkCKPT_):
        self.name = name_
        self.linkYAML = linkYAML_
        self.linkCKPT = linkCKPT_
    
    def getName(self):
        return self.name
    
    def getLinks(self):
        a = []
        a.append(self.linkYAML)
        a.append(self.linkCKPT)
        return a