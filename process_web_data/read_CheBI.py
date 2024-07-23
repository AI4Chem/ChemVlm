# -*- coding: GBK -*-
import pandas as pd 
import numpy as np
import json
import os
import cv2
import yaml
from tqdm import tqdm
import random


smiles_templates = [
    "What is the name of the molecule shown in this image?",
"What kind of compound does this molecular structure represent?",
"Can you help me identify this molecule in the image?",
"What is the chemical structure in this image?",
"Can you tell me the chemical formula of this molecule?",
"What kind of molecule is shown in the image?",
"Can you explain the composition of the molecule in the image?",
"What kind of chemical molecule is in this image?",
"Can you identify the molecule in the image?",
]

smiles_chinese_templates = [
    "��������ͼƬչʾ�ķ���������ʲô��",
    "������ӽṹ�������ֻ����",
    "�ܷ����ʶ��ͼ�е�������ӣ�",
    "����ͼ���еĻ�ѧ�ṹ��ʲô��",
    "������ӵĻ�ѧʽ�ܸ�������",
    "ͼ����ʾ�������ַ��ӣ�",
    "���ܽ���һ��ͼƬ�з��ӵ������",
    "����ͼƬ�е�����һ�ֻ�ѧ���ӣ�",
    "����ʶ���ͼƬ�е����������"]



caption_templates = [
    "Can you provide a description of the molecule in the image?",
"How would you describe the molecule shown in the image?",
"Could you detail the molecule depicted in the image?",
"What are the characteristics of the molecule in the image?",
"Can you explain the features of the molecule in the image?",
"Could you elaborate on the molecule presented in the image?",
"How would you characterize the molecule shown in the image?",
"Can you outline the properties of the molecule in the image?",
"What details can you provide about the molecule in the image?",
"Can you give an overview of the molecule depicted in the image?"
]
 
iupac_templates = [
    "Can you provide the IUPAC name of the molecule depicted in the image?",
"What is the IUPAC nomenclature for the molecule in the image?",
"Could you tell me the IUPAC name for the molecule shown in the image?",
"What is the systematic IUPAC name of the molecule displayed in the image?",
"How is the molecule in the image named according to IUPAC standards?",
"What is the official IUPAC name of the molecule illustrated in the image?",
"Could you identify the IUPAC name of the molecule in the image?",
"What would the IUPAC name be for the molecule presented in the image?",
"Can you specify the IUPAC designation of the molecule shown in the image?",
"What is the formal IUPAC name for the molecule in the image?",
]

iupac_chinese_templates = [
"ͼ�з��ӵ�IUPAC������ʲô��",
"���ܸ�����ͼ�з��ӵ�IUPAC������",
"ͼ����ʾ�������IUPAC������ʲô��",
"���ͼ�з��ӵ�IUPAC��׼������ʲô��",
"����ͼ����ʾ�ķ��ӵ�IUPAC������ʲô��",
"ͼ����ʾ���ӵ�ϵͳIUPAC������ʲô��",
"ͼ�з��ӵ�IUPAC��ʽ������ʲô��",
"�����ṩͼ�з��ӵ�IUPAC������",
"ͼ����ʾ���ӵ�IUPAC������ʲô��",
"ͼ����ʾ�Ļ�ѧ���ӵ�IUPAC�����������ģ�"
]

