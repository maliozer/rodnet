from tqdm import tqdm

import pandas as pd
import numpy as np
import json
import os

os.chdir("/media/data/bderinbay/rvc_devkit/datasets/json_file/")

with open('../joined_val_boxable.json') as f:
  data = json.load(f)

df_cats = pd.read_csv('categories.csv')

df_images = pd.DataFrame(data['images'])
df_images = df_images.drop(['ds_id'], axis=1)
df_images['dataset_name'] = df_images.file_name.apply(lambda x: x.split("/")[0])

df_anno = pd.DataFrame(data['annotations'])
df_anno = df_anno[:1504179]
df_anno = df_anno.drop(['file_name', 'segments_info'], axis=1)

sample_columns = ['image_id','bbox','category_id', 'category_name', 'file_name', 'height', 'width','ds_id']

"""
df_sample = pd.DataFrame([], columns=sample_columns)
"""
del data

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

df_sample = pd.DataFrame([], columns=sample_columns)

for cat_id in tqdm(df_cats.id.values):
    anno_set = df_joined[df_joined.category_id == cat_id]
    db_count = get_dataset_counts(anno_set)

    #increase the value for added annotations
    limit = 15
    db_quota = {'coco': 0, 'mvs': 0, 'objects365': 0, 'oid': 0}
    number_of_dataset=0

    #count how many database has annotation in category<-cat_id
    for x in db_count:
        if(db_count[x] > 0):
            number_of_dataset += 1

    #ilgili kategoriden hiçbir dataset te bulunamazsa
    if(number_of_dataset == 0):
        print(cat_id,": not found in -> ",number_of_dataset)
    else:
        #calculate avg quota for each database
        quota_foreach_db = int(limit / number_of_dataset)
        #loop through annotation set
        for a in tqdm(anno_set.itertuples()):
            if(db_quota[a.dataset_name] < quota_foreach_db):
                df_a = pd.DataFrame([a])

                #it uses the image_id's as Index, rename it for convenience
                df_a = df_a.rename(columns={"Index": "image_id"})
                df_a['category_name'] = find_category(df_a['category_id'].values[0])
                df_sample = df_sample.append(df_a)
                db_quota[a.dataset_name]+=1

#df_sample has zeros on index, reset and drop them
df_sample = df_sample.reset_index(drop=True)

#console outputs
print(df_sample.shape)
print(df_sample.head(5))

df_sample.to_csv('df_sample_val_v1.csv',index=False)


print("###############################")


df_sample = pd.read_csv('df_sample_val_v1.csv')

image_id_set = set(df_sample['image_id'].values)

anno_set = df_anno[df_anno.image_id.isin(image_id_set)]

df_image_set = df_images[df_images.id.isin(image_id_set)]

df_set_joined = anno_set.set_index('image_id').join(df_image_set.set_index('id'))

df_set_joined.to_csv('val_joined_annotations_v1.csv',index=False)

#will be edit with apply method
for a in tqdm(df_set_joined.itertuples()):
    df_a = pd.DataFrame([a])
    df_a= df_a.drop('Index',axis=1)
    df_a['category_name'] = find_category(df_a['category_id'].values[0])
    df_sample = df_sample.append(df_a)


df_sample.to_csv('val_sample1_200fec.csv',index=False)