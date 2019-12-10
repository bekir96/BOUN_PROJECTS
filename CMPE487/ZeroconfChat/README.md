# CmpE 487 WORKSHOP 3 :heavy_plus_sign:

## ZEROCONF CHAT APP

### Requirements 

- Python 3
- I tested with `Yusuf Yüksel` and `Berat Sert`
- Yusuf Yüksel's student id `2014400051`
- All `Python 3` modules are mentioned in `requirements.txt`

### Usage

`$ chmod u+x zeroconf.py`

`$ ./zeroconf.py`

### Design Notes

In designing this project, I aimed to further diversify the notification part in my previous project. To do this, I researched what the `ansi escape character` is, and found how to make declarations on the text and add color to the background. Reference sites are below. In addition, with the `import pickle`, I write the sending messages to the `store.txt` when exiting the program. So I don't have to deal with `EOFError: Ran out of input` every time I open or close the file. Also, in our design, I send 3 announce packages with udp every 60 seconds. While listening, I'm sending a response package to only one of the three packages that will come in a row.

#### References

- [http://ozzmaker.com/add-colour-to-text-in-python/](http://ozzmaker.com/add-colour-to-text-in-python/)

- [https://en.wikipedia.org/wiki/ANSI_escape_code](https://en.wikipedia.org/wiki/ANSI_escape_code)
