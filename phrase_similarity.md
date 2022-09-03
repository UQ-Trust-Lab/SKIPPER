* code description: An algorithm that compares the similarity between two phrases
* input:phrase1, phrase2
* output:The score of similarity between two phrases
* details: When entering two different phrases into the ```wordnetSim3``` function, this function end up with a result greater than or equal to 0 and less than 2. If the result is greater than 0.7, we treat these two phrases as similar. 
***Notice: *** Phrases must contain pure words only. For example, they should not contain numbers and punctuation. The format of a phrase should be ```word + space + word....```.   
Example:```wordnetSim3("location data", "geographical position information")```
