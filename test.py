import xml.etree.ElementTree as ET;

class Probability:
    def __init__(self,fore,given):
        self.fore = fore;
        self.given = given;
    def __eq__(self, other):
        return self.fore == other.fore and self.given == other.given;
    def __hash__(self):
        return self.fore.__len__();


def readdata(filename = ''):
    root = ET.parse(filename).getroot();
    data = dict();
    for definition in root.iter('DEFINITION'):
        fore = '';
        given = [];
        pro = [];
        for child in definition:
            if(child.tag == 'FOR'):
                fore = child.text;
            if(child.tag == 'GIVEN'):
                given.append(child.text);
            if(child.tag == 'TABLE'):
                table = child.text;
                pro = table.strip().split();
                givensize = given.__len__();
                for i in range(len(pro) // 2):
                    cur_fore_1 = fore.lower();
                    cur_fore_2 = '!'+fore.lower();
                    cur_given = [];
                    tmp = i;
                    for g in range(givensize):
                        if(tmp%2 == 0):
                            cur_given.append(given[givensize-1-g].lower());
                        elif(tmp%2 == 1):
                            cur_given.append('!'+given[givensize-1-g].lower());
                        tmp = tmp>>1;
                    cur_given.reverse();
                    p1 = Probability(cur_fore_1,set(cur_given));
                    p2 = Probability(cur_fore_2,set(cur_given));
                    p1.fore = cur_fore_1;
                    p1.given = set(cur_given);
                    p1.pro = pro[i*2+0];
                    p2.fore = cur_fore_2;
                    p2.given = set(cur_given);
                    p2.pro = pro[i*2+1];
                    data[p1] = float(pro[i*2+0]);
                    data[p2] = float(pro[i*2+1]);
    return data;

data = readdata('dog-problem.xml')
p1 = Probability('a',{'b','!e'});
# for key,value in data.items():
#     print(key.fore,'|',key.given,value);
