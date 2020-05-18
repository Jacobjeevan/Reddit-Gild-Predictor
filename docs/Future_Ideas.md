This is just a space to jot down ideas for future exploration.
 
 Depending on age of data collected, a time series analysis could be done (Ex: Are people more generous during holiday season i.e. comments more likely to receive gildings during holiday season). Further exploration would require more data (perhaps from other subreddits as well).

- Comment text
  - Top words (stop words like "the" removed)
  - Occurence of top words in a comment (compare to # of upvotes/gildings; do comments with top words receive more upvotes/gildings?
  - Infer topic of thread based on comment text (reddit thread id should be collected during scraping)
  - Do comments who deviate from main topic of the thread receive more upvotes/gildings?
  - Since the data is from 'r/gaming', some relevant topics would include pc games, console games. Interesting qn to ask: Do comments about pc gaming receive more upvotes? What about console games? For the future, collect original thread data as well (as of the time of adding this, scraping has ended).
  - Semi supervised approach; topic modeling to extract thread topic and build a model to classify the threads solely based on thread data. Build another model with concatenated data of thread attributes and comment attributes (use thread id to associate comments in one thread).