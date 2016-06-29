# BBC News Segmentation

### Pipeline to segment BBC News articles and evaluate the segmentation by categories/sections from the BBC News page

This set of python scripts uses the body of selected news stories from the BBC News data in data-from-Juicer to segment the articles into a defined number of topics. In a second step the catgegory/section label derived from the BBC News page is used to evaluate the segmentation.


#### Step 1: Create a mapping for the 106 BBC News sections, different sections can be grouped under one name, sections mapped to '-' will be ignored for the analysis 

Edit **categories_mapped.csv** to the reflect the number of sections you want to include, as well as the desired section mapping. Save in a new test folder, e.g. **new-test**

    	export folder=new-test
    	mkdir tests/$folder
    	save tests/$folder/categories_mapped.csv

#### Step 2: 

