from id_mapper.metanetx import load_xrefs
from id_mapper.graph import insert_pairs

if __name__ == '__main__':
    for pairs in load_xrefs('chem_xref'):
        insert_pairs('Metabolite', *pairs)
    for pairs in load_xrefs('reac_xref'):
        insert_pairs('Reaction', *pairs)
