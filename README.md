# e-hentai_downloader

Downloading picture from e-hentai.org 

## set up

first, you should fill in parameter to pretend a **browser**
```python
#header
headers = {
	'user-agent': 'you should write your user-agent here'
}
```
**user-agent** :  A request header what you use to connect to server, You can see more information [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent).  You should use **browser** User-Agent request header.

then, fill in the path you want of downloading picture
```python
#path
path = 'you should write your path here'
```

## Using
Run the code. Copy the URL of album you want to download and paste to program
URL format should like this https://e-hentai.org/g/**/*
