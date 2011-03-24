# coding: utf-8
'''


@author: Assem Chelli
@contact: assem.ch [at] gmail.com
@license: GPL
@organization: Waiting support 

'''


from whoosh.scoring import Cosine, TF_IDF, Frequency, BM25F
from whoosh.highlight import highlight, NullFragmenter, BasicFragmentScorer, FIRST, Fragment, HtmlFormatter,GenshiFormatter
from TextProcessing import QHighLightAnalyzer, Gword_tamdid
from whoosh.analysis import StandardAnalyzer

#Results.extend(results)Results.upgrade(results)Results.upgrade_and_extend(results)    
def QScore(methode=None):
    """ chooose the methode of score 
        - Cosine
        - BM25F
        - TF_IDF
        - Frequency
    
    """
    if not methode:methode = BM25F(B=0.75, K1=1.2)#Frequency
    return methode

def QSort(sortedby):
    """         """
    if sortedby == "mushaf":sortedby = "gid"
    elif sortedby == "tanzil":sortedby = ("sura_order", "aya_id")
    elif sortedby == "subject":sortedby = ("chapter", "topic","subtopic")
    elif sortedby == "score": sortedby = None
    else: sortedby = sortedby
    return sortedby
    

def QFilter(results, new_results):
    """           """
    results.filter(new_results)
    return results

def QExtend():
    pass

def QPaginate(results, pagelen=10):
    """generator of pages"""
    l = len(results)
    min = lambda x, y:y if x > y  else  x
    for i in range(0, l, 10):
        yield (i / pagelen, results[i:min(i + pagelen, l)])
        

def Qhighlight(text, terms,type="css"):
    """ highlight terms in text 
    
    @param type: the type of formatting , html or css or genchi
    """
    if type=="html":
        formatter= QHtmlFormatter()
    elif type=="genshi":
        formatter=GenshiFormatter()
    elif type=="bold":
        formatter=QBoldFormatter()
    else:
        formatter=HtmlFormatter(tagname="span", classname="match", termclass="term", maxclasses=8)
    

    
    h = highlight(
                      text,
                      terms,
                      analyzer=QHighLightAnalyzer, 
                      fragmenter=QFragmenter(),
                      formatter= formatter,
                      top=3,
                      scorer=BasicFragmentScorer,
                      minscore=1
                )
    
    if h:return h
    else:return text

class QFragmenter:
    """ TO DO """
    def __init__(self):
        pass
    
    def __call__(self, text, tokens):
        return [Fragment(list(tokens))]


class QHtmlFormatter(object):
    """ add the style tags to the text """
    def __init__(self, change_size=True, color_cycle=["red", "green", "orange", "blue"]):
        
        self._change_size = True
        self._color_cycle = color_cycle

        
    def _format(self, text, color, score=1):   
        if self._change_size:ration = 100 + (score - 1) * 0.25
        else:ration = 100
        
        return "<span style=\"color:" + color + ";font-size:" + str(ration) + "%\"><b>" + Gword_tamdid(text) + "</b></span>" 
        
        
  
    def _format_fragment(self, text, fragment):
        output = []
        index = fragment.startchar
        CC = self._color_cycle
        CPT = 0
        MAX = len(CC)
        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            
            ttxt = text[t.startchar:t.endchar]
            if t.matched: 
                ttxt = self._format(ttxt, color=CC[CPT])#:TO DO: SCORE score=BasicFragmentScorer(fragment)
                CPT = (CPT + 1) % MAX
            output.append(ttxt)
            index = t.endchar
        
        output.append(text[index:fragment.endchar])
        return "".join(output)

    def __call__(self, text, fragments):
        return "".join((self._format_fragment(text, fragment)
                                  for fragment in fragments))  
        

class QBoldFormatter(object):
    """ add the style tags to the text """
      
    def _format(self, text):   
        return "<b>" + Gword_tamdid(text) + "</b>" 
        
        
  
    def _format_fragment(self, text, fragment):
        output = []
        index = fragment.startchar

        for t in fragment.matches:
            if t.startchar > index:
                output.append(text[index:t.startchar])
            
            ttxt = text[t.startchar:t.endchar]
            if t.matched: 
                ttxt = self._format(ttxt)
            output.append(ttxt)
            index = t.endchar
        
        output.append(text[index:fragment.endchar])
        return "".join(output)

    def __call__(self, text, fragments):
        return "".join((self._format_fragment(text, fragment)
                                  for fragment in fragments))  
        

if __name__ == "__main__":
    H = Qhighlight(u"الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", [u"الحمد", u"لله"],"bold")
    print H