smiles_answer_templates = english_expressions = [
    "I believe the molecular formula in this image, when represented with SMILES, should be {}.",
    "From my perspective, the molecular structure in the image is written in SMILES format as {}.",
    "In my view, the molecular formula displayed in the image with a SMILES representation is {}.",
    "According to my understanding, the molecular formula in the image can be represented in SMILES as {}.",
    "I think the chemical structure in this image, when described with SMILES, is {}.",
    "From my personal perspective, the molecular structure in the image can be represented with SMILES as {}.",
    "As I observe, the molecular formula in this image, expressed in SMILES format, should be {}.",
    "My interpretation is that the molecular formula in this image, according to SMILES format, is {}.",
    "In my opinion, the SMILES expression of the molecular formula shown in this image should be {}.",
    "For me, the SMILES representation of the molecule in the image should be {}.",
    "My analysis shows that the molecular formula in this image is represented in SMILES format as {}.",
    "In my view, the molecular structure in this image is expressed in SMILES notation as {}.",
    "Based on my analysis, the molecular formula displayed in the image, if written in SMILES, would be {}.",
    "I guess the molecular formula in this image, if expressed in SMILES syntax, would be {}.",
    "From my angle, the molecular formula in the image in SMILES format is {}.",
    "I speculate that the molecular formula in this image, expressed in SMILES format, could be {}.",
    "Based on my observation, the molecular formula in this image, as per SMILES, is {}.",
    "I estimate that the molecular structure in this image, written in SMILES, should be {}.",
    "My opinion is that the molecular structure of the image in SMILES format is {}.",
    "In my view, the molecular formula in the image translated into SMILES language should be {}.",
    "From my perspective, the molecular structure in this image, represented in SMILES format, is {}.",
    "My understanding is that the molecular structure in the image, represented with SMILES code, is {}.",
    "From my vantage point, the molecular formula in the image, if represented with SMILES, would be {}.",
    "From my analysis, the molecular formula in this image expressed in SMILES syntax is {}.",
    "My judgment is that the molecular structure displayed in the image, written in SMILES, should be {}.",
    "I believe the chemical structure in this image, when converted to SMILES format, is {}.",
    "I feel that the molecular formula in this image, represented in SMILES fashion, is {}.",
    "I believe that the molecular structure in this chart, if represented with SMILES syntax, is {}.",
    "From a scientific viewpoint, the molecular formula in this image, marked with SMILES, should be {}.",
    "I am confident that the molecular structure shown in this image, expressed in SMILES format, would be {}."
]

chinese_smiles_answers = [
    "����Ϊ����ͼƬ��ķ���ʽ����SMILES��ʾӦΪ {}��",
    "���ҿ�����ͼƬ�еķ��ӽṹ��SMILES��ʽд�� {}��",
    "�ҵĿ����ǣ���ͼ��ʾ�ķ���ʽ��SMILES��ʾ���� {}��",
    "�����ҵ���⣬ͼ�еķ���ʽ����SMILES��ʽ��ʾΪ {}��",
    "�Ҿ��ã����ͼƬ�еĻ�ѧ�ṹ����SMILES������������ {}��",
    "���Ҹ��˵ĽǶȳ�����ͼƬ��ķ��ӽṹ��SMILES���Ա�ʾΪ {}��",
    "���ҹ۲죬��ͼ�еķ���ʽ��SMILES��ʽ��ӦΪ {}��",
    "�ҵĽ���ǣ����ͼ�еķ���ʽ����SMILES��ʽ�� {}��",
    "���ҵļ��⣬����ͼƬչʾ�ķ���ʽ��SMILES���Ӧ���� {}��",
    "������˵����ͼƬ�з��ӵ�SMILES��ʾӦ�� {}��",
    "�ҵķ�����ʾ������ͼ�еķ���ʽ��SMILES��ʽ��ʾΪ {}��",
    "���ҿ���������ͼƬ�еķ��ӽṹ��SMILES���ʽ�� {}��",
    "���ҷ�����ͼ��չʾ�ķ���ʽ�����SMILESд����Ӧ�� {}��",
    "�Ҳ������ͼƬ�ķ���ʽ�������SMILES�﷨�������� {}��",
    "���ҵĽǶ��жϣ�ͼƬ����ʾ����ʽ��SMILES��ʽ�� {}��",
    "���Ʋ�����ͼƬ�еķ���ʽ����SMILES��ʽ�������� {}��",
    "�����ҵĹ۲죬���ͼƬչʾ�ķ���ʽ����SMILES��˵�� {}��",
    "�ҹ������ͼ�ķ��ӽṹ����SMILES��ʽд������Ӧ���� {}��",
    "�ҵ�����ǣ���ͼ�ķ��ӽṹ��SMILES��ʽ��ʾ��Ϊ {}��",
    "���ҿ�����ͼ�еķ���ʽת����SMILES����Ӧ���� {}��",
    "����֮�������ͼƬ�еķ��ӽṹ��SMILES��ʽ��ʾΪ {}��",
    "�ҵ�����ǣ�ͼ�еķ��ӽṹ����SMILES�����ʾ���� {}��",
    "���ҵ��ӽǣ���ͼƬ�еķ���ʽ�������SMILES��ʾ������ {}��",
    "���ҵķ�������������ͼƬ�еķ���ʽ��SMILES�﷨��Ϊ {}��",
    "�ҵ��ж��ǣ����ͼչʾ�ķ��ӽṹ����SMILES��дӦ�� {}��",
    "����Ϊ����ͼƬ�еĻ�ѧ�ṹ��ת����SMILES��ʽ������ {}��",
    "�Ҹо�����ͼ�еķ���ʽ����SMILES�ķ�ʽ��ʾ�������� {}��",
    "����Ϊ���ͼ���еķ��ӽṹ����SMILES�﷨��ʾ������ {}��",
    "�ӿ�ѧ���ӽ�����������ͼƬ�еķ���ʽ��SMILES��ǣ�Ӧ�� {}��",
    "����������ͼƬչʾ�ķ��ӽṹ������SMILES��ʽ�������� {}��"
]

