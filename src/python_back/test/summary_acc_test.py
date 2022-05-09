import unittest, time, string, math

class TranscriptTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TranscriptTest, self).__init__(*args, **kwargs)
        self.summary1 = self.summary_txt1()
        self.summary2 = self.summary_txt2()
    
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_summary(self):
        print(self.documentSimilarity(self.summary_txt1, self.summary_txt2))

    # returns a list of the words
    # in the file
    def get_words_from_line_list(self, text): 
        translation_table = str.maketrans(string.punctuation+string.ascii_uppercase,
                                        " "*len(string.punctuation)+string.ascii_lowercase)

        text = text.translate(translation_table)
        word_list = text.split()
        
        return word_list


    def count_frequency(self, word_list): 
        
        D = {}
        for new_word in word_list:
            if new_word in D:
                D[new_word] = D[new_word] + 1
            else:
                D[new_word] = 1
                
        return D
    

    def word_frequencies_for_file(self, filename): 
        
        line_list = filename
        word_list = self.get_words_from_line_list(line_list)
        freq_mapping = self.count_frequency(word_list)
        
        return freq_mapping

    # returns the dot product of two documents
    def dotProduct(self, D1, D2): 
        Sum = 0.0
        
        for key in D1:
            
            if key in D2:
                Sum += (D1[key] * D2[key])
                
        return Sum
    
    # returns the angle in radians 
    # between document vectors
    def vector_angle(self, D1, D2): 
        numerator = self.dotProduct(D1, D2)
        denominator = math.sqrt(self.dotProduct(D1, D1)*self.dotProduct(D2, D2))
        
        return math.acos(numerator / denominator)
    
    
    def documentSimilarity(self, file1, file2):
    
        sorted_word_list_1 = self.word_frequencies_for_file(file1)
        sorted_word_list_2 = self.word_frequencies_for_file(file2)
        distance = self.vector_angle(sorted_word_list_1, sorted_word_list_2)
        
        # print("The distance between the documents is: % 0.6f (radians)"% distance)
        return distance
        
  

    def summary_txt1(self):
        txt = ''
        with open("src/python_back/summaries/summary03.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                txt += line.strip()

        return txt

 
    def summary_txt2(self):
        txt = ''
        with open("src/python_back/summaries/summary04.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                txt += line.strip()

        return txt

def lastest_summary():
    from os import listdir
    from os.path import isfile, join
    mypath = "src/python_back/summaries"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    transripts = []
    for transript in onlyfiles:
        if transript.endswith("txt"):
            transripts.append(transript)

    return transripts

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TranscriptTest)
    unittest.TextTestRunner(verbosity=0).run(suite)