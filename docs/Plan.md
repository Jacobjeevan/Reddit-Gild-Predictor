# Reddit Gild Predictor Plan:

## Objective:

Given a reddit comment, classify which gilding, if any, it would receive?

## Step 1: Choose subreddit to scrape data from:

'R/gaming' was chosen for scraping. This is because of its popularity (4th in terms of subscriber count, Redditlist.com, April 2020) and because of the author's familiarity with the subreddit.

Another reasoning is that a more popular subreddit is more likely to have gilded comments.

## Step 2: Extract the data

- Modify the Scraper (from Reddit Upvote predictor project) to collect relevant data.
- Based on initial research, relevant features include comment text, # of upvotes, # of gildings (total), list of received gildings (and number) and comment author's link karma, comment karma, account creation date.
- After initial scraping, thread data was also added to the list of features.
- Following is the comprehensive list of all attributes collected:

Comment attributes:

- Number of upvotes, downvotes, gildings
- Comment text/body
- Whether comment was edited or not
- Comment creation time (linux time)

Thread attributes:

- Thread title
- Gildings, if any
- Whether post was edited
- Total number of comments
- Thread creation time (Linux time)

Author attributes:

- Total comment and link karmas
- Account creation date
- Premium status

Data was saved in CSV format.

## Step 3: EDA

### Extract features:

 - Account age (based on creation date: choose a date/time to calculate account age)
 - Account activity within 'r/gaming' subreddit (extract account id for each comment)
 - Does the comment contain any emojis? or pictures?
 - Comment length
- Normalize the numerical features for a better model (Note: Standardization might be a better approach since comments with gildings are outliers due to their rarity). 
- Since each level of guilding (none -> silver -> gold) is better than the other, a model with ordinal targets might be more appropriate. Try another model with one hot encoded targets.

### Visualize

- Refer to Visualization.md

### Step 5: Models

- Develop a baseline model
  - Depending on the linearity of the data, if possible, start with a much simpler model, such as linear regression for predicting the number of gildings a comment might receive or logistic regression for binary classification (gilded vs not gilded).
  - Finetune and test the baseline model
- Develop a more complex model
  - Want to try experimenting with Decision Trees and particularly Gradient Boosted Trees as a learning experience.

### Current:

- Initial scraping was completed on 4/17. As expected, the dataset was heavily imbalanced (out of ~500k comments, there were only ~550 gilded comments). Several approaches can be taken to address the imbalance:
  - Continue scraping (We rewrote the python script to continue scraping (possibly get more gilded comments).
  - Oversample/undersample, SMOTE techniques since there's a high imbalance between gilded comments and non-gilded ones, even more so than we expected. Ex: ~600 gilded for ~500k non-gilded comments. Hence we decided to continue scraping in the hopes of collecting bit more data.

- Scraping was redone to account for an error in the collection process. The attribute for number of gilded comments returns only the number for gilded comments (this attribute was initially used to filter out comments with no gilds). The new version of scraping script also added methods for collecting thread information for further analysis.

### Milestones:

- Refer to Milestones.md