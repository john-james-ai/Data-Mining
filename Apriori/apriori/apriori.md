Project : Data Mining    
File    : \apriori.md     
Python  : 3.9.1     

---------------------------------------------------------------------------

Author  : John James      
Company : nov8.ai          
Email   : john.james@nov8.ai           
URL     : https://github.com/john-james-sf/Data-Mining/           

---------------------------------------------------------------------------

Created       : Friday, February 19th 2021, 5:08:39 pm          
Last Modified : Friday, February 19th 2021, 5:08:40 pm           
Modified By   : John James (john.james@nov8.ai)            

---------------------------------------------------------------------------
   
License : BSD          
Copyright (c) 2021 nov8.ai           

---------------------------------------------------------------------------

# Apriori Design Notes
## Itemset 
Standard format for an itemset will be a dictionary containing the following 
kv pairs as indicated in the following examples:

    {id: 23, support: 3000, items: ["Fast Food"]}
    {id: 432, support: 274, items: ["Food & Dining","Restaurant","Bar"]}

## Itemsets
Itemsets are dictionaries with key k, the size of the itemsets and a value equal to 
a list of all itemsets of size k.
For example:
        {k: 2, itemset_list:[]}
## Output
The output file must be in the format support:itemset. Each item in the itemset
must be separated by semicolons.