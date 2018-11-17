import xml.etree.ElementTree as ET;

class Probability:
    def __init__(self,fore,given):
        self.fore = fore;
        self.given = given;
    def __eq__(self, other):
        return self.fore == other.fore and self.given == other.given;
    def __hash__(self):
        return self.fore.__len__();
    def __str__(self):
        return self.fore + ' | ' + str(self.given)

def readdata(filename = ''):
    root = ET.parse(filename).getroot();
    data = dict();
    parents = dict();
    for definition in root.iter('DEFINITION'):
        fore = '';
        given = [];
        pro = [];
        for child in definition:
            if(child.tag == 'FOR'):
                fore = child.text;
            if(child.tag == 'GIVEN'):
                given.append(child.text.lower());
            if(child.tag == 'TABLE'):
                table = child.text;
                pro = table.strip().split();
                givensize = given.__len__();
                for i in range(len(pro) // 2):
                    cur_fore_1 = fore.lower();
                    cur_fore_2 = '!'+fore.lower();
                    if (i == 0):
                        parents[cur_fore_1] = given;
                        parents[cur_fore_2] = given;
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
    return data,parents;

def Prob(fore='',parents={},data = {},event = []):
    given = set(parents[fore]);
    for g in given:
        if ('!' + g) in event:
            given.discard(g);
            given.add('!' + g);

    p = Probability(fore, given);
    probability = data[p];
    return probability;

def sort(bn = [], parents = {}):
    queue = bn.copy();
    res = [];
    while(queue.__len__() != 0):
        first_element = queue.pop(0);
        given = parents[first_element.lower()];
        if(len(given) == 0):
            res.append(first_element);
            continue;
        else:
            b = True;
            for g in given:
                if(g not in res) and (g.upper() not in res) and (('!'+g) not in res):
                    b = False;
                    break;
            if(b):
                res.append(first_element);
            else:
                queue.append(first_element);
    return res;

# data,parents = readdata('aima-alarm.xml')
# p1 = Probability('a',{'b','!e'});
# print(parents)