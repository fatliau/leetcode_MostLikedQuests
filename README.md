# leetcode_MostLikedQuests
Using API calls to get all leetcode questions and store its like/dislike counts to get the top like/dislike ratio questions

## requirements
1. python 3
2. python module sqlalchemy
3. sqlite3

## steps
before query on the database, you can either
* execute the main.py to create and load the database, or
* download the leetcode.db, or
* download the questions.csv

## check the data
### highest like/dislike ratio questions without premium limitation
```
SELECT questionFrontendId, title, isPaidOnly, difficulty, (likes / dislikes) as likeDislike_ratio, likes, dislikes
FROM questions WHERE isPaidOnly = 0 order by likeDislike_ratio DESC LIMIT 200;
```
![LikeDislieRatio.png](/pics/LikeDislieRatio.png)
