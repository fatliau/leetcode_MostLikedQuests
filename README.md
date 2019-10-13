# leetcode_MostLikedQuests
Using API calls to get all leetcode questions and store its like/dislike counts to get the top like/dislike ratio questions

## requirements
1. python 3
2. python module sqlalchemy

## steps
1. execute the main.py
2. start querying in sqlite

## check the data
### highest like/dislike ratio question without premium limitation
```
SELECT questionFrontendId, title, isPaidOnly, difficulty, (likes / dislikes) as likeDislike_ratio, likes, dislikes
FROM questions WHERE isPaidOnly = 0 order by likeDislike_ratio DESC LIMIT 200;
```
![LikeDislieRatio.png](/pics/LikeDislieRatio.png)
