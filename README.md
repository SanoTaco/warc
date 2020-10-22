# warc tool (IR homework)

## Note
Coz the warc package only supports Python 2.7 and is no longer maintained, you need Python 2.7 to run warc tool. 

## Usage
`python main.py filename`

## Input example:
`python main.py 114514.warc`

## Output dict file:
`output.dict`

## Panacea ~~「靈丹妙藥」這什麼鬼名字~~:
Word: `terms.keys()`<br/>
Document ID: `terms[word].keys()`<br/>
Document ID and positions: `terms[word]`<br/>
Term frequency: `len(terms[word][docid])`<br/>
The document frequency is stored in dict `amount`.

## Structure:
Dict Object: term{}
```json
{
   "wordN":{
      "doc1":[
         "pos1",
         "pos2"
      ],
      "doc2":[
         "pos1",
         "pos2",
         "pos3"
      ],
      "docN":[
         "posN"
      ]
   }
}
```

### Example

```json
{
   "a":{
      "1":[
         3
      ]
   },
   "is":{
      "1":[
         1
      ],
      "0":[
         2
      ]
   },
   "student":{
      "1":[
         4
      ]
   }
}
```

## Some tests in `test.py`(for HW2):
```python
array = np.array(list(terms.items()))

print array, "\n", array[1], "\n", array[1, 1]
for v in array[1, 1]:
    print v
```

The terminal will show:
```bash
[['sb' {'1': [3], '2': [1, 2, 3]}]
 ['is' {'1': [1], '0': [2]}]
 ['my' {'1': [2], '0': [3]}]
 ['brother' {'1': [0], '0': [0, 1, 4], '2': [0]}]
 ['student' {'1': [4], '2': [4]}]] 
['is' {'1': [1], '0': [2]}] 
{'1': [1], '0': [2]}
1
0
```

We can easily understand that `array[row]` ->`[word{docID:[pos], ... , docIDN:[posN]}] ` and `array[row][1]`->`{docID:[pos],...,docIDN:[posN]}`, it means that that `array[row]`will show word in which row and `array[row][1]` will show where this word appears in which document and position.</br>

If we want to get all the positions, we can use for loop function to get them.

Example:

```Python
for docid in array[row, 1]:
    print docid # To get keys
    
for docid in array[row, 1]:
    print array[row, 1][docid] # To get values
```



And the we can easily find the panacea（靈丹妙藥) in this test:

Word: `array[row, 0]`<br/>
Document ID: `array[row, 1].keys()`<br/>
Document ID and positions: `array[row, 1]`<br/>
Term frequency: `len(array[row, 1][docid])`<br/>

tests for tf-idf:

```python
dictTest = {}

for s in range(1, doc_i):
    print array[s, 0]
    for v in array[s, 1]:
        if v not in dictTest:
            dictTest[v] = {}
        print "doc", int(v)+1, "\ttf:", len(array[s, 1][v])
        print "idf", np.log(doc_i/amount[array[s, 0]]+1)
        print "TF-IDF for doc", int(v)+1, ":", len(
            array[s, 1][v])*np.log(doc_i/amount[array[s, 0]]+1), "\n"
        tf_idf_data = len(array[s, 1][v])*np.log(doc_i/amount[array[s, 0]]+1)
        dictTest[v][array[s, 0]] = tf_idf_data
print dictTest
```

The terminal will show:

```bash
who
doc 4   tf: 1
idf 1.6094379124341003
TF-IDF for doc 4 : 1.6094379124341003 

brother
doc 1   tf: 3
idf 1.0986122886681098
TF-IDF for doc 1 : 3.295836866004329 

doc 4   tf: 1
idf 1.0986122886681098
TF-IDF for doc 4 : 1.0986122886681098 

gg
doc 4   tf: 1
idf 1.6094379124341003
TF-IDF for doc 4 : 1.6094379124341003

{'0': {'brother': 3.295836866004329}, '3': {'gg': 1.6094379124341003, 'who': 1.6094379124341003, 'brother': 1.0986122886681098}}
```

Make `dictTest` json format, we will get:

```json
{
    "0": {
        "brother": 3.295836866004329
    }, 
    "3": {
        "gg": 1.6094379124341003, 
        "who": 1.6094379124341003, 
        "brother": 1.0986122886681098
    }
}
```

It means:

```json
{
    "doc1": {
        "word1": tf-idf
    }, 
    "doc2": {
        "word1": tf-idf, 
        "word2": tf-idf, 
        "word3": tf-idf
    }
}
```

