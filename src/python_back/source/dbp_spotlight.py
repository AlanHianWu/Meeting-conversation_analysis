import rdflib, spacy

class Sparql_query(object):
    
    def __init__(self, url):
        self.url = url
        self.sub = url[28:]
        try:
            self.graph = rdflib.Graph().parse(url)
        except Exception as e:
            # url = url[28:].replace('-', '_')
            # url = url.replace('_', '-')
            # url = url.replace('', '-')
            #
            print("Soarql error no graph: ", url,e)
            return None
 

    def get_abstract(self):
        # g.parse('http://dbpedia.org/resource/Human_capital')
        try:
            g = self.graph
            qres = g.query('''
                        prefix dbpedia: <http://dbpedia.org/resource/>
                        prefix dbpedia-owl: <http://dbpedia.org/ontology/>
                        select ?abstract where { 
                            dbpedia:'''+self.sub+''' dbpedia-owl:abstract ?abstract.
                            filter(langMatches(lang(?abstract),"en"))
                            }''')
            res = ''
            for i in qres:
                res += str(i)

            return res
        except Exception as e:
            return None

    def get_details(self):
        try:
            g = self.graph
            qres = g.query('''
                        prefix dbr: <http://dbpedia.org/resource/>
                        select ?Type where {
                            dbr:'''+self.sub+''' a ?Type} LIMIT 100'''
                            )
            res = ''
            for i in qres:
                res += str(i)
            return res

        except Exception as e:
            print("get_detail error: ", self.sub, e)
            return None

    def get_type(self):
        try:
            g = self.graph
            qres = g.query('''
                            prefix dbr: <http://dbpedia.org/resource/>
                            SELECT *
                            WHERE
                                {
                                    OPTIONAL { dbr:'''+self.sub+''' rdf:type ?RDFtype .} 
                                    OPTIONAL { dbr:'''+self.sub+''' dbo:type ?DBOtype .} 
                                }
                        ''')
            res = []
            for i in qres:
                res.append(i)
            return res
        except Exception as e:
            print("get_type error: ", self.sub, e)
            return None


def csv():
    import csv
    txt = ''
    with open('src/python_back/transcripts/Recording.csv') as f:
        reader = csv.reader(f)
        data = list(reader)

        for t in data:
            txt += ' ' + t[1]
    return txt

def transcript():
    txt = ''
    with open("src/python_back/transcripts/transcript_file.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            txt += line.strip()[12:]

    return txt

# v1
def get_time_csv(word):
    import csv
    with open('src/python_back/transcripts/Recording.csv') as f:
        reader = csv.reader(f)
        data = list(reader)

        for t in data:
            if word in t[1]:
                return t[0]

    return 'Not found'

# v1
def get_time_transcript(word):
    with open("transcript_file.txt", "r") as f:
        for line in f.readlines():
            line = line.strip()
            if word in line:
                return line[6:11]

    return 'Not found'

# v1
def get_times_transcript(entity):

    path = get_latest_transcript()

    all_times = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line[34:]) != 0 and entity in line:
                all_times.append(line[6:11])
    return " & ".join(all_times)



def dbp_nlp(txt, con):
    nlp = spacy.blank('en')
    nlp.add_pipe('dbpedia_spotlight', config={'confidence': con})

    return nlp(txt)

def dbp_get_resources(nlp_results):
    'goes trough the layers of results'
    data = []
    # for entity in identified in transcribe
    for ent in nlp_results.ents:
        '''return name, id, similarity score, types, raw'''
        data.append( (ent.text, ent.kb_id_, ent._.dbpedia_raw_result['@similarityScore'], ent._.dbpedia_raw_result["@types"], ent._.dbpedia_raw_result) )
    return data
    

def get_latest_transcript():
    import os, glob
    path = "src/python_back/transcripts/*"
    list_of_files = list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)

    return latest_file


def get_latest_summary():
    import os, glob
    path = "src/python_back/summaries/*"
    list_of_files = list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)

    return latest_file

def populate(meeting_name, nlp_results, transcript, summary, database=None):
    import database_link
    # populates the database
    if database == None:
        # print('Default DataBase')
        node_maker = database_link.dataBase("bolt://localhost:7687", "neo4j", "pass")
    else:
        node_maker = database_link.dataBase(database[0], database[1], database[2])
    
    # create base node
    baseID = node_maker.create_base_node(meeting_name)
    node_maker.add_transcript(baseID, transcript) # put transcript here
    node_maker.add_summary(baseID, summary) # put summary here

    for data in nlp_results:
        '''populate strategically'''

        # created base entity node
        entityID = node_maker.create_dbp_entity(data[0], data[1], data[2], get_times_transcript(data[0]))
        
        # Looks for links in the entity to grab more info to add to node
        resource = Sparql_query(data[1])
    
        node_maker.add_abstract(entityID, resource.get_abstract())
        types = resource.get_type()
        
        '''adding all the type url if not none'''
        if types != None and len(types) != 0:
            # print('getting types for', data[1][28:], entityID)
            for t in types:
                '''remove all none types in t'''
                t = [i for i in t if i]
                # print('getting type  ', t, '  for ', entityID)
                node_maker.add_types(entityID, ",".join(list(t)))
                
    
        node_maker.add_details(entityID, resource.get_details())
    
        node_maker.add_relation(baseID, entityID)
    
    node_maker.close()
        
    

    '''node triming, cluster similair nodes, ie AI will link to AI with relation same!'''
    # trim nodes

def main(name=None, dataBase=None):
    path = get_latest_transcript()
    s_path = get_latest_summary()

    txt = ''
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line[34:]) != 0:
                txt += line[34:] + '. '
    
    summ = ''
    with open(s_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) != 0:
                summ += line

    nlp_results = dbp_nlp(txt, 0.9)
    
    # data = dbp_get_resources(nlp_results)
    # print("data: ")
    # for d in data:
    #     print()
    #     for t in d:
    #         print(t)
    if name == None:
        populate('Meeting01', dbp_get_resources(nlp_results), txt, summ)
    else:
        populate(name, dbp_get_resources(nlp_results), txt, summ, dataBase)


def test(con):  
    path = get_latest_transcript()
    s_path = get_latest_summary()

    txt = ''
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line[34:]) != 0:
                txt += line[34:] + '. '
    
    summ = ''
    with open(s_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) != 0:
                summ += line

    nlp_results = dbp_nlp(txt, con)
    
    return nlp_results


    
    

if __name__ == "__main__":
    main()
    # test()

    
