# Reddit Gild Predictor Plan:

## Objectives:

**First stage**: Given a reddit comment and it's attributes (such as number of upvotes, comment author data), build a model
to classify if it's a gilded comment or not.

Optional: Repeat first stage to predict number of gildings received (regression problem). Could also do the same with number of upvotes.

**Second stage**: Repeat, but for multiclass classification (gold, silver or no gildings)

**Third stage**: Repeat first and second stages, but use NLP techniques (Using comment body for classification)

**Fourth stage**: Use a model to combine results from both first/second and third stages.

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

### Progress History:

- 04/17: Data scraping completed (Initial)

- 04/18: Decided on continue scraping based on initial analysis due to higher than expected class imbalance (gilded vs non gilded comments).

- 05/03: Collected 1.5 million comments

- 05/10: Rerunning scraping due to a bug in the initial collection, as well as collecting more relevant features for future work.

- 05/19: Stopped scraping. Completed initial EDA.

- 05/20-21: Experimented with Logistic Regression Model (with Resampling).

- 05/22-23: Experimented with SVM Model (Using Gradient Descent due to high volume of data).

- 05/23-25: Experimented with Decision Trees, Random Forests and Ensemble Models (Under progress)

- 05/25-27: Refactoring into classes and utility functions

- 06/01-02: Second stage refactoring (dividing classes into even more meaningful chunks), cleaning up code.

- 06/04-05: Completed Decision Trees

- 06/06-07: More feature engineering/experimentation (Note: Modified comment age to be calculated in terms of the specific thread it belongs to).
Reran all models. Logistic Regression performed best.

- 06/08: Started literature review for outlier detection approach.

### Notes:

- Initial scraping was completed on 4/17. As expected, the dataset was heavily imbalanced (out of ~500k comments, there were only ~550 gilded comments). Several approaches can be taken to address the imbalance:
  - Continue scraping (We rewrote the python script to continue scraping (possibly get more gilded comments).
  - Oversample/undersample, SMOTE techniques since there's a high imbalance between gilded comments and non-gilded ones, even more so than we expected. Ex: ~600 gilded for ~500k non-gilded comments. Hence we decided to continue scraping in the hopes of collecting bit more data.

- Scraping was redone to account for an error in the collection process. The attribute for number of gilded comments returns only the number for gilded comments (this attribute was initially used to filter out comments with no gilds). The new version of scraping script also added methods for collecting thread information for further analysis.

### Milestones:

- Refer to Milestones.md