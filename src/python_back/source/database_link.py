from neo4j import GraphDatabase

class dataBase(object):
 
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.res = []

    def close(self):
        self.driver.close()
            
    def create_node(self, name):
        with self.driver.session() as session:
            node = session.write_transaction(self._create_node, name)
    
    def add_relation(self, nodeID1, nodeID2):
        with self.driver.session() as session:
            node = session.write_transaction(self._add_relation, nodeID1, nodeID2)
    
    def create_dbp_entity(self, name, link, score, time):
        with self.driver.session() as session:
            node = session.write_transaction(self._create_dbp_node_entity, name, link, score, time)
            '''returns (name, ID)'''
            return node
            
    '''New node types'''
    
    def add_abstract(self, nodeID, text):
        if text and len(text) > 0:
            with self.driver.session() as session:
                node = session.write_transaction(self._add_abstract, nodeID, text)
    
    def add_transcript(self, nodeID, text):
        with self.driver.session() as session:
            node = session.write_transaction(self._add_transcript, nodeID, text)

    def add_summary(self, nodeID, text):
        with self.driver.session() as session:
            node = session.write_transaction(self._add_summary, nodeID, text)
    
    def add_types(self, nodeID, text):
        if text and len(text) > 0:
            with self.driver.session() as session:
                node = session.write_transaction(self._add_types, nodeID, text)
        
    def add_details(self, node, text):
        if text and len(text) > 0:
            with self.driver.session() as session:
                node = session.write_transaction(self._add_details, node, text)
            
    # working on it!
    def create_base_node(self, meeting_id):
        with self.driver.session() as session:
            node = session.write_transaction(self._create_base_node, meeting_id)
            return node
            
    # @staticmethod
    def _create_base_node(self, tx, meeting_id):
        query = ("CREATE (a:Meeting) "
                        "SET a.name = $meeting_id "
                        "RETURN a.name AS name, id(a) AS ID")
        res = tx.run(query, meeting_id=meeting_id)
        return [(n['name'], n['ID']) for n in res][0]
     

        
    @staticmethod
    def _add_details(tx, nodeID, text):
        query = ("CREATE (a:Details) "
                        "SET a.details = $text "
                        "RETURN id(a) AS ID")
        iden = tx.run(query, text=text)
        iden = [i['ID'] for i in iden][0]
    
        query = (
               "MATCH (a:Details) "
               "WITH a "
               "MATCH (b:Entity) "
               "WHERE id(a) = $iden AND b.name = $node1 AND id(b) =$node2 "
               "MERGE (a)-[r: Details]->(b)"
               )
        tx.run(query, iden=iden, node1=nodeID[0], node2=nodeID[1])
    
    @staticmethod
    def _add_types(tx, nodeID, text):
        query = ("CREATE (a:Types) "
                        "SET a.types = $text "
                        "RETURN id(a) AS ID")
        iden = tx.run(query, text=text)
        iden = [i['ID'] for i in iden][0]

        query = (
               "MATCH (a:Types) "
               "WITH a "
               "MATCH (b:Entity) "
               "WHERE id(a) = $iden AND b.name = $node1 AND id(b) =$node2 "
               "MERGE (a)-[r: Type]->(b)"
               )
        tx.run(query, iden=iden, node1=nodeID[0], node2=nodeID[1])
        
    @staticmethod
    def _add_transcript(tx, nodeID, text):
        
        query = ("CREATE (a:Transcript) "
                        "SET a.text = $text "
                        "RETURN id(a) AS ID")
        iden = tx.run(query, text=text)
        iden = [i['ID'] for i in iden][0]
    
        query = (
               "MATCH (a:Transcript) "
               "WITH a "
               "MATCH (b:Meeting) "
               "WHERE id(a) = $iden AND b.name = $node1 AND id(b) = $node2 "
               "MERGE (a)-[r: transcript]->(b)"
               )
        tx.run(query, iden=iden, node1=nodeID[0], node2=nodeID[1])
    
    @staticmethod
    def _add_summary(tx, nodeID, text):
        query = ("CREATE (a:Summary) "
                        "SET a.text = $text "
                        "RETURN id(a) AS ID")
        iden = tx.run(query, text=text)
        iden = [i['ID'] for i in iden][0]
    
        query = (
               "MATCH (a:Summary) "
               "WITH a "
               "MATCH (b:Meeting) "
               "WHERE id(a) = $iden AND b.name = $node1 AND id(b) = $node2 "
               "MERGE (a)-[r: summary]->(b)"
               )
        tx.run(query, iden=iden, node1=nodeID[0], node2=nodeID[1])

    
    @staticmethod
    def _add_abstract(tx, nodeID, text):        
        query = ("CREATE (a:Abstract) "
                        "SET a.text = $text "
                        "RETURN id(a) AS ID")
        iden = tx.run(query, text=text)
        iden = [i['ID'] for i in iden][0]
    
        query = (
               "MATCH (a:Abstract) "
               "WITH a "
               "MATCH (b:Entity) "
               "WHERE id(a) = $iden AND b.name = $name AND id(b) = $idb "
               "MERGE (a)-[r: abstract]->(b)"
               )
        tx.run(query, iden=iden, name=nodeID[0], idb=nodeID[1])

    @staticmethod
    def _add_relation(tx, nodeID1, nodeID2):

        query = (
               "MATCH (a:Meeting) "
               "WITH a "
               "MATCH (b:Entity) "
               "WHERE a.name = $name1 AND id(a) = $iden AND b.name = $name2 AND id(b) = $idb "
               "MERGE (a)-[r: isEntityof]->(b)"
               )
        
        tx.run(query, name1=nodeID1[0], iden=nodeID1[1], name2=nodeID2[0], idb=nodeID2[1])
    
    @staticmethod
    def _create_node(tx, name):
        query = ("CREATE (a:Node) "
                        "SET a.name = $name "
                        "RETURN a.name + ', from node ' + id(a)")
        tx.run(query, name=name)
    
    # @staticmethod
    def _create_dbp_node_entity(self, tx, name, link, score, time):
        query = ("CREATE (a:Entity) "
                        "SET a.name = $name "
                        "SET a.link = $link "
                        "SET a.score = $score "
                        "SET a.time = $time "
                        "RETURN a.name AS name, id(a) AS ID")
        res = tx.run(query, name=name, link=link, score=score, time=time)
        
        return [(n['name'], n['ID']) for n in res][0]

        


if __name__ == "__main__":
    node_maker = dataBase("bolt://localhost:7687", "neo4j", "pass")
    
    nid = node_maker.create_dbp_entity("test", "test", "test", "test")
    print(nid)
    baseID = node_maker.create_base_node('meeting1')
    node_maker.add_abstract(nid, "test")
    node_maker.add_types(nid, "test")
    node_maker.add_details(nid, "test")

    node_maker.add_transcript(baseID, 'test')
    node_maker.add_summary(baseID, 'test')
    
    node_maker.add_relation(baseID, nid)
    # print("nid", [n for n in nid], nid)
   

   
    node_maker.close()







