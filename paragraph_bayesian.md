* code description: A Bayesian classifier is trained to automatically categorize the subtitles. The labeled subtitles are fed into the ```readtrain``` function, and the training set and test set are divided in line 30 to line 33 of the code. Finally, a Bayesian classifier named ```CLF``` is obtained.  
* input: Labeled subtitles
* output: A Bayesian classifier that can categorize a subtitle into one of the types listed in Table 1 
***Notice: *** The training method is the same as that in the sentence-level classifier (see ```sentence_bayesian.py```), except that in the latter, the labeled data are sentences.
