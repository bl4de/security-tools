### nodestructor.py - static code analysis tool for Node.js applications


```nodestructor``` is a simple Python script to perform some basic static code analysis of installed npm modules in your ```node_modules``` directory, but it can be easily changed into universal JavaScript files scanner.


I've created this tool while working on [Node.js third-party modules Bug Bounty Program](https://hackerone.com/nodejs-ecosystem) on HackerOne and I just add any new "suspicious" code pattern that in certain conditions might lead to security vulnerability (like calls to ```fs``` module functions like ```readFile()``` or ```createReadStream()``` - without proper sanitization this sometimes leads to Path Traversals and Local File Include vulnerabilities - you can read more about such vulnerabilities found in many ```npm``` modules [here](https://github.com/bl4de/research/blob/master/npm-static-servers-most-common-issues/npm-static-servers-most-common-issues.md) )


There are two sets of dangerous patterns implemented: one is NodeJS application specific (like ```child_process``` or ```fs.readFile```), and the other one is more focused on browser patterns (like ```innerHTML``` or ```location.href```).

Important thing is that the presence of such patterns does not mean application is vulnerable. It might be, if user input is processed there in an insecure way, eg. input from the user is directly used in ```innerHTML``` call, which might cause DOM-based XSS.

```nodestructor``` only helps to find those patterns across huge codebases, like heavy npm'ed NodeJS apps. There is always a long way between source, where input comes, and a sink, when it can be (eventualy) executed.

