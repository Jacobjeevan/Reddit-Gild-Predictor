# Reddit Gild Predictor Plan:

## Objective:

Given a reddit comment, classify which gilding, if any, it would receive?

## Plan:

Two models: One with one hot encoded and the other with ordinal (since each gilding is better
Try gradient boosting.

### Step 1: Choose subreddit to scrape data from:

We chose 'r/gaming' for scraping the data. This is because of its popularity (4th in terms of subscriber count, Redditlist.com, April 2020) and our own familiarity with the subreddit.

We also theorized that a popular subreddit would be more likely to have more comments (and thus, more gilded comments). Based on initial scraping tests, we decided on scraping for ~week (or till collecting more then 500k comments).

### Step 2: Extract the data

- Modify the Scraper (from Reddit Upvote predictor project) to collect relevant data.
- Based on initial research, relevant features include comment text, # of upvotes, # of gildings (total), list of received gildings (and number) and comment author's link karma, comment karma, account creation date.

Note: Comment and link karma are attributes of the author (overall activity on reddit). Relevant qn: Is 
a more active redditor more likely to receive gildings?

Collect comment attributes:

Number of upvotes, link karma and comment karma of the comment author. Comment text was also collected for feature extraction.

### Step 3: EDA

- Extract features: 
 - Account age (based on creation date: choose a date/time to calculate account age)
 - Account activity within 'r/gaming' subreddit (extract account id for each comment)
 - Does the comment contain any emojis? or pictures?
 - Comment length
 - Depending on age of data collected, a time series analysis could be done (Ex: Are people more generous during holiday season i.e. comments more likely to receive gildings during holiday season). Further exploration would require more data (perhaps from other subreddits as well).

- Comment text
  - Top words (stop words like "the" removed)
  - Occurence of top words in a comment (compare to # of upvotes/gildings; do comments with top words receive more upvotes/gildings?
  - Infer topic of thread based on comment text (reddit thread id should be collected during scraping)
  - Do comments who deviate from main topic of the thread receive more upvotes/gildings?
  - Since the data is from 'r/gaming', some relevant topics would include pc games, console games. Interesting qn to ask: Do comments about pc gaming receive more upvotes? What about console games? For the future, collect original thread data as well (as of the time of adding this, scraping has ended).
  - Semi supervised approach; topic modeling to extract thread topic and build a model to classify the threads solely based on thread data. Build another model with concatenated data of thread attributes and comment attributes (use thread id to associate comments in one thread).

- Normalize the numerical for a better model (Note: Standardization might be a better approach since comments with gildings are outliers due to their rarity). 
- Since each level of guilding (none -> silver -> gold) is better than the other, a model with ordinal targets might be more appropriate. Try another model with one hot encoded targets.


