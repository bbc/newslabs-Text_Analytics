# BBC News Segmentation experiment

### Experimenta pipeline to segment BBC News articles and evaluate the segmentation by categories/sections from the BBC News page


This set of  scripts uses the body of selected news stories from the BBC News data in data-from-Juicer to segment the articles into a defined number of topics. In a second step the category/section label derived from the BBC News page is used to evaluate the segmentation.

#### Step 1: Create a mapping for the BBC News sections. Different sections can be grouped under one name, sections mapped to '-' will be ignored for the analysis 

Edit **categories_mapped.csv** to the reflect the number of sections you want to include, as well as the desired section mapping. Save in a new test folder, e.g. **new-test**

    	export folder=new-test
    	mkdir tests/$folder
    	save tests/$folder/categories_mapped.csv

#### Step 2: Subset the news dataset to include only the sections we want to experiment with, relabel sections to group them together.

Input:

* tab file with news stories [ section | ID | title | full text ]

Output:

* subset of news stories [ new section label | ID | title | full text ]


    	python 2-reset-categories.py $folder

#### Step 3: Run topic modelling on the corpus of the selected news stories.

Input: 

* subset of news stories [ new section label | ID | title | full text ]
* path of output folder
* number of desired topics to segment into

Output (in output folder):

* DictLDA - the dictionary
* LDAmodel.state - the model 
* docTopics.csv - csv file connecting each news story with the assigned topic ID and a probability for the assignment
* topics - a list of topic IDs
* wordTopic.csv - csv file connecting topic IDs with the x-most (default 10) relevant words for that topic
* wordTopic.string - same as wordTopic.csv, just with one line per topic ID for easier plotting

    	python 3-segment-articles.py tests/$folder/bbc-data-201601-201606_sub.tab tests/$folder/out/ 2


#### Step 4: Evaluate the predicted topic ID with the section labels given through BBC News sections.

Using the `wordTopic` and `docTopic` matrices in the respective tests output folder, plot a 'visual confusion matrix' (Rplot.pdf). To calculate a proper confusion matrix, we would have to manually assign the topic IDs (0,1,..., x) to the section labels. This could be done using the most relevant words for each topic where appropriate. 
 
	cd tests/$folder
	Rscript ../../4-plot.R 
	

	

