# warc tool (IR homework)

## Note
Coz the warc package only supports Python 2.7 and is no longer maintained, you need Python 2.7 to run warc tool. 

## Usage
`python main.py filename -c` for create dict.

`python main.py filename -s` for search.

## Input example
`python main.py 114514.warc -c` 

## Output dict file
`output.dict`

## Panacea ~~「靈丹妙藥」這什麼鬼名字~~:
Word: `terms.keys()`<br/>
Document ID: `terms[word].keys()`<br/>
Document ID and positions: `terms[word]`<br/>
Term frequency: `len(terms[word][docid])`<br/>
The document frequency is stored in dict `amount`.

 ~~## Structure:~~

## Search Example

```bash
#如果是 OR 會是
Query: gfw able OR hama able
Searching for words:  ['hama', 'able']  
#或者
Query: gfw able OR hama able
Searching for words:  ['gfw', 'able'] 

#如果是 AND
Query: gfw able AND hama
Searching for words:  ['gfw', 'able', 'hama'] 

#Single keywords
Query: able
Searching for words:  ['able']

#Free texts
Query: able abn
Searching for words:  ['able', 'abn']

Query: gfw able OR hama able

Searching for words:  ['hama', 'able'] 

  #doc  #similarity score
 doc66          0.058510
 doc72          0.054423
 doc26          0.037607
 doc15          0.035602
 .....
```



##  ~~Some tests in `test.py`(for HW2):（已廢棄）~~


## ~~Try to implement search function search in `test_for_query.py`(for HW2):（已廢棄）~~

