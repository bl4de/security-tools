### source_tracker.py - compare website source code with snapshot

This tool compares website source code with previously saved snapshot. 

When used first time, it creates snapshot. When used again, it compares source code from the moment when tools was run with the source code saved in snapshot - and shows all differences (line by line) if any.

### Usage

Sample usage (no differences found between current source and snapshoted one):

```
$ ./compare.py https://hackerone.com

[+] snapshot not found, saving snapshot...

$ ./compare.py https://hackerone.com

[+] snapshot found, compare snapshot with current source...


--------------------------------------------------------------------------------------------
[+] no differencies found; snapshot and current https://hackerone.com source are identical

[+] DONE.
```

Sample usage (differences found):


```
$ ./compare.py http://localhost:8080/test.html

[+] snapshot not found, saving snapshot...

```

Now, I've introduced some small changes in `test.html` and run tool again:

```
$ ./compare.py http://localhost:8080/test.html

[+] snapshot found, compare snapshot with current source...

-- LINE 4 --------------------------------------------------------------------------------

>>>>>  snaphsot line 4
: 
    <title>Node HackerOne Playground</title>


<<<<<  site source line 4

    <title>Node HackerOne Playground Title changed?</title>

-- LINE 9 --------------------------------------------------------------------------------

>>>>>  snaphsot line 9
: 
        console.log('uh oh, change!!')


<<<<<  site source line 9

        console.log('changed here!!')


--------------------------------------------------------------------------------------------
[+] 2 differencies between snapshot and current source found

[+] DONE.

```

### TODO

- refactoring
- multiple websites compare (loaded list form file, eg. output from Aquatone?)
- colorful output :D
- multiple snapshots (?)

