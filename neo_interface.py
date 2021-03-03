from neo4j import GraphDatabase

class neo():
    def __init__(self,uri,user,pw):
        if user == '':
            self.driver = GraphDatabase.driver(uri)
        else:
            self.driver = GraphDatabase.driver(uri, auth=(user,pw))

    def run_query(self,q):
        with self.driver.session() as session:
            res = session.read_transaction(rq,q)
        return res

    def get_node_ids(self):
        with self.driver.session() as session:
            friends = session.read_transaction(query_node_ids)
        return friends

def rq(tx,cypher):
    result = tx.run(cypher)
    results = [ r['output'] for r in result ]
    return results

def ex(tx,cypher):
    result = tx.run(cypher)
    for record in result:
        return record

def query_node_ids(tx):
    identifiers = []
    q = f"MATCH (a)" \
         "where not a:Concept and not a:SequenceVariant " \
         "RETURN a.id"
    result = tx.run(q)
    for record in result:
        identifiers.append(record['a.id'])
    return identifiers
