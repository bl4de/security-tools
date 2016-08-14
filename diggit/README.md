### How it works

If we know, where .git folder is located on the remote server, but we can not just clone or checkout it,
 there's always a possibility to read all information from Git objects.
 
Git objects are stored in a special folder and each of them has an unique identifier,
which is simple SHA1 hash.

Each object contains some information, eg. current tree structure, file content or commit content.

More details:

https://github.com/bl4de/research/tree/master/hidden_directories_leaks#hidden-directories-and-files-as-a-source-of-sensitive-information-about-web-application


### Command syntax

```
$ ./diggit.py -u remote_git_repo -t temp_folder -o object_hash [-r=True]
```


### Basic usage

```
./diggit.py -u http://webpage.com -t /path/to/temp/folder/ -o d60fbeed6db32865a1f01bb9e485755f085f51c1
```

where:

- -u is remote path, where .git folder exists
- -t is path to local folder with dummy Git repository
- -o is a hash of particular Git object to download

Dummy Git repository can be made by command _init_:
```
$ cd /path/to/temp/folder && git init
```

If hash is a commit or tree and _-r_ is set to 'True', 
*diggit* will find current tree hash and all blobs in this tree 
(it will download all objects)