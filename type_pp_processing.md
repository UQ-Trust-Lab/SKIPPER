* code description: Match the data types in the text to our constructed dictionary of data types.  
* input: Data type paragraph (string)
* output: A list of data types containing 0 and 1
* details: First, the data type paragraph extracted from the privacy policy is entered into the ```caculateSim``` function as a parameter. If the paragraph contains a data type from the data type dictionary, the data type is marked as 1. If it does not appear in the paragraph, the data type will be marked as 0. This function will end up with a matrix in which all data types appearing in the paragraph will be marked as 1.

