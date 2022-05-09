import unittest, time, string, math


class TranscriptTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TranscriptTest, self).__init__(*args, **kwargs)
        self.zoom = self.csv()
        self.deep = self.deep_transcript()
        self.google = self.google_transcript()
    
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))
    
    def test_standard_google1(self):
        self.assertEqual(1, 1) 
        self.documentSimilarity(self.zoom, self.google)
    
    def test_standard_google2(self):
        self.assertEqual(1, 1) 
        self.documentSimilarity(self.deep, self.google)
    
    def test_standard_zoom1(self):
        self.assertEqual(1, 1) 
        self.documentSimilarity(self.deep, self.zoom)
    
    def test_standard_google3(self):
        self.assertAlmostEqual(self.documentSimilarity(self.zoom, self.google), self.documentSimilarity(self.deep, self.google))
  
    def test_standard_zoom3(self):
        self.assertAlmostEqual(self.documentSimilarity(self.google, self.zoom), self.documentSimilarity(self.deep, self.zoom))

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
        
    def csv(self):
        import csv
        txt = ''
        with open('src/python_back/transcripts/Recording.csv') as f:
            reader = csv.reader(f)
            data = list(reader)

            for t in data:
                txt += ' ' + t[1]
        return txt

    def deep_transcript(self):
        txt = ''
        with open("src/python_back/transcripts/deep-speech_transcript_file.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                txt += line.strip()[12:]

        return txt

    def google_transcript(self):
        txt = ''
        with open("src/python_back/transcripts/google_transcript_file.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                txt += line.strip()[34:]

        return txt

def set_vad_level():
    pass


def lastest_scripts():
    from os import listdir
    from os.path import isfile, join
    mypath = "src/python_back/transcripts"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    transripts = []
    for transript in onlyfiles:
        if transript.endswith("txt"):
            transripts.append(transript)

    return transripts

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TranscriptTest)
    unittest.TextTestRunner(verbosity=0).run(suite)