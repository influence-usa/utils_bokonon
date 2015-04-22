Simple parser that reliably produces data for training.

Two main functions:
- `extractRelation` in relations.py: splits up fields based on FKA, OBO, AKA keywords/phrases. 
- `tagName` in tagger.py: takes in a string and produces a tagged sequence of
  tokens, with special tags for indicators of corporate status. 
