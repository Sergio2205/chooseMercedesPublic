
from openai import OpenAI
import base64
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
job_id = "ftjob-i2RJ4p1AINmsKxiVjGSh7VY5"
content = client.files.content('file-5vRw9nyxLMp2nYiSvPXeCr')

content.text

file_content = base64.b64decode(content.read()) 

metrics_str = 'file_contenttxt'
metrics_list = [line.split(',') for line in metrics_str.split('\n')]
df = pd.DataFrame(metrics_list[1:], columns=metrics_list[0])
df = df.apply(pd.to_numeric, errors='coerce')
df.tail()
#conversión a numéricos para graficación
df = df.apply(pd.to_numeric, errors='coerce')
df.tail()
import matplotlib.pyplot as plt

plt.figure(figsize=(7,4))
plt.plot(df['step'], df['train_accuracy'])
plt.title('Training Accuracy over Steps')
plt.xlabel('Step')
plt.ylabel('Training Accuracy')
plt.show()
plt.figure(figsize=(7,4))
plt.plot(df['step'], df['train_loss'])
plt.title('Training Loss over Steps')
plt.xlabel('Step')
plt.ylabel('Training Accuracy')
plt.show()