caption_answer_templates = [
    "As I see it, {}",
"To my mind, {}",
"In my view, {}",
"Personally, I think {}",
"In my assessment, {}",
"It seems to me {}",
"I believe that {}",
"To me, {}",
"As far as I'm concerned, {}"
]

iupac_answers = [
     "I think the molecular formula in this image, when given its IUPAC name, should be {}",
"In my opinion, the IUPAC name for the molecular formula in this image should be {}",
"I am convinced that the IUPAC name for the molecule shown in this image should be {}",
"It is my belief that the molecular formula depicted here, when named using IUPAC standards, should be {}",
"From my perspective, the molecular formula in this image should be named according to IUPAC as {}",
"I hold the view that the molecule in the image, when expressed with its IUPAC name, should be {}",
"It seems to me that the molecular formula shown in this image should have the IUPAC name {}",
"I consider that the IUPAC name for the molecular formula illustrated in this image should be {}",
"I feel that the IUPAC name for the molecule depicted in this image should be {}",
"To my mind, the molecular formula in this image, when converted to its IUPAC name, should be {}",
"In my assessment, the IUPAC name for the molecule in this image should be {}",
"I would suggest that the molecular formula shown here, when translated into IUPAC nomenclature, should be {}",
"My view is that the IUPAC name for the molecular formula in this image should be {}",
"I reckon that the molecule displayed in this image, when named using IUPAC conventions, should be {}",
"I assert that the IUPAC name for the molecular formula shown in this image should be {}",
"My perspective is that the molecular formula depicted in the image should be given the IUPAC name {}",
"I surmise that the IUPAC name for the molecule in the image should be {}",
"It is my opinion that the molecular formula in this image, when represented by its IUPAC name, should be {}",
"I maintain that the molecule in the image should be named with the IUPAC name {}",
"I gather that the IUPAC name for the molecular formula depicted in this image should be {}"
]

