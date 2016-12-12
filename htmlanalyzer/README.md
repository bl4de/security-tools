## htmlanalyzer

This program analyze HTML and output information about:

- JavaScript references (both external scripts and inline code)
- comments
- all tags with "src" attribute (images, CSS)


### Usage:

If you want to htmlanalyzer download HTML and analyze it, use -u option:

```
$ ./htmlanalyzer.py -u http://site.com
```


If you already have HTML file saved, use -f instead:
```
$ ./htmlanalyzer.py -f index.html
```

### Options reference

- ```-c True``` - include informations about found comments (default: False)
- ```-v True``` - be verbose; by default only critical informations like possible DOM injectiuon points or debug information are shown

