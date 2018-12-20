
Werbcorp-crawler
================

This is a set of simple tools for postprocessing results acquired, for instance,
from a web corpus. The tools included here are especially relevant for
cases when 

- concordance results provided by the corpus's interface cannot be easily fetched
as json, csv etc.
- the corpus doesn't contain all the kinds of annotations you would like to have
and you want to add these annotations to individual concordance results afterwards.


Installation
============

Via pip:

```
pip3 install git+https://github.com/tunicorpora/webcorpcrawler
```

Alternatively, you can just manually clone the repository, 
cd into the directory and run `pip3 install -e .` (note the dot at the end of
the command)

<!-- 
TODO:

add a note on responsive usage

-->

Examples
========

See the `docs` folder. ([dircet link](https://github.com/utacorpora/webcorpcrawler/blob/master/docs/))