iupac_chinese_answers = [
    "�Ҿ���ͼ�з��ӵ�IUPAC������ {}",
"���ҿ�����ͼ�з��ӵ�IUPAC������ {}",
"����֮����ͼ�з��ӵ�IUPAC������ {}",
"���ҵĽǶ�������ͼ�з��ӵ�IUPAC������ {}",
"���Ҷ��ԣ�ͼ�з��ӵ�IUPAC������ {}",
"�ҵĿ����ǣ�ͼ�з��ӵ�IUPAC������ {}",
"�ҵĹ۵��ǣ�ͼ�з��ӵ�IUPAC������ {}",
"�����ţ�ͼ�з��ӵ�IUPAC������ {}",
"������֪��ͼ�з��ӵ�IUPAC������ {}",
"����֮����ͼ�з��ӵ�IUPAC������ {}",
"�͸��˶��ԣ�����Ϊͼ�з��ӵ�IUPAC������ {}",
"�Ҹ��˵�����ǣ�ͼ�з��ӵ�IUPAC������ {}",
"�ҵ�����ǣ�ͼ�з��ӵ�IUPAC������ {}",
"���Ʋ�ͼ�з��ӵ�IUPAC������ {}",
"�ҵĽ����ǣ�ͼ�з��ӵ�IUPAC������ {}",
"���ҿ�����ͼ�з��ӵ�IUPAC������ {}",
"�ҳ��еĹ۵��ǣ�ͼ�з��ӵ�IUPAC������ {}",
"���ҵ�����������ͼ�з��ӵ�IUPAC������ {}",
"�ҹ���ͼ�з��ӵ�IUPAC������ {}",
"����Ϊͼ�л������IUPAC������ {}"
]

def add_image_token(text):
    a = random.choice('01')
    if a == '0':
        text = '<image>\n' + text
    else:
        text = text + '\n<image>'
    return text

def get_prompt_from_templates(template):

    return add_image_token(random.choice(template))

def get_ans_from_templates(template, raw_ans):
    
    return random.choice(template).format(raw_ans)

def read_data(path: str):
    """
    convert parquet to dict list
    """
    df = pd.read_csv(path)
    print(df.columns)
    #print(len(df.values))
    #print(df['description'].values[0])
    #print(df['choices'].values[0])
    data = df.to_dict('records') #ת��Ϊ�ֵ��б�Ĺؼ��䣡����

    """
    for root, _, files in os.walk('/mnt/petrelfs/zhangdi1/lijunxian/CheBI/image'):
        files_names = files
        break
    """
    print(data[0].keys())
    return data

def gen_smiles_dataset(data, img_store_path: str):
    """
    make qa pairs of smiles
    """
    #print(data)
    prompt_list = list()
    for index, line in tqdm(enumerate(data), desc='gen smiles'):
        #print(line['CID'])
        q_id = 'chebi_smiles' + str(line['CID'])
        lang = random.choice(['english','chinese'])
        if lang == 'english':
            prompt = get_prompt_from_templates(smiles_templates)   
            ans_prompt = get_ans_from_templates(smiles_answer_templates, line['SMILES'])
        else: 
            prompt = get_prompt_from_templates(smiles_chinese_templates)   
            ans_prompt = get_ans_from_templates(chinese_smiles_answers, line['SMILES'])
        #q_type = line['question_type']
        if index==0:
            print(ans_prompt)
        
        imgs = []
        
        cid_num = line['CID']
        image_np = cv2.imread('/mnt/petrelfs/zhangdi1/lijunxian/CheBI/image/'+f'CID_{cid_num}.png')
        #��numpy���󱣴�Ϊjpg��ʽ��ͼƬ�ļ�
        cv2.imwrite(img_store_path + f"{index}.png", image_np)
        imgs.append(img_store_path + f"{index}.png")
        
        conversations = {'id': q_id, 'images': imgs, 'conversations':[{'from':'human', 'value': prompt}, {'from':'gpt', 'value': ans_prompt}]}
        

        prompt_list.append(conversations)
    
    return prompt_list

