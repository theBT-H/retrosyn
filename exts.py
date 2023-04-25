import pymysql
from rdkit import Chem
db = pymysql.connect(host="localhost", user="root", password="4613845822", database="retrosys", charset="utf8")



def is_smiles(smiles_str):
    mol = Chem.MolFromSmiles(smiles_str)
    return mol is not None