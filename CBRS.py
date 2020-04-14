#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


movies_df=pd.read_csv('D:\\movies.csv')
ratings_df=pd.read_csv('D:\\ratings.csv')
movies_df.head()


# In[3]:


movies_df['year']=movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)
movies_df['year']=movies_df.year.str.extract('(\d\d\d\d)',expand=False)
movies_df['title']=movies_df.title.str.replace('(\(\d\d\d\d\))','')
movies_df['title']=movies_df['title'].apply(lambda x:x.strip())
movies_df.head()


# In[4]:


movies_df['genres']=movies_df.genres.str.split('|')
movies_df.head()


# In[6]:


moviesWithGenres_df = movies_df.copy()
for index,row in movies_df.iterrows():
    for genre in row['genres']:
        moviesWithGenres_df.at[index,genre]=1
moviesWithGenres_df=moviesWithGenres_df.fillna(0)
moviesWithGenres_df.head()


# In[7]:


ratings_df.head()


# In[18]:


ratings_df = ratings_df.drop('timestamp',1)
ratings_df.head()


# In[19]:


userInput = [
            {'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ] 
inputMovies = pd.DataFrame(userInput)
inputMovies


# In[20]:


inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
inputMovies = pd.merge(inputId, inputMovies)
inputMovies = inputMovies.drop('genres', 1).drop('year', 1)
inputMovies


# In[21]:


userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]
userMovies


# In[22]:


userMovies = userMovies.reset_index(drop=True)
userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
userGenreTable


# In[23]:


inputMovies['rating']


# In[24]:


userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
userProfile


# In[25]:


genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
genreTable.head()


# In[26]:


genreTable.shape


# In[27]:


recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
recommendationTable_df.head()


# In[28]:


recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
recommendationTable_df.head()


# In[29]:


movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(20).keys())]


# In[ ]:




