from neo_interface import neo
import json
import requests

def get_and_write_identifiers(n):
    identifiers = n.get_node_ids()
    with open('original_ids','w') as outf:
        for i in identifiers:
            outf.write(f'{i}\n')


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def normalize(batch):
    response = requests.post('https://nodenormalization-sri.renci.org/get_normalized_nodes',json={'curies':batch})
    return response.json()


def normalize_identifiers():
    old = []
    originals={}
    with open('original_ids','r') as inf:
        for line in inf:
            o = line.strip()
            l = o
            if o.startswith('NCBIGene'):
                l = f'NCBIGENE:{l.split(":")[-1]}'
            if o.startswith('KEGG:'):
                l = f'KEGG.COMPOUND:{l.split(":")[-1]}'
            if o.startswith('http::_www.ebi.ac.uk_efo_'):
                l = l.split('_')[-1]
            old.append(l)
            originals[l] = [o]
    BATCH_SIZE = 1000
    nb = 0
    N = len(old)/BATCH_SIZE
    with open('translation','w') as outf:
        for batch in chunks(old, BATCH_SIZE):
            nb += 1
            print(f'{nb} / {N}')
            batch_done = normalize(batch)
            for k,v in batch_done.items():
                if v is None:
                    outf.write(f"{originals[k]}\t{k}\tNone\n")
                else:
                    newid = v['id']['identifier']
                    oldid = originals[k]
                    if oldid != newid:
                        outf.write(f"{oldid}\t{k}\t{newid}\n")

def go():
    with open('conn.json', 'r') as inf:
        conn_data = json.load(inf)
    n = neo(conn_data['neouri'], conn_data['neouser'], conn_data['neopass'])
    #get_and_write_identifiers(n)
    normalize_identifiers()

if __name__ == '__main__':
    go()