# -*- coding: GBK -*-
import openai

from http import HTTPStatus
import dashscope
from dashscope import Generation
from dashscope import MultiModalConversation
from dashscope.api_entities.dashscope_response import Role

from rdkit import Chem
from rdkit import DataStructs
import os
import base64
import json
import time
import random
from tqdm import tqdm

from time import sleep


dashscope.api_key = 'sk-eea7c876461747c5a6eebe0531164767' #qwen API-KEY
"""
client = OpenAI(
    api_key="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"
)
"""
 
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def call_qwen(question:str):
    """
    Call qwen-max to extract SMILES from generated texts and ground truth texts
    """
    messages = [
        {'role': 'user', 'content': question}]
    response = Generation.call(
        model='qwen-max',
        max_tokens=128,
        messages=messages,
        result_format='message'
        #stream=True,
        #incremental_output=True
    )
    full_content = ''
    #for response in responses:
    if response.status_code == HTTPStatus.OK:
        full_content = response.output.choices[0]['message']['content']
        
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
    return full_content

def test_chemvl_perform_single_choice(data_to_eval: dict):
    """
    evaluate single choice
    """
    prompt_template = "����һλ��Ϥ��ѧ�߿���𰸺����ֵ�ר�ң�������һ������ѡ����Ļش�:```{}```�����ж�����ش���Ϊ����ȷѡ�ע�⣬��ֻ��Ҫ�ش�һ������ѡ�����ĸ"
    human_question = prompt_template.format(data_to_eval['text'])
    
    ans = call_qwen(human_question)
    print(ans)
    if ans == data_to_eval['annotation']:
        return 1
    else:
        return 0

def test_chemvl_perform_fill_in_blank(data_to_eval: dict):
    """
    evaluate the fill-in-the-blank problem
    """
    return 


def test_chemvl_perform(ans_paths: list):
    """
    test our model's performance by qwen-max or gpt-4o
    """
    total_val_score = 0.
    total_right_score = 0.
    for answer_path in ans_paths:
        with open(answer_path, 'r') as f:
            data_to_test = f.readlines()

        total_q_num = 0.0
        cnt_right_num = 0
        cur_score = 0.0
        for line in data_to_test:
            line = json.loads(line)
            res = line['text']
            std_ans = line['annotation']
            if len(std_ans) == 1:
                score = test_chemvl_perform_single_choice(line)
                cur_score += score
                total_q_num += 1
            else:
                pass
            
            #human_prompt = f'����һλ��ѧ��ʦ��������һ����һ��{}�Ľ��```'+res+'```������ݱ�׼��```'+std_ans+'```�ж�������ĵ÷֡������ȫ��ȷ����ش�1�֡��������ȫ������ش�0�֡������������ȷ���밴����ȷ�ı�������0-1֮��ķ�������ش�ĸ�ʽӦ����: ```m��```������m��0��1����0��1֮���С����'
            #messages=[
            #{
                #"role": "user", 
                #"content": [
                    #{"type":"text", "text":human_prompt},
                #]
            #}
            #]
            #completion = client.chat.completions.create(
            #model="gpt-4o",
            #messages=messages
            #)
            
            #print(f'ChatGPT: {answer}')
            #if "1��" in answer and "0��" not in answer:
                #cnt_right_num += 1
            #cur_score += float(answer[:-1])
        if total_q_num != 0:
            print(cnt_right_num/total_q_num)
            total_val_score += total_q_num
            total_right_score += cur_score
    
    print(f"�ܷ�{total_val_score}, ģ�ͻ��{total_right_score}��")

if __name__ == "__main__":
    gaokao_chemvl_results = ['/mnt/petrelfs/zhangdi1/lijunxian/chemexam_repo/ChemLLM_Multimodal_Exam/results/gaokao_chemvl_ft_6_4_0-merge__jia.jsonl',
                             '/mnt/petrelfs/zhangdi1/lijunxian/chemexam_repo/ChemLLM_Multimodal_Exam/results/gaokao_chemvl_ft_6_4_0-merge__jia1.jsonl',
                             '/mnt/petrelfs/zhangdi1/lijunxian/chemexam_repo/ChemLLM_Multimodal_Exam/results/gaokao_chemvl_ft_6_4_0-merge__xinkebiao.jsonl']
    #gaokao_chemvl_results = ['/mnt/petrelfs/zhangdi1/lijunxian/chemexam_repo/ChemLLM_Multimodal_Exam/results/gaokao_chemvl_ft_6_4_0-merge__xinkebiao.jsonl']
    test_chemvl_perform(gaokao_chemvl_results)