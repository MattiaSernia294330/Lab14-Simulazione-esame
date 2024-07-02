from dataclasses import dataclass
@dataclass
class Connessione():
    c1:int
    c2:int
    GeneID1:str
    GeneID2:str
    esp:float

    def __hash__(self):
        return hash(f"{self.c1}{self.c2}{self.GeneID1}{self.GeneID2}")
    def __str__(self):
        return f"{self.c1}-->{self.c2}: {self.esp}"