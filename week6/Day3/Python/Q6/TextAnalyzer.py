from collections import Counter

class TextAalyser:
    def __init__(self,text:str) -> None:
        self.text=text
        self.lower_text=text.lower()

    def get_char_frequency(self,include_spaces=False):
       content = self.text if include_spaces else self.text.replace(" ","")
       return Counter(content)  
    
    def get_word_frequency(self,min_length=1):
        content =self.text.split()
        counts=Counter(content)
        if min_length<2:
         return counts
        ans={}
        for word,count in counts.items():
           if count>=min_length:
              ans[word]=count
        return ans      
    
    def find_common_words(self,n=10,exclude_common=True):
       common_words={"the","and","is","in","to","of","a","that","it","as","had","for","by","on","with","as","into","than","also","other","but","from","up","out","over","again","down","off","still","under","once","here","when","where","why","how","all","any","some","one","two","three","four","five","six","seven","eight","nine","ten"}
       words=self.get_word_frequency()
       if exclude_common:
          words=Counter({word:count for word,count in words.items() if word not in common_words})
       return words.most_common(n)
     
    def get_reaading_statistics(self):
       char_count=len(self.text)
       word_count=len(self.text.split())
       sentence_count=self.text.count(".")
       average_words_length=sum(len(word) for word in self.text.split())/word_count
       reading_time_in_minutes=word_count/200
       return{
          "char_count":char_count,
          "word_count":word_count,
          "sentence_count":sentence_count,
          "average_words_length":average_words_length,
          "reading_time_in_minutes":reading_time_in_minutes
       }

    def compare_with_text(self,other_text):
       common_words=self.find_common_words(exclude_common=False)
       other_words=TextAalyser(other_text).find_common_words(exclude_common=False)
       common_words_set=set(common_words)
       other_words_set=set(other_words)
       common_word_count=len(common_words_set)
       similarity_score=common_word_count/max(len(common_words_set),len(other_words_set))
       uniques_to_first=common_words_set-other_words_set
       uniques_to_second=other_words_set-common_words_set
       return{
          "common_words":common_words,
          "similarity_score":similarity_score,
          "uniques_to_first":uniques_to_first,
          "uniques_to_second":uniques_to_second
       }

textAnalyser = TextAalyser("hello hi not,wise good hi holla bhola hi hello the the the ")
print(textAnalyser.get_char_frequency(include_spaces=True))    
print(textAnalyser.get_word_frequency(3))    
print(textAnalyser.find_common_words())    
print(textAnalyser.compare_with_text("hello hi good hi hi well not zig zag hello rest the the the "))
print(textAnalyser.get_reaading_statistics())