def gen_caption_dataset(data, img_store_path: str):
    """
    make qa pairs of molecule captions
    """
    #print(data)
    prompt_list = list()
    for index, line in tqdm(enumerate(data), desc='gen caption'):
        q_id = 'chebi_caption' + str(line['CID'])
        prompt = get_prompt_from_templates(caption_templates)
        
        ans_prompt = get_ans_from_templates(caption_answer_templates, line['description'].replace('The', 'the'))
        #q_type = line['question_type']
        if index==0:
            print(ans_prompt)
            image_np = cv2.imread(img_store_path + f"{index}.png")
        
        imgs = []
     
        #image_np = cv2.imread(img_store_path + f"{index}.png")
        #��numpy���󱣴�Ϊjpg��ʽ��ͼƬ�ļ�
        #cv2.imwrite(img_store_path + f"{index}.png", image_np) ֻ��Ҫд��һ�μ���
        imgs.append(img_store_path + f"{index}.png")
        
        conversations = {'id': q_id, 'images': imgs, 'conversations':[{'from':'human', 'value': prompt}, {'from':'gpt', 'value': ans_prompt}]}
        

        prompt_list.append(conversations)
    
    return prompt_list

def gen_iupac_dataset(data, img_store_path: str):
    """
    make qa pairs of molecule captions
    """
    #print(data)
    prompt_list = list()
    for index, line in tqdm(enumerate(data), desc='gen iupac'):
        q_id = 'chebi_iupac' + str(line['CID'])
        lang = random.choice(['english','chinese'])
        if lang == 'english':
            prompt = get_prompt_from_templates(iupac_templates)
            ans_prompt = get_ans_from_templates(iupac_answers, line['iupacname'])
        else:
            prompt = get_prompt_from_templates(iupac_chinese_templates)
            ans_prompt = get_ans_from_templates(iupac_chinese_answers, line['iupacname'])
        #q_type = line['question_type']
        if index==0:
            print(ans_prompt)
            image_np = cv2.imread(img_store_path + f"{index}.png")
        
        imgs = []
     
        #image_np = cv2.imread(img_store_path + f"{index}.png")
        #��numpy���󱣴�Ϊjpg��ʽ��ͼƬ�ļ�
        #cv2.imwrite(img_store_path + f"{index}.png", image_np) ֻ��Ҫд��һ�μ���
        imgs.append(img_store_path + f"{index}.png")
        
        conversations = {'id': q_id, 'images': imgs, 'conversations':[{'from':'human', 'value': prompt}, {'from':'gpt', 'value': ans_prompt}]}
        

        prompt_list.append(conversations)
    
    return prompt_list


def write_total_data(prompt_list: list, file_path: str):
    writer = open(file_path, 'w')
    for item in prompt_list:
        writer.write(json.dumps(item, ensure_ascii=False) + '\n')
    writer.close()   
    
    print("Finish!")
    return 


    

if __name__ == "__main__":
    #print('A'+1)
    """
    raw_data_1 = read_data('/mnt/petrelfs/zhangdi1/ChemQA/data/train-00000-of-00002.parquet')
    raw_data_2 = read_data('/mnt/petrelfs/zhangdi1/ChemQA/data/train-00001-of-00002.parquet')
    raw_data = raw_data_1 + raw_data_2
    """
    raw_data = read_data('/mnt/petrelfs/zhangdi1/lijunxian/CheBI/test.csv')
    smiles_prompt_list = gen_smiles_dataset(raw_data, '/mnt/hwfile/ai4chem/share/cheBI/test/')
    caption_prompt_list = gen_caption_dataset(raw_data, '/mnt/hwfile/ai4chem/share/cheBI/test/')
    iupac_prompt_list = gen_iupac_dataset(raw_data, '/mnt/hwfile/ai4chem/share/cheBI/test/')

    total_list = smiles_prompt_list+caption_prompt_list+iupac_prompt_list
    write_total_data(total_list, '/mnt/petrelfs/zhangdi1/lijunxian/datagen/cheBI_test.jsonl')
    #convert_bytes_to_images(raw_data, '/mnt/hwfile/ai4chem/share/chemqa/val/', '/mnt/petrelfs/zhangdi1/lijunxian/datagen/chemqa_val.jsonl')