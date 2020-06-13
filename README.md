# Reddit Gild Predictor

## Why?

The project is primarily for exploration and to check if it's possible to capture complex real world relationships through ML.

*Is it possible to capture general opinions within a subreddit?* If so, what opinions are more likely to get gilded? Is it possible to capture
such relationships purely without relying on textual data?

NLP techniques such as text abstraction could be used for 'labeling' a comment text (or even summarizing content of reddit thread). 

Can we extract sentiments associated with topics? For instance: Microtransactions are not looked upon favorably by the gaming community, same is true for r/Gaming.

Can we capture such sentiments, without manually labeling the data? And how do these sentiments relate to gild status of a comment?

## Objectives:

**First stage**: Given a reddit comment and it's attributes (such as number of upvotes, comment author data), build a model
to classify if it's a gilded comment or not.

Optional: Repeat first stage to predict number of gildings received (regression problem). Could also do the same with number of upvotes.

**Second stage**: Repeat, but for multiclass classification (gold, silver or no gildings)

**Third stage**: Repeat first and second stages, but use NLP techniques (Using comment body for classification)

Optional: Use a model to combine results from both first/second and third stages.

## Current Progress:

- 05/20-21: Experimented with Logistic Regression Model (with Resampling).

- 05/22-23: Experimented with SVM Model (Using Gradient Descent due to high volume of data).

- 05/23-25: Experimented with Decision Trees, Random Forests and Ensemble Models (Under progress)

- 05/25-27: Refactoring into classes and utility functions

- 06/01-02: Second stage refactoring (dividing classes into even more meaningful chunks), cleaning up code.

- 06/04-05: Completed Decision Trees

- 06/06-07: More feature engineering/experimentation (Note: Modified comment age to be calculated in terms of the specific thread it belongs to).
Reran all models. Logistic Regression performed best.

- 06/08: Started literature review for outlier detection approach.

## Plan:

- Plan of action is available under docs/Plan.md

### Visualize

- Refer to docs/Visualization.md

### Milestones:

- Refer to docs/Milestones.md