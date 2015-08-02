[ ![Codeship Status for madisonmay/Tomorrow](https://codeship.com/projects/9a3b4c60-1b5b-0133-5ec7-7e346f2e432c/status?branch=master)](https://codeship.com/projects/94472)

# Tomorrow
Magic decorator syntax for asynchronous code in Python

Installation
------------

Tomorrow is conveniently available via pip:
```
pip install tomorrow
```

or installable via `git clone` and `setup.py`
```
git clone git@github.com:madisonmay/Tomorrow.git
sudo python setup.py install
```

Usage
-----
The tomorrow library enables you to utilize the benefits of multi-threading with minimal concern about the implementation details.

Let's take a look at how simple it is to speed up an inefficient chunk of blocking code with minimal effort.


Naive Web Scraper
-----------------
You've collected a list of urls and are looking to download the HTML of the lot.  The following is a perfectly reasonable first stab at solving the task.

For the following examples, we'll be using the top sites from the Alexa rankings.

```
urls = [
    'http://google.com',
    'http://facebook.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
]
```

Right then, let's get on to the code.

```
import time
import requests

from tomorrow import threads

def download(url):
    return requests.get(url)

if __name__ == "__main__":

    start = time.time()
    responses = [download(url) for url in urls]
    html = [response.text for response in responses]
    end = time.time()
    print "Time: %f seconds" % (end - start)
```

More Efficient Web Scraper
--------------------------

Using tomorrow's decorator syntax, we can define a function that executes in multiple threads.  Individual calls to `download` are non-blocking, but we can largely ignore this fact and write code identically to how we would in a synchronous paradigm. 

``` 
import time
import requests

@threads(5)
def download(url):
    return requests.get(url)

if __name__ == "__main__":
    import time

    start = time.time()
    responses = [download(url) for url in urls]
    html = [response.text for response in responses]
    end = time.time()
    print "Time: %f seconds" % (end - start)

```

Awesome!  With a single line of additional code (and no explicit threading logic) we can now download websites ~10x as efficiently.


How Does it Work?
-----------------

Feel free to read the source for a peek behind the scenes -- it's less that 50 lines of code.
