Creating a custom crawler
=========================


1. Write a custom crawler that inherits from the Scraper class (cf. `../docs/custom_crawler_example.py`)
  - look for examples in the `parser_examples` folder. These serve as a good starting point
  or may even be used directly with little customization.
2. launch with `webcorpcrawler crawl --scraper PATH_TO_FILE_WITH_CUSTOM_SCRAPER  --crawlconfig config.yml`

The contens of the crawlconfig file should be as follows:

```
output:
    - root: /home/developer/
targets: 
    - url: https://first-url-to-process.com/stuff
      meta: description_of_this_stuff
    - url: https://first-url-to-process.com/morestuff
      meta: description_of_this_stuff_too
```

3. The output will be produced at the folders specified in the yaml file in json format. 

4. These results can be further processed with other tools in this package


## Using the docker container

A docker container has been prebuilt in order to make things easier.

```
docker pull xxx
docker run xxx DATA:PWD:...
command...
```



