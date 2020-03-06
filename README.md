# Aspect-based Sentiment Analysis with Pytorch

Demo for aspect-based Sentiment Analysis with Pytorch and Torchtext shown at the jambit Meetup on the 6th of November 2019 and at the jambit CoffeeTalks on the 6th of March 2020.


## Repository contents

`slides`: The slides shown at the talk.

`src/notebooks`: The code shown at the talk as a [Google CoLab](https://colab.research.google.com) notebook (with a few additional comments added after the meetup to make the code more understandable).

`src/preprocessing`: The code used to get from the SemEval 2014 XML format to the csv files read in the notebook. You can get the original data from [the SemEval 2014 task web page](http://alt.qcri.org/semeval2014/task4/index.php?id=data-and-tools). Registration for metashare to download the data is free and very simple. In the meetup, I have used the restaurant part of "Train data (Laptops & Restaurants) V2.0 (released on 18/2/14)" as training data and the "Restaurants trial data (updated on 17/12/13)" as test data (because the real test data did not seem to have polarity annotations).


## Contact and Licence

(c) 2019-2020, Wiltrud Kessler

This work is shared under a [CC-BY-NC 4.0 licence](https://creativecommons.org/licenses/by-nc/4.0/).

The code is based mainly on [Ben Trevett's PyTorch Sentiment Analysis](https://github.com/bentrevett/pytorch-sentiment-analysis) distributed under a MIT License. Thank you!
