#! usr/bin/env python3

import sys
import os
import praw
import time
import argparse
import pandas as pd
from pathlib import Path

class Scraper:

    def __init__(self, args):
        """Parse the arguments and initialize the dictionaries for saving the data"""
        self.exectime = time.time()
        self.checkpoint = args.checkpoint #Checkpoint and Interval are used for saving the data after every n records.
        self.interval = args.checkpoint
        self.minimum = args.minimum # Minimum number of records before exiting the program
        if self.minimum < self.checkpoint: # Ensure that minimum is greater than checkpoint
            print(
                "The minimum number (default: 200k) of records has to larger than checkpoint (default: 10k)")
            sys.exit()
        # Initialize respective dictionaries for storing thread, comment, gildings and author data.
        self.threaddata = {"thread_ids": [], "title": [], "author_ids": [
        ], "upvotes": [], "gildings": [], "created_utc": [], "premium": [], "num_comments": [], "edited": []}
        self.commentdata = {"comment_body": [],
                            "ups": [], "downs": [], "comment_ids": [], 
                            "author_ids": [], "created_utc": [], "edited": [], "thread_ids" : []}
        self.gildings = {"comment_ids": [], "gildings": []}
        self.author = {"author_ids": [], "comment_karma": [],
                       "link_karma": [], "created_utc": [], "is_premium": []}
        # Initializing the praw reddit object and calling it.
        self.reddit = praw.Reddit()
        self.subreddit = self.reddit.subreddit(args.subreddit).top(limit=None)
        # Default save path of the data.
        self.savepath = "../../data/raw/"

    def output_filename(self):
        """Simple function to quickly fetch directory path and return the
        right filepath for saving files.
        Also creates the save folder if it doesn't already exist"""
        dirname = os.path.dirname(__file__)
        Path(os.path.join(dirname, self.savepath)).mkdir(
            parents=True, exist_ok=True)
        return os.path.join(dirname, self.savepath)

    def retrieveUser(self, comment):
        """Takes in comment object as a parameter, which is used to obtain author information such as:
        Author id: is used as the shared column to merge with comments data table
        Comment karma, Link karma, and Premium Status (is_gold)"""

        self.author["author_ids"].append(comment.author.id)
        self.author["comment_karma"].append(
            comment.author.comment_karma)
        self.author["link_karma"].append(comment.author.link_karma)
        self.author["created_utc"].append(
            comment.author.created_utc)
        self.author["is_premium"].append(comment.author.is_gold)

    def retrieveGilds(self, comment):
        '''Takes in the comment object and retrieves comment gild information; adds it to the list'''
        self.gildings["comment_ids"].append(comment.id)
        self.gildings["gildings"].append(comment.gildings)

    def retrieveComment(self, comment, threadid):
        """Takes in comment object as a parameter, which is used to obtain information regarding the comment.
        Threadid is used to keep track of which comments belong to the thread.

        Comment_id is used as the shared column for merging comment and gild data.
        Comment object is then passed to parseUser function to obtain author information.

        Note that some suspended users will still be retrieved (i.e. their comments will be added, however
        their accounts won't have suspended attribute, but will return a 404 error). We will have to remove
        such comments if the author information cannot be found from authors data table.
        """

        # Skip if the comment has been deleted or if the user is suspended/deleted.

        suspended = None
        try:
            suspended = comment.author.is_suspended
        except:
            pass
        if (comment.author is None or comment.body is None or suspended != None):
            pass
        else:
            if (comment.author_fullname[3:] in self.author["author_ids"]):
                pass
            else:
                try:
                    self.retrieveUser(comment)
                except:
                    return
            self.commentdata["thread_ids"].append(threadid)
            self.commentdata["comment_ids"].append(comment.id)
            self.commentdata["comment_body"].append(comment.body)
            self.commentdata["ups"].append(comment.ups)
            self.commentdata["downs"].append(comment.downs)
            self.commentdata["author_ids"].append(comment.author_fullname[3:])
            self.commentdata["created_utc"].append(comment.created_utc)
            self.commentdata["edited"].append(comment.edited)
            if comment.gildings:
                self.retrieveGilds(comment)

    def retrieveThread(self, submission):
        """Takes in the submission object and grabs relevant information regarding the thread,
        including thread author, title, ups/downs, gildings, created time, author premium status etc."""
        self.threaddata["author_ids"].append(submission.author_fullname[3:])
        self.threaddata["thread_ids"].append(submission.id)
        self.threaddata["title"].append(submission.title)
        self.threaddata["upvotes"].append(submission.ups)
        self.threaddata["edited"].append(submission.edited)
        self.threaddata["gildings"].append(submission.gildings)
        self.threaddata["created_utc"].append(submission.created_utc)
        self.threaddata["num_comments"].append(submission.num_comments)
        self.threaddata["premium"].append(submission.author_premium)

    def addTo(self):
        """Takes the subreddit input from user as a parameter, calls respective method for retrieving relevant data."""
        subreddit = self.subreddit
        for submission in subreddit:
            if (submission.id not in self.threaddata["thread_ids"]):
                self.retrieveThread(submission)
                print(f"Collecting: {submission.num_comments} comments")
                submission.comments.replace_more(limit=None)
                all_comments = submission.comments.list()
                for comment in all_comments:
                    # Pass in the submission id as well (so we can keep track of thread <- comments)
                    self.retrieveComment(comment, submission.id)
                    self.save_files()

    def exit_conditions(self):
        """Prompts the user for exit conditions. Enter N and a new minimum in the following prompt to continue scraping."""

        flag = True
        while (flag):
            val = input(
                "Would you like to exit now? Press Y/N; N allows to continue scraping.\n")
            if (val.lower() == 'y'):
                sys.exit()
            elif (val.lower() == 'n'):
                print(f"Current minimum is {self.minimum}\n")
                try:
                    new_min_val = int(
                        input("Type in a new minimum (larger than the previous):"))
                    if new_min_val > self.minimum:
                        self.minimum = new_min_val
                        flag = False
                    else:
                        print(
                            "New minimum is smaller than previous minimum. Try again\n")
                except:
                    print("Wrong type of input. Please enter valid input.\n")
                    continue
            else:
                print("Wrong type of input. Please enter valid input.\n")

    def save_files(self):
        """Saves the files for every checkpoints, exits the program when minimum number of records is reached"""
        length = len(self.commentdata["comment_ids"])
        if (length < self.checkpoint):
            pass
        else:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print("Collected {} records so far; Saving in progress. Time now: {}".format(
                length, current_time))
            # Convert the relevant data to pandas Dataframe and store on disk as csv files
            threaddata = pd.DataFrame(self.threaddata)
            commentdata = pd.DataFrame(self.commentdata)
            authors = pd.DataFrame(self.author)
            gildings = pd.DataFrame(self.gildings)
            threaddata.to_csv(
                f"{self.output_filename()}/thread_data.csv", mode="w", index=False)
            commentdata.to_csv(
                f"{self.output_filename()}/comment_data.csv", mode="w", index=False)
            authors.to_csv(
                f"{self.output_filename()}/author_data.csv", mode="w", index=False)
            gildings.to_csv(
                f"{self.output_filename()}/gildings_data.csv", mode="w", index=False)
            self.checkpoint += self.interval
        # If length of records meets the minimum condition, trigger exit function
        if (length > self.minimum):
            exectime = ((time.time() - self.exectime) / (60*60))
            print("Collected {} records so far; Total execution time: {} hours".format(
                length, exectime))
            self.exit_conditions()


def build_parser():
    """Parser to grab and store command line arguments"""
    MINIMUM = 200000
    CHECKPOINT = 10000
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subreddit", help="Specify the subreddit to scrape from")
    parser.add_argument("-m", "--minimum", help="Specify the minimum number of data records to collect",
                        type=int, default=MINIMUM)
    parser.add_argument("-c", "--checkpoint",
                        help="Save the file every c comments", type=int, default=CHECKPOINT)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    Scraper(args).addTo()


if __name__ == "__main__":
    main()
