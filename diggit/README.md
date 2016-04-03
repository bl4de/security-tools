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
./diggit.py http://webpage.com/ d60fbeed6db32865a1f01bb9e485755f085f51c1 /path/to/temp/folder/
```
