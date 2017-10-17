import sys
from os.path import join as path_join
from os.path import dirname as dir_name
import json
from collections import OrderedDict

from bs4 import BeautifulSoup


def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        val = unicode_or_str.encode('utf-8')
    else:
        val = unicode_or_str
    return val


def remove_n_t(text):
    text = text.replace('\n', '')
    text = text.replace('\t', ' ')
    text = ' '.join(text.split())
    return text


class HtmlTableParser(object):
    def __init__(self, html_file):
        self.html_file = html_file
        self.json_file = path_join(dir_name(html_file), 'question.json')
        self.image_dir = dir_name(html_file)

    def reader(self):
        fp = open(self.html_file)
        html = BeautifulSoup(fp, "html.parser")
        with open(self.json_file, 'w') as j_f:
            for table in html.find_all('table'):
                #out = json.dumps(read_table(table))
                #j_f.write(out + '\n')
                json.dump(self.__read_table(table), j_f, indent=4)

    def __read_table(self, table):
        question_dict = OrderedDict()
        rows = table.find_all('tr')
        for row in rows:
            cln = row.find_all('td')
            key = question_key = remove_n_t(to_str(cln[0].text))
            val = question_val = {'text': remove_n_t(to_str(cln[1].text))}
            if cln[1].img:
                val['image'] = path_join(self.image_dir, to_str(cln[1].img['src']))
            question_dict[key] = val
        return question_dict

if __name__ == '__main__':
    file_name = sys.argv[1]
    htp = HtmlTableParser(file_name)
    htp.reader()

    
    
