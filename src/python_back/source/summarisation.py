from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")


# tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")

torch_device = 'cpu'

def bart_summarize(text, num_beams, length_penalty, max_length, min_length, no_repeat_ngram_size):
    text_input_ids = tokenizer.batch_encode_plus([text], return_tensors='pt', max_length=1024, truncation=True)['input_ids'].to(torch_device)
    summary_ids = model.generate(text_input_ids, num_beams=int(num_beams), length_penalty=float(length_penalty), max_length=int(max_length), min_length=int(min_length), no_repeat_ngram_size=int(no_repeat_ngram_size))           
    summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True, )

    return summary_txt

        
def get_latest_transcript():
    import os, glob
    path = "src/python_back/transcripts/*"
    list_of_files = list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)

    return latest_file


def summary():
    path = get_latest_transcript()

    lst = []
    min_len = 140

    with open(path, "r") as f:
        lines = f.readlines()
        txt = ''

        for line in lines:
            summ = ''
            '''remove timestamp'''
            line = line[34:].strip()
            if len(line) != 0:
                # print("len txt : ", len(txt), txt)
                
                if len(line) < min_len:
                    txt += line + ". "
                
                elif min_len < len(txt):
                    
                    s = truncate_summ(txt)
                    if summ != s:
                        summ += s + ". "
                        # print('txt:  ', 'line ', len(line), summ)
                        lst.append(summ)
                        txt = ''
                
                elif min_len < len(line) :
                    
                    s = truncate_summ(line)
                    if summ != s:
                        summ += s + ". "
                        # print('summ:  ', 'line ', len(line), summ)
                        lst.append(summ)

                print('End Sum: ', lst)
    return lst


def truncate_summ(line):
    import copy

    min_len = 140
    max_len = 150

    if len(line) != 0:

        if min_len < len(line):
            # too big cut down and add to next
            L = line.strip().split()

            for i in range(-1, (len(L))*-1, -1):
                #smart truncate
                new_l = " ".join(L[:i])
            
                if len(new_l) < min_len:
                    
                    R = copy.deepcopy(" ".join(L[i:]))
                    L = copy.deepcopy(" ".join(L[:i]))
                    # print('L check:  ', L)
                    # print('R check:  ', R)
                    '''no repeat grams too low makes it dream'''                
                    # print("L:  ", L)
                    # print("R:  ", R)
                    # print("b:  ", b)

                    return bart_summarize(L, 4, 2, max_len, min_len, 5) + ". " + truncate_summ(R)+ ". "
    

    return ''
    
    

if __name__ == '__main__':

    with open("src/python_back/summaries/summary01.txt", 'a') as f:
        res = summary()
        # for line in res:
        #     f.write(line)

        for line in res:
            f.write(line[0])


    # txt = "The town of Borodyanka may have faced some the worst attacks since Russia launched its invasion of Ukraine."*5
    # print("start size: ", len(txt.split()))
    # print("truncate: ", truncate_summ(txt))
    

