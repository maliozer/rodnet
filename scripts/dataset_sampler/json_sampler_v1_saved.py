from tqdm import tqdm

import pandas as pd
import numpy as np
import os

os.chdir("/media/data/bderinbay/rvc_devkit/datasets/json_file/")

df_cats = pd.read_csv('categories.csv')
df_images = pd.read_csv('images.csv')
df_anno = pd.read_csv('annotations.csv')

sample_columns = ['image_id','bbox','category_id', 'category_name', 'file_name', 'height', 'width','ds_id']
df_sample = pd.DataFrame([], columns=sample_columns)


#return-> string: category name
def find_category(cat_id):
    try:
        return df_cats.name[df_cats.id == cat_id].values[0]
    except: 
        return "no-catagory"

#return-> dict annoset counted as dataset 
def get_dataset_counts(anno_set):
    dataset_names = ['coco', 'objects365', 'oid', 'mvs']
    anno_set_db = anno_set.groupby(['dataset_name']).count()
    cols = [col for col in anno_set_db.columns if col not in ['dataset_name', 'id']]
    anno_set_db = anno_set_db.drop(cols, axis=1)
    anno_set_dbcount_dict = anno_set_db.to_dict()['id']
    for dbname in dataset_names:
        if(dbname not in anno_set_dbcount_dict.keys()):
            anno_set_dbcount_dict[dbname] = 0
    return anno_set_dbcount_dict

#drop mismatched columns and join two dataframe
df_joined = df_anno.set_index('image_id').join(df_images.set_index('id'))

for cat_id in tqdm_notebook(df_cats.id.values):
    anno_set = df_joined[df_joined.category_id == cat_id]
    db_count = get_dataset_counts(anno_set)

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
        df_a['category_name'] = find_category(df_a['category_id'].values[0])
        #df_a = df_a.set_index('Index', drop=True)
        df_sample = df_sample.append(df_a)
        db_quota[a.dataset_name]+=1

df_sample = df_sample.reset_index(drop=True)