To learn more about how to identify this relationship between sources and sinks, I strictly recommend to watch an awesome video made by @LiveOverflow (https://twitter.com/LiveOverflow), available here: https://www.youtube.com/watch?v=ZaOtY4i5w_U


You can use nodestructor and modify it as you want, as it's available under WTFPL Licence (https://pl.wikipedia.org/wiki/WTFPL).


### Usage and options 

```
                                                                              
                    (                )                    )           
                    )\ )   (      ( /( (      (        ( /(      (    
        (      (   (()/(  ))\ (   )\()))(    ))\   (   )\()) (   )(   
        )\ )   )\   ((_))/((_))\ (_))/(()\  /((_)  )\ (_))/  )\ (()\  
        _(_/(  ((_)  _| |(_)) ((_)| |_  ((_)(_))(  ((_)| |_  ((_) ((_) 
        | ' \))/ _ \/ _` |/ -_)(_-<|  _|| '_|| || |/ _| |  _|/ _ \| '_| 
        |_||_| \___/\__,_|\___|/__/ \__||_|   \_,_|\__|  \__|\___/|_|   
                                                                
#####    static code analysis for Node.js and other JavaScript apps        #####
#####    GitHub.com/bl4de | twitter.com/_bl4de | hackerone.com/bl4de       #####

example usages:   
            $ ./nodestructor filename.js
            $ ./nodestructor -R ./dirname
            $ ./nodestructor -R ./dirname --skip-node-modules --skip-test-files
            $ ./nodestructor -R ./node_modules --exclude=babel,lodash,ansi
            $ ./nodestructor -R ./node_modules --include=body-parser,chalk,commander


usage: nodestructor [-h] [-R] [-E EXCLUDE] [-I INCLUDE] [-S] [-T] filename

positional arguments:
  filename              Specify a file or directory to scan

optional arguments:
  -h, --help            show this help message and exit
  -R, --recursive       check files recursively
  -E EXCLUDE, --exclude EXCLUDE
                        comma separated list of packages to exclude from
                        scanning (eg. babel excludes ALL packages with babel
                        in name, like babel-register, babel-types etc.
  -I INCLUDE, --include INCLUDE
                        comma separated list of selected packages for
                        scanning. Might be useful in projects where there are
                        hundreds of dependiences and only some of them needs
                        to be processed
  -S, --skip-node-modules
                        when scanning recursively, do not scan ./node_modules
                        folder
  -T, --skip-test-files
                        when scanning recursively, do not check test files
                        (usually test.js)
  -P PATTERN, --pattern PATTERN
                        define your own pattern to look for. Pattern has to be
                        a RegEx, like '.*fork\('. nodestructor removes
                        whiitespaces, so if you want to look for 'new fn()',
                        your pattern should look like this: '.*newfn\(\)' (all
                        special characters for RegEx have to be escaped with \
                        )




```

![Sample usage screen](screen.jpg)


#### Scanning single file

The basic usage - scan single file:

```
$ nodestructor ./node_modules/path_to_module/sample_filename.js
```

This will give the following output:

```
$ nodestructor ./node_modules/nunjucks/src/filters.js 


#####  nodestructor.py - static code analysis for Node.js applications  #####
# GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de | bloorq@gmail.com #

examples:   $ ./nodestructor filename.js
            $ ./nodestructor -R ./dirname
            $ ./nodestructor -R ./dirname --skip-node-modules --skip-test-files
            $ ./nodestructor -R ./node_modules --exclude babel,lodash,ansi


FILE: ./node_modules/nunjucks/src/filters.js

::  line 591 :: <a.href.>  code pattern identified:  
      return "<a href=\"" + possibleUrl + "\"" + noFollowAttr + ">" + shortUrl + "</a>";

::  line 596 :: <a.href.>  code pattern identified:  
      return "<a href=\"http://" + possibleUrl + "\"" + noFollowAttr + ">" + shortUrl + "</a>";

::  line 601 :: <a.href.>  code pattern identified:  
      return "<a href=\"mailto:" + possibleUrl + "\">" + possibleUrl + "</a>";

::  line 606 :: <a.href.>  code pattern identified:  
      return "<a href=\"http://" + possibleUrl + "\"" + noFollowAttr + ">" + shortUrl + "</a>";

Identified 4 code pattern(s)

----------------------------------------------------------------------------------------------------

 1 file(s) scanned in total

Identified 4 code pattern(s) in 1 file(s)

```


#### -h

This option displays simple help with description of all available options.



#### -R or --recursive

This option forces ```nodestructor``` to scan all directories recursively. Typical usage will be like this (to scan all modules installed):

```
$ nodestructor -R ./node_modules/
```

To scan only one module, use:

```
$ nodestructor -R ./node_modules/module_name
```

#### -E or --exclude

Here a list of comma-separated module names can be provided, to omit scanning large modules, typically installed by default by many npm packages (like Babel etc.). This allows to provide an output to be more clear and focused only on interested modules.

Also, there is ```EXCLUDE_ALWAYS``` array defined directly in the source code file ```nodestructor.py```. Those modules are excluded from scanning always, no matter if ```-E``` option was set (just for convenience).

Example usage:

```
$ nodestructor -R ./node_modules/ --exclude=some_module,other_module,this_module_as_well
```

#### -I or --include

This option allows to scan only predefined list of modules. Might be helpful when application contains hundreds of npm package dependiences and you want to scan only couple of them. When this option is set, then ```--exclude``` is ignored.

Example usage:

```
$ nodestructor -R node_modules --include=body-parser,chalk,commander --skip-test-files
```

This will scan only ```body-parser```, ```chalk``` and ```commander``` directories in ```node_modules``` folder.


#### -T or --skip-test-files

This option allows to exclude form scanning typical test files, like ```test.js```, ```tests.js``` etc. Feel free to extend this for your needs (defined in source as ```TEST_FILES``` array)


#### -P or --pattern

Allows to define own patterns to look for. Defined pattern should follow format used in ```nodestructor```, which means no spaces between words and escaping all RegEx special characters with ```\```.

Example:

If you'd like to look for:

```
return Object.keys(myObj)
```

the pattern should be defined as follows:

```
"returnObject\.keys\(myObj\)"
```

Complete command will then look like this:

```
$ nodestructor -R node_modules -P "returnObject\.keys\(myObj\)"
```

or

```
$ nodestructor -R node_modules --pattern "returnObject\.keys\(myObj\)"
```


#### Complete sample usage

After installing a template engine ```nunjucks``` (https://www.npmjs.com/package/nunjucks), I did a scan with following options set:

```
$ nodestructor -R node_modules/nunjucks/ --exclude=docs,browser,samples --skip-test-files
```

The result was:

```

#####  nodestructor.py - static code analysis for Node.js applications  #####
# GitHub: bl4de | Twitter: @_bl4de | hackerone.com/bl4de | bloorq@gmail.com #

examples:   $ ./nodestructor filename.js
            $ ./nodestructor -R ./dirname
            $ ./nodestructor -R ./dirname --skip-node-modules --skip-test-files
            $ ./nodestructor -R ./node_modules --exclude babel,lodash,ansi


FILE: node_modules/nunjucks/src/filters.js

::  line 591 :: <a.href.>  code pattern identified:  
      return "<a href=\"" + possibleUrl + "\"" + noFollowAttr + ">" + shortUrl + "</a>";

::  line 596 :: <a.href.>  code pattern identified:  
      return "<a href=\"http://" + possibleUrl + "\"" + noFollowAttr + ">" + shortUrl + "</a>";

::  line 601 :: <a.href.>  code pattern identified:  
      return "<a href=\"mailto:" + possibleUrl + "\">" + possibleUrl + "</a>";

::  line 606 :: <a.href.>  code pattern identified:  
      return "<a href=\"http://" + possibleUrl + "\"" + noFollowAttr + ">" + shortUrl + "</a>";

Identified 4 code pattern(s)

----------------------------------------------------------------------------------------------------
FILE: node_modules/nunjucks/src/precompile.js

::  line 85 :: fs.File(  code pattern identified:  
    precompiled.push(_precompile(fs.readFileSync(input, 'utf-8'), opts.name || input, env));

::  line 93 :: fs.File(  code pattern identified:  
        precompiled.push(_precompile(fs.readFileSync(templates[i], 'utf-8'), name, env));

Identified 2 code pattern(s)

----------------------------------------------------------------------------------------------------
FILE: node_modules/nunjucks/src/node-loaders.js

::  line 96 :: fs.File(  code pattern identified:  
      src: fs.readFileSync(fullpath, 'utf-8'),

Identified 1 code pattern(s)

----------------------------------------------------------------------------------------------------

 36 file(s) scanned in total

Identified 7 code pattern(s) in 3 file(s)

```


#### Predefined settings

Some of predefined settings are hardcoded directly in the code. If you'd like to tune up this tool to meet your needs or you think something is not working as you expect, this is likely a good place to take a look at:

```python

EXTENSIONS_TO_IGNORE = ['md', 'txt', 'map', 'jpg', 'png']
MINIFIED_EXT = ['.min.js']
SKIP_ALWAYS = ['package.json', 'README.md']
TEST_FILES = ['test.js', 'tests.js']
SKIP_NODE_MODULES = False
SKIP_TEST_FILES = False
EXCLUDE = []
EXCLUDE_ALWAYS = ['babel', 'lodash', 'ansi', 'array', 'core-util', '.bin',
                  'core-js', 'es5', 'es6', 'convert-source-map', 'source-map-', '.git', '.idea']
INCLUDE = []
```

#### LICENCE

This software is made under WTFPL Licence (https://pl.wikipedia.org/wiki/WTFPL)