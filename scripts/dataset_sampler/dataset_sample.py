import pandas as pd
import numpy as np

import json

from tqdm import tqdm

with open('../joined_val_boxable.json') as f:
  data = json.load(f)


limit = 20
sample_category_counter = np.zeros(640,dtype = int)

#parsing data as dataframe
df_anno = pd.DataFrame(data['annotations'])
df_images = pd.DataFrame(data['images'])
df_cats = pd.read_csv("categories.csv")

del data

def find_category(cat_id):
    try:
        return df_cats.name[df_cats.id == cat_id].values[0]
    except: 
        return "no-catagory"

def get_annotations(img_id):
   df_annoset = df_anno[df_anno.image_id==img_id]
   for x in df_annoset.values:
       image_id = img_id
       bbox = x[3]
       category_id = x[4]
       if(category_id > 0 and category_id < 641):
           if(sample_category_counter[category_id-1] < limit):
               category_name = find_category(category_id)
               sample_row = [image_id, bbox, category_id, category_name]
               sample_category_counter[category_id-1] += 1
               return sample_row
           else:
               pass
   return(None)


#give a set of annotation candidate count how many of them in which dataset as dict
def get_dataset_counts(anno_set):
  anno_set_db = anno_set.groupby(['dataset_name']).count()
  cols = [col for col in anno_set_db.columns if col not in ['dataset_name', 'id']]
  anno_set_db = anno_set_db.drop(cols, axis=1)
  anno_set_dbcount_dict = anno_set_db.to_dict()['id']
  return anno_set_dbcount_dict

#%%


sample_columns = ['image_id','bbox','category_id', 'category_name', 'file_name', 'height', 'width','ds_id']
df_sample = pd.DataFrame([], columns=sample_columns)


#%%


for x in tqdm(df_images.values):
    file_name = x[1]
    print(file_name)
    """
    row = get_annotations(x[4])
    if(row is not None):
        height = x[2]
        width = x[3]
        ds_id = x[5]
        
        row.append(file_name)
        row.append(height)
        row.append(width)
        row.append(ds_id)
        
        df_row = pd.DataFrame([row], columns=sample_columns)
        
        df_sample = df_sample.append(df_row)


df_sample.to_csv('sample_data.csv', index=False)
"""

#%%

df_anno = pd.read_csv("annotations1.csv")
df_images = pd.read_csv("images.csv")
df_cats = pd.read_csv("categories.csv")

#%%

#drop mismatched columns and join two dataframe
df_joined = df_anno.set_index('image_id').join(df_images.set_index('id'))

for x in tqdm_notebook(df_cats.id.values):
  anno_set = df_joined[df_joined.category_id == x]
  
  #sample solution 1
  df = anno_set.sample(n=200)
  break




  #increase the value for added annotations
limit = 200
db_quota = {'coco': 0, 'mvs': 0, 'objects365': 0, 'oid': 0}
df_sample = pd.DataFrame([], columns=sample_columns)
number_of_dataset=0
for x in db_count:
  if(db_count[x] > 0):
    number_of_dataset += 1
quota_foreach_db = int(limit / number_of_dataset)

for a in tqdm_notebook(anno_set.itertuples()):
  if(db_quota[a.dataset_name] < quota_foreach_db):
    df_a = pd.DataFrame([a])
    df_a = df_a.rename(columns={"Index": "image_id"})
    df_a['category_name'] = find_category(df_a['image_id'].values[0])
    #df_a = df_a.set_index('Index', drop=True)
    df_sample = df_sample.append(df_a)
    db_quota[a.dataset_name]+=1
df_sample = df_sample.reset_index(drop=True)