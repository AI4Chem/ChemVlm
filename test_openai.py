# -*- coding: GBK -*-
import openai

from openai import OpenAI
import os
import base64
import json
 
client = OpenAI(
    api_key="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"
)
 
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
"""
for filename in os.listdir(fig_path):
    if filename.endswith('.png'):
       image_path=os.path.join(fig_path, filename)
       print(image_path)
       base64_image = encode_image(image_path)
       messages=[
        {
            "role": "user", 
             "content": [
                {"type":"text", "text":"What's in this image?"},
                {
                   "type":"image_url",
                   "image_url":{
                      "url":f"data:image/png;base64,{base64_image}"
                      }
                }
            ]
        }
        ]
       completion = client.chat.completions.create(
          model="gpt-4o",
          messages=messages
        )
       chat_response = completion
       answer = chat_response.choices[0].message.content
       print(f'ChatGPT: {answer}')
"""

#prompt = f'����һλ��ѧ��ʦ��������һ������Ŀ�Ľ��```{}```������ݱ�׼��```{}```�ж��������Ƿ���ȷ����Ӧ�ûظ�����ȷ���򡰲���ȷ����'
#fig_path='Processed'
def test_chemvl_perform(answer_path):
    """
    test our model's performance by gpt-4o
    """
    with open(answer_path, 'r') as f:
        data_to_test = f.readlines()

    total_q_num = len(data_to_test)
    cnt_right_num = 0
    for line in data_to_test:
        line = json.loads(line)
        res = line['text']
        std_ans = line['annotation']
        human_prompt = '����һλ��ѧ��ʦ��������һ������Ŀ�Ľ��```'+res+'```������ݱ�׼��```'+std_ans+'```�ж�������ĵ÷֡������ȫ��ȷ����ش�1�֡��������ȫ������ش�0�֡������������ȷ���밴����ȷ�ı�������0-1֮��ķ�����'
        messages=[
        {
            "role": "user", 
             "content": [
                {"type":"text", "text":human_prompt},
            ]
        }
        ]
        completion = client.chat.completions.create(
          model="gpt-4o",
          messages=messages
        )
        chat_response = completion
        answer = chat_response.choices[0].message.content
        print(f'ChatGPT: {answer}')
        if "��ȷ" in answer and "����ȷ" not in answer:
            cnt_right_num += 1
        
    print(cnt_right_num/total_q_num)

if __name__ == "__main__":
    test_chemvl_perform("/mnt/petrelfs/zhangdi1/lijunxian/chemexam_repo/ChemLLM_Multimodal_Exam/results/gaokao_chemvl_ft_6_4_0-merge__all_.jsonl")