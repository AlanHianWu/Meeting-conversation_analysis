from itertools import count
import re

from neo4j import GraphDatabase
from collections import Counter

'''better take base node and analysis from that?'''
class Analysis(object):

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()


    '''should use node based tracking'''

    def most_frequent_words(self, meeting_name, c):
        with self.driver.session() as session:
            query = (
               "MATCH (a:Transcript)-[r:transcript]->(b:Meeting) "
               "where b.name = '"+meeting_name+
               "' RETURN a.text AS text"
               )

            result = session.run(query)
            
            txt = [r['text'] for r in result]
            
            count = Counter(txt[0].split())

        return count.most_common(c)
    
 
    def meeting_context():
        '''what was the meeting about'''
        
        
        pass
    
    def context_finder(self, n):
        '''when was node in meeting mentioned'''
        with self.driver.session() as session:
            query = (
                "MATCH (p:Entity) "
                "WHERE p.name = '"+n+
                "' RETURN p.time AS time"
            )
            result = session.run(query)
            
            res = [r['time'] for r in result]
            return res
       
    
    def node_frequency(self):
        '''how many times the nodes in meeting'''
        with self.driver.session() as session:
            query = (
                "MATCH (p:Entity) "
                "WITH p.name as name,COUNT(p) as count "
                "WHERE count>1 "
                "RETURN name, count"
            )
            result = session.run(query)
            
            res = [(r['name'], r['count']) for r in result]
            return res
    
    def all_topics(self):
        '''return all entity mentioned'''
        with self.driver.session() as session:
            query = (
                "MATCH (p:Entity) "
                "WITH p.name as name,COUNT(p) as count "
                "WHERE count>0 "
                "RETURN name, count"
            )
            result = session.run(query)
            
            res = [(r['name'], r['count']) for r in result]
            return res
        
    
    def top_topics(self):
        '''top types'''
        with self.driver.session() as session:
            query = (
                "MATCH (p:Types) "
                "WITH p.types as types,COUNT(p) as count "
                "WHERE count>1 "
                "RETURN types, count"
            )
            result = session.run(query)

            res = [(r['types'], r['count']) for r in result]
            return res
    

    def hot_topics(self):
        '''what was disscused at the same time'''
        '''top types high frequency'''
        with self.driver.session() as session:
            query = (
                "MATCH (p:Entity) "
                "WITH p.types as types, COUNT(p) as count "
                "WHERE count>1 "
                "RETURN types, count"
            )
            result = session.run(query)

            res = [(r['types'], r['count']) for r in result]
            return res
        pass
    
    def top_topic_time_stamps():
        '''what meeting discused types'''
        '''return time stamps for topic'''
        pass



def main():
    ana = Analysis("bolt://localhost:7687", "neo4j", "pass")
    
    print("node frequency  ", ana.node_frequency())
    print("all topics  ", ana.all_topics())
    tup = ana.top_topics()
    print("top topics  ", sorted(tup, key = lambda x: x[1])[:10])

    print("most frequent words  ", ana.most_frequent_words('Meeting01', 40))
    
    print("find context Dublin  ", ana.context_finder('Dublin'))
        
    ana.close()


if __name__ == '__main__':
    main()

