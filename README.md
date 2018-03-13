# thumbups
**System requirements**
1. python 2 or 3

**Usage**
1. (optional) create virtual enviroment
    * `virtualenv -p /usr/bin/python venv`
    * `source venv/bin/activate`
2. `pip install -r requirements.txt`
3. run script:
    * put videos_ids in `thumbups.py` and run 
    
    `python thumbups.py`
    * (alternative) put space separated videos_ids in command line:
     
     `python thumbups.py 257287904 174711575 253228558`

**Known issues in setting environment**

You may see the following error:
`ImportError: pycurl: libcurl link-time ssl backend (openssl) is different from compile-time ssl backend (none/other)`

if you face this error try
1. `pip uninstall pycurl`
2. `export PYCURL_SSL_LIBRARY=openssl`
3. `pip install pycurl`
