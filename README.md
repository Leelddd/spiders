# zhihu-spider

Spider for [zhihu.com](https://www.zhihu.com), mainly used for get user follow links

## api and data format analysis

User Info

Basic
- id
- name
- user_token
- user_type: people/organization

Follow Info
- follower
- followee

Contribution
- answer
- get_like
- collected
- questions
- articles
- think

https://www.zhihu.com/api/v4/members/{username}/followees?limit=20&offset=0

## 策略

从一个用户出发，爬取所有关注的人，将关注列表送入检查队列，检查是否符合爬去标准（赞，关注者），
然后将符合要求的用户送入爬取队列，爬取线程随机取队列爬取
