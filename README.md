* Fetch Rewards Coding Exercise - Data Engineer

The code in this repo is in response to [this challenge](https://fetch-hiring.s3.amazonaws.com/data-engineer/text-similarity.html) from Fetch Rewards.

Scoring the similarity of documents is a thoroughly developed area of computer science and algorithmic study.
I have nothing new to contribute to that body of knowledge with this coding challenge.
Nevertheless, I implemented a fairly naive algorithm called `silly_score`.
Additionally, I found (and cited) two fairly straightforward algorithms and implemented them.
What I hope will stand out as novel is my approach to average the results of the multiple algorithms.

The program has a driver loop to run all three and then return the average.

I know more about document similarity now than I did before this challenge.

Also, this is the first time I've ever used Flask.

Here's what to do:
```
git clone https://github.com/rothrock/fetch.git
cd fetch
```

build the image.
```
docker build -t fetch:latest .
```

Start the app.
```
docker run --name fetch -d -p 5000:5000 fetch
```

Run this shell script:
```
./compare.sh sample_2.txt sample_1.txt 
```

Or, use the curl command line utility directly to get the comparison score:
```
curl --data-urlencode doc_a@sample_1.txt --data-urlencode doc_b@sample_2.txt http://localhost:5000/score
```

Stop and remover the container.
```
docker stop fetch
docker rm fetch
```
