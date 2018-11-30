
Example use case for adding syntactic annotations to a set of concordances
===============================================================

Here's a use case for data retrieved from twitter using R's `tweetR`
package. It demonstrates how you can add syntactic
annotations to twitter data using webcorpcrawl and 
an parser (in this case, stanford's dep parser).

Let's imagine we want to analyze the usage of the word "referee" in recent Uefa
champions' league games (recent, because the Twitter api only let's you search
for tweets not older than one week). In order to run the following you need to
have requested developer access from Twitter, but never mind, the data is also
available as a small data set accompanying our `depsearcheR` package.

```r

library(rtweet)
ref <- search_tweets("(#UCL OR #ChampionsLeague OR #UEFAChampionsLeague) referee",  n = 5000)
library(jsonlite)
write_json(ref, "/tmp/referee.json")

```

Now, in order to parse the tweets we need to index them first.
This can be done in the following way:

```bash

webcorpcrawler add_uids --files /tmp/referee.json --prettyprint


```

The next step is to extract the property containing the actual
material that will be parsed. In the results of Twitter API calls,
this variable is called "text" (see the `--prop` flag in the command). 


```bash

webcorpcrawler prepare --files /tmp/referee.json --prop text --output_folder /tmp/

```

In the `/tmp` folder we now have two new files, `contents.txt`
and `ids.txt`. `contents.txt` is the one you should feed to your
parser. For instance, if you have the stanford parser installed,
you could run something like 

```bash

./corenlp.sh -annotators tokenize,ssplit,pos,lemma,parse, -file contents.txt -outputFormat conll

```

The final task is to inject the parsed results back to the original
json files with the following command:

```bash

webcorpcrawler add_parsed --files /tmp/referee.json --parsed_source contents.txt.conll --indices ids.txt --prop parsed_text --parser stanford


```

Note that we are using the `--parser` flag to tell the script the output
is from stanford's parser. If this is not specified, the script
will try to segment the parsed output using a default pattern.

As a result, we should now have the the file with the tweets in the following format:


```json
    {
        "text": "Here's my #PSGLFC #PARLIV #ChampionsLeague #Football match report:\n\n#PSG #Tuchel 2-1 #LFC #Klopp #ParcDesPrinces\n\nThe Reds unable to cope with the French champions. #ARGH\n\nPlenty off talking points, incl. fails, dives, whines, &amp; annoying referee!!! #UEFA \n\nhttps://t.co/myEFFToA9u https://t.co/v6TNXQ4jhh",
        "source": "Twitter Web Client",
        "display_text_width": 284,
        "is_quote": false,
        "is_retweet": false,
        "favorite_count": 1,
        "retweet_count": 1,
        "hashtags": [
            "PSGLFC",
            "PARLIV",
            "ChampionsLeague",
            "Football",
            "PSG",
            "Tuchel",
            "LFC",
            "Klopp",
            "ParcDesPrinces",
            "ARGH",
            "UEFA"
        ],
        "symbols": [
            null
        ],
        "id": "b2600c4a-e56d-47e5-b47b-ee67e4fb1937",
        "parsed_text": "1\tHere\there\tRB\t_\t0\tROOT\n2\t's\t's\tPOS\t_\t1\tdep\n3\tmy\tmy\tPRP$\t_\t6\tnmod:poss\n4\t#PSGLFC\t#psglfc\tNN\t_\t6\tcompound\n5\t#PARLIV\t#parliv\tNN\t_\t6\tcompound\n6\t#ChampionsLeague\t#championsleague\tNN\t_\t2\tnmod\n7\t#Football\t#football\tNN\t_\t9\tcompound\n8\tmatch\tmatch\tNN\t_\t9\tcompound\n9\treport\treport\tNN\t_\t6\tdep\n10\t:\t:\t:\t_\t9\tpunct\n11\t#PSG\t#psg\tNN\t_\t12\tcompound\n12\t#Tuchel\t#tuchel\tNN\t_\t9\tdep\n13\t2-1\t2-1\tCD\t_\t16\tnummod\n14\t#LFC\t#lfc\tNN\t_\t16\tcompound\n15\t#Klopp\t#klopp\tNN\t_\t16\tcompound\n16\t#ParcDesPrinces\t#parcdesprinces\tNNS\t_\t12\tdep\n17\tThe\tthe\tDT\t_\t18\tdet\n18\tReds\tred\tNNS\t_\t12\tdep\n19\tunable\tunable\tJJ\t_\t1\tamod\n20\tto\tto\tTO\t_\t21\tmark\n21\tcope\tcope\tVB\t_\t19\txcomp\n22\twith\twith\tIN\t_\t25\tcase\n23\tthe\tthe\tDT\t_\t25\tdet\n24\tFrench\tfrench\tJJ\t_\t25\tamod\n25\tchampions\tchampion\tNNS\t_\t21\tnmod\n26\t.\t.\t.\t_\t1\tpunct\n\n1\t#ARGH\t#ARGH\tNNP\t_\t2\tcompound\n2\tPlenty\tPlenty\tNNP\t_\t0\tROOT\n3\toff\toff\tIN\t_\t4\tmark\n4\ttalking\ttalk\tVBG\t_\t2\tacl\n5\tpoints\tpoint\tNNS\t_\t4\tdobj\n6\t,\t,\t,\t_\t5\tpunct\n7\tincl\tincl\tNN\t_\t5\tappos\n8\t.\t.\t.\t_\t2\tpunct\n\n1\tfails\tfail\tVBZ\t_\t0\tROOT\n2\t,\t,\t,\t_\t1\tpunct\n3\tdives\tdive\tVBZ\t_\t1\tdep\n4\t,\t,\t,\t_\t1\tpunct\n5\twhines\twhine\tNNS\t_\t1\tdobj\n6\t,\t,\t,\t_\t5\tpunct\n7\t&\t&\tCC\t_\t5\tcc\n8\tannoying\tannoying\tJJ\t_\t9\tamod\n9\treferee\treferee\tNN\t_\t5\tconj\n10\t!!!\t!!!\tIN\t_\t9\tamod\n\n1\t#UEFA\t#uefa\tNN\t_\t3\tcompound\n2\thttps://t.co/myEFFToA9u\thttps://t.co/myefftoa9u\tNN\t_\t3\tcompound\n3\thttps://t.co/v6TNXQ4jhh\thttps://t.co/v6tnxq4jhh\tNN\t_\t0\tROOT\n"
    },
    {
```


(For clarity's sake I removed some of the props provided by Twitter from the example)


Just for reference, here's how the json can be transformed
back to R as a tibble:

```R

ucl_ref <- read_json("/tmp/referee.json")  
mylist <- list()
ucl_ref <- lapply(ucl_ref, function(x){
           return (tibble(x$text, x$followers_count, x$retweet_count, x$favorite_count, x$location,  x$parsed_text))
}
) %>% do.call(rbind, .)  %>% as_tibble

colnames(ucl_ref) <- c("text","followers","retweets","favorites","location","parsed_text")

```



