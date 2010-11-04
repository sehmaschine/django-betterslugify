Slugifornication
================

A drop in replacement for Django's slugify function.

Sponsored by [Webrunners GmbH](http://www.webrunners.de)

Features:

- Retains readability by replacing Umlaut characters with standard ascii chars
- Shortens length to a word limit
- Removes stopwords (German, English French at the moment)
  Stopword list brovided by http://www.ranks.nl/resources/stopwords.html
