Simple parser that reliably produces data for training.

Two main functions:
- `parseName` takes in a string and returns a list of lists of tuples. The first
  level of lists corresponds to the full input string/field. The second level of lists corresponds to the various parts of the field, broken apart into distinct names with relationship references (AKA,OBO,FKA). Finally, the tuples that compose each name list are pairs where the first element is the tag and the second element is the string itself. There are a variety of possible tags, such as "INC", "SIMPLE", "COMPANY","FKA".
- `collectedName` takes in a string and returns nested dicts representing the
  various relationships between the named entities in the field. The base level
  dict for just a simple name in the field is just a dict with the `tag`
  property being name and `first` property being the tokenized string. Nesting
  occurs when a relationship indicator is found. See below for an example of the
  output.

Example usage:

``` python
>>>parseName("The Data Company Inc.")
[[('SIMPLE', u'the'), ('SIMPLE', u'data'), ('COMPANY', u'company'), ('CORPORATION', u'inc')]]
>>>parseName("The DATA Company L.L.C. formerly known as The Data Company Incorporated")
[[('SIMPLE', u'the'), ('SIMPLE', u'data'), ('COMPANY', u'company'), ('LLC', u'l.l.c')], [('FKA', u'formerly |   | known |   | as')], [('SIMPLE', u'the'), ('SIMPLE', u'data'), ('COMPANY', u'company'), ('CORPORATION', u'incorporated')]]
>>>collectedName("The DATA Company L.L.C. formerly known as The Data Company Incorporated")
{'tag': ('FKA', u'formerly |   | known |   | as'),
 'first': [[('SIMPLE', u'the'), ('SIMPLE', u'data'), ('COMPANY', u'company'), ('LLC', u'l.l.c')]],
 'second': {'tag': 'name', 'first': [[('SIMPLE', u'the'), ('SIMPLE', u'data'), ('COMPANY', u'company'), ('CORPORATION', u'incorporated')]]}}
```
