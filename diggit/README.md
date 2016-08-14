### How it works

If we know, where .git folder is located on the remote server, but we can not just clone or checkout it,
 there's always a possibility to read all information from Git objects.
 
Git objects are stored in a special folder and each of them has an unique identifier,
which is simple SHA1 hash.

Each object contains some information, eg. current tree structure, file content or commit content.

More details:

https://github.com/bl4de/research/tree/master/hidden_directories_leaks#hidden-directories-and-files-as-a-source-of-sensitive-information-about-web-application

### Basic usage

```
./diggit.py http://webpage.com /path/to/temp/folder/ d60fbeed6db32865a1f01bb9e485755f085f51c1
```

where:

- http://webpage.com is remote path, where .git folder exists
- /path/to/temp/folder is path to local folder with dummy Git repository
- d60fbeed6db32865a1f01bb9e485755f085f51c1 is a hash of particular Git object to download

Dummy Git repository can be made by command _init_:
```
$ cd /path/to/temp/folder && git init
```

If hash is a commit, *diggit* will find current tree hash and all blobs in this tree 
(it will download all objects)