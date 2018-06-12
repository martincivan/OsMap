

class Zaznam:

    def __init__(self, zaznam):
        self.typ = zaznam.attrib['type']
        self.popis = zaznam.attrib['description']
        self.mbzipu = zaznam.attrib['size']
        self.mbsuboru = zaznam.attrib['targetsize']
        self.velkost = zaznam.attrib['contentSize']
        self.velkostzipu = zaznam.attrib['containerSize']
        self.cas = zaznam.attrib['timestamp']
        self.subor = zaznam.attrib['name']
