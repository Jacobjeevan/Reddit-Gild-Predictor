# Challenges

## Data Collection

Imbalance of data was known, but the degree was underestimated, hence after initial analysis, scraping was continued until a substantial amount of
data was collected (~1.5 million samples).

Unfortunately, the data was not usable as data collection process had a bug (for gilded comments, only comments with gold gilds were collected. All
other gilded comments were ignored). This was due to a misinterpretation of the PRAW API. The error was found later in the scraping stage.

The data wasn't fully usable since it had a mix of gilded and nongilded comments (labeled as "nongilded"). The program was modified to rectify the error,
a few other changes were also made, in order to collect more relevant features.

Data collection was a time consuming process (roughly ~70k records collected everyday), so roughly a week needed to collect 500k comments. The scraping
was also interrupted by power outages due to weather.

Hence a few more changes needed to be made, after which the data collection was completed in about 8 days, collecting a total of (after preprocessing) ~620k comments, of which about ~1k was gilded.

## Analysis

The high class imbalance meant that standard metrics, such as accuracy, could not be used to compare model performance. After initial literature review,
F1 and ROC AUC scores were chosen as performance metrics.

Initially, Sklearn's default F1 score functionality was used for comparison. However, a custom scoring function had to written for crossvalidation comparisons(Forman et al, Ref: https://www.hpl.hp.com/techreports/2009/HPL-2009-359.pdf).

Forman et al, showed that the default F1 score is slighly negatively biased and would result in a more optimistic result. Following this, all models had to be
rerun to account for the bias.

## Refactoring

The third major challenge was refactoring the code for further use. Initially functional paradigm was used for quick and dirty analysis, however I chose to
refactor the entire code in object oriented style for better presentation and easier future use (for second stage and beyond).