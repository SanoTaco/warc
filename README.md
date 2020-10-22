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

<img src="image-20201022235226100.png" alt="image-20201022235226100" style="zoom:50%;" />

```python
test = [
    ["brother", "brother", "is", "my", "brother"],
    ["s", "is", "my", "sb", "student"],
    ["s", "sb", "sb", "sb", "student"],
    ["brother", "who", "brother", "sb", "brother", "gg"]
]

dictTest = {}

for s in range(np.shape(array)[0]):
    print array[s, 0]
    for v in array[s, 1]:
        if "doc"+str(int(v)+1) not in dictTest:
            dictTest["doc"+str(int(v)+1)] = {}
        print "doc", int(v)+1, "\ttf:", len(array[s, 1][v])
        print "idf", np.log(doc_i/amount[array[s, 0]]+1)
        print "TF-IDF for doc", int(v)+1, ":", (1+np.log(len(array[s, 1][v])))*np.log10(doc_i/amount[array[s, 0]]+1), "\n"
        tf_idf_data = (1+np.log(len(array[s, 1][v])))*np.log10(doc_i/amount[array[s, 0]]+1)
        dictTest["doc"+str(int(v)+1)][array[s, 0]] = tf_idf_data
```

The terminal will show:

```bash
is
doc 2   tf: 1
idf 1.0986122886681098
TF-IDF for doc 2 : 0.47712125471966244 

doc 1   tf: 1
idf 1.0986122886681098
TF-IDF for doc 1 : 0.47712125471966244 

who
doc 4   tf: 1
idf 1.6094379124341003
TF-IDF for doc 4 : 0.6989700043360189 

brother
doc 1   tf: 3
idf 1.0986122886681098
TF-IDF for doc 1 : 1.0012925283394312 

doc 4   tf: 3
idf 1.0986122886681098
TF-IDF for doc 4 : 1.0012925283394312 

gg
doc 4   tf: 1
idf 1.6094379124341003
TF-IDF for doc 4 : 0.6989700043360189 

s
doc 2   tf: 1
idf 1.0986122886681098
TF-IDF for doc 2 : 0.47712125471966244 

doc 3   tf: 1
idf 1.0986122886681098
TF-IDF for doc 3 : 0.47712125471966244 

student
doc 2   tf: 1
idf 1.0986122886681098
TF-IDF for doc 2 : 0.47712125471966244 

doc 3   tf: 1
idf 1.0986122886681098
TF-IDF for doc 3 : 0.47712125471966244 

sb
doc 2   tf: 1
idf 0.6931471805599453
TF-IDF for doc 2 : 0.3010299956639812 

doc 4   tf: 1
idf 0.6931471805599453
TF-IDF for doc 4 : 0.3010299956639812 

doc 3   tf: 3
idf 0.6931471805599453
TF-IDF for doc 3 : 0.6317452481581388 

my
doc 2   tf: 1
idf 1.0986122886681098
TF-IDF for doc 2 : 0.47712125471966244 

doc 1   tf: 1
idf 1.0986122886681098
TF-IDF for doc 1 : 0.47712125471966244
```

Make `dictTest` to be json formatted and sorted, we will get:

```python
{
    "doc1": {
        "brother": 1.0012925283394312, 
        "is": 0.47712125471966244, 
        "my": 0.47712125471966244
    }, 
    "doc2": {
        "is": 0.47712125471966244, 
        "my": 0.47712125471966244, 
        "s": 0.47712125471966244, 
        "sb": 0.3010299956639812, 
        "student": 0.47712125471966244
    }, 
    "doc3": {
        "s": 0.47712125471966244, 
        "sb": 0.6317452481581388, 
        "student": 0.47712125471966244
    }, 
    "doc4": {
        "brother": 1.0012925283394312, 
        "gg": 0.6989700043360189, 
        "sb": 0.3010299956639812, 
        "who": 0.6989700043360189
    }
}
```