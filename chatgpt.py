from openai import OpenAI
import random
import copy
from collections import deque
import json
import os
import json
from ses import api_key, base_url

with open("label_prompt.txt", "r") as f:
  prompt = f.readlines()
  prompt = "".join(prompt)

entry = 'The llama 3 herd of models,2493,https://arxiv.org/abs/2407.21783,"Modern artificial intelligence (AI) systems are powered by foundation models. This paper presents a new set of foundation models, called Llama 3. It is a herd of language models that natively support multilinguality, coding, reasoning, and tool usage. Our largest model is a dense Transformer with 405B parameters and a context window of up to 128K tokens. This paper presents an extensive empirical evaluation of Llama 3. We find that Llama 3 delivers comparable quality to leading language models such as GPT-4 on a plethora of tasks. We publicly release Llama 3, including pre-trained and post-trained versions of the 405B parameter language model and our Llama Guard 3 model for input and output safety. The paper also presents the results of experiments in which we integrate image, video, and speech capabilities into Llama 3 via a compositional approach. We observe this approach performs competitively with the state-of-the-art on image, video, and speech recognition tasks. The resulting models are not yet being broadly released as they are still under development."'

prompt += "\nBelow is one entry: \n" + entry
print(prompt)

data_prompt = {
  "system": "You are GPT-4, answer my questions as if you were an expert in the field.",
  # Just output the prompt with no more comminicate. , and have no prefix.',
  "user": prompt,
  "model": "gpt-4o",
}

template = data_prompt


def check_answer(dic):
  try:
    flag = (
      (dic["Object_unchange"] in dic["Prompt_0"])
      and (dic["Object_unchange"] in dic["Prompt_1"])
      and (dic["Object_changed"] in dic["Prompt_0"])
      and (dic["Object_new"] in dic["Prompt_1"])
    )
    # import ipdb; ipdb.set_trace()
    return flag
    # import ipdb; ipdb.set_trace()
  except:
    # import ipdb; ipdb.set_trace()
    print("format error")
    return False


def open_ai_sdk(template, prompt=None):
  client = OpenAI(api_key=api_key, base_url=base_url)

  # tmp = copy.copy(template['user']).replace('***', str(prompt))
  # print(tmp)
  chat_completion = client.chat.completions.create(
    messages=[
      {"role": "system", "content": template["system"]},
      {"role": "user", "content": template["user"]},
    ],
    # model="gpt-35-turbo-1106",
    # model = "gpt-4-1106-preview",
    model=template["model"],
  )

  # print(prompt)
  # print('-------------------------------------------------')
  return chat_completion.choices[0].message.content


def main():
  name = "obj_replace"
  tmp = data_prompt[name]
  answer = open_ai_sdk(tmp)
  print(answer)


if __name__ == "__main__":
  main()
