
from openai import OpenAI
import random
import copy
from collections import deque
import json
import os
import json
import jsonlines
# 设置 API key 和 API base URL
api_key = ""
base_url = "http://gpt-proxy.jd.com/gateway/azure"
data_prompt = dict(
    obj_replace= {'system': 'You are GPT-4, answer my questions as if you were an expert in the field.' ,
                # Just output the prompt with no more comminicate. , and have no prefix.',

                'user': "Below is a paragraph from an academic paper. Polish the writing to meet the academic style, improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. Furthermore, list all modification and explain the reasons to do so in markdown table. \
                    With the development of text-to-image (T2I) generation based on diffusion models~\cite{nichol2021glide, ramesh2022hierarchical,rombach2022high,saharia2022photorealistic}, creative image generation has gradually attracted attention, especially visual concept generation, which allows generating certain concepts of the reference images, which is more flexible and controllable than T2I. The visual concepts in an image can be divided into three orthogonal parts, including content (various semantic subjects, background, etc.), style (art style, color, etc.), and composition (relationship, camera view, layout, pose, etc.). These concepts can be used to generate individually or combined to generate creative results. \
                ", 
                'model': "gpt-4o-mini",
                }
)

def check_answer(dic):
    try:
        flag = (dic['Object_unchange'] in dic['Prompt_0']) and (dic['Object_unchange'] in dic['Prompt_1']) and (dic['Object_changed'] in dic['Prompt_0']) and (dic['Object_new'] in dic['Prompt_1'])
        # import ipdb; ipdb.set_trace()
        return flag
        # import ipdb; ipdb.set_trace()
    except:
        # import ipdb; ipdb.set_trace()
        print('format error')
        return False

def open_ai_sdk(template, prompt=None):
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # tmp = copy.copy(template['user']).replace('***', str(prompt))
    # print(tmp)
    chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": template['system'],
                    },
                    {
                        "role": "user",
                        "content": template['user'],
                    }
                ],
                # model="gpt-35-turbo-1106",
                # model = "gpt-4-1106-preview",
                model = template['model'],
            )

    # print(prompt)
    # print('-------------------------------------------------')
    return chat_completion.choices[0].message.content

def main():
    name = 'obj_replace'
    tmp = data_prompt[name]
    answer = open_ai_sdk(tmp) 
    print(answer)
        


if __name__ == '__main__':
    main()
