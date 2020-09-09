import datetime
import json
import numpy
import os
import random

from PIL import Image
from secrets import randbelow
from time import sleep

# data set up
data = dict()
data["Magikarp"] = 0
data["Gyrados"] = 0
data["Immune Magikarp"] = 0
data["Immune Gyrados"] = 0
data["Duplicate Magikarp"] = 0
data["Duplicate Gyrados"] = 0
data["Sampled"] = 0

# output directory
output_dir = './output/'
if not os.path.exists(output_dir+'Magikarp'):
    os.makedirs(output_dir+'Magikarp')
if not os.path.exists(output_dir+'Gyrados'):
    os.makedirs(output_dir+'Gyrados')

# open the original images
magikarp_image = Image.open('./assets/magikarp.png')
gyrados_image = Image.open('./assets/gyrados.png')

# image data
pokemon = dict()
# magikarp
pokemon["Magikarp"] = dict()
pokemon["Magikarp"]["primary"] = (255, 165, 82)
pokemon["Magikarp"]["secondary"] = (214, 82, 49)
pokemon["Magikarp"]["outline"] = (24, 16, 16)
pokemon["Magikarp"]["image_array"] = numpy.array(magikarp_image)
pokemon["Magikarp"]["r"], pokemon["Magikarp"]["g"], pokemon["Magikarp"]["b"], pokemon["Magikarp"]["a"] = pokemon["Magikarp"]["image_array"].T
pokemon["Magikarp"]["primary_array"] = (pokemon["Magikarp"]["r"] == 255) & (pokemon["Magikarp"]["g"] == 165) & (pokemon["Magikarp"]["b"] == 82)
pokemon["Magikarp"]["secondary_array"] = (pokemon["Magikarp"]["r"] == 214) & (pokemon["Magikarp"]["g"] == 82) & (pokemon["Magikarp"]["b"] == 49)
pokemon["Magikarp"]["outline_array"] = (pokemon["Magikarp"]["r"] == 24) & (pokemon["Magikarp"]["g"] == 16) & (pokemon["Magikarp"]["b"] == 16)

#gyrados
pokemon["Gyrados"] = dict()
pokemon["Gyrados"]["primary"] = (90, 123, 189)
pokemon["Gyrados"]["secondary"] = (148, 165, 222)
pokemon["Gyrados"]["outline"] = (24, 16, 16)
pokemon["Gyrados"]["image_array"] = numpy.array(gyrados_image)
pokemon["Gyrados"]["r"], pokemon["Gyrados"]["g"], pokemon["Gyrados"]["b"], pokemon["Gyrados"]["a"] = pokemon["Gyrados"]["image_array"].T
pokemon["Gyrados"]["primary_array"] = (pokemon["Gyrados"]["r"] == 90) & (pokemon["Gyrados"]["g"] == 123) & (pokemon["Gyrados"]["b"] == 189)
pokemon["Gyrados"]["secondary_array"] = (pokemon["Gyrados"]["r"] == 148) & (pokemon["Gyrados"]["g"] == 165) & (pokemon["Gyrados"]["b"] == 222)
pokemon["Gyrados"]["outline_array"] = (pokemon["Gyrados"]["r"] == 24) & (pokemon["Gyrados"]["g"] == 16) & (pokemon["Gyrados"]["b"] == 16)

# helper function for DNA creation
def pad(value: int):
    return str(value).zfill(3)

running = True
start = datetime.datetime.now()
while running:
    try:
        # choose the pokemon
        choice = random.choices(["Magikarp", "Gyrados"], weights = [0.9, 0.1], k=1)[0]
        data[choice] += 1
        if randbelow(8193) == 0:
            print(f'Immune {choice}!')
            data[f'Immune {choice}'] += 1
            sleep(1)
            continue
        else:
            primary = (randbelow(256), randbelow(256), randbelow(256))
            secondary = (randbelow(256), randbelow(256), randbelow(256))
            outline = (int(primary[0]*0.50), int(primary[1]*0.50), int(primary[2]*0.50))
        
        dna = ''.join(map(pad, (primary+secondary+outline)))

        # grab the image array and transpose into new palette
        arr = pokemon[choice].get("image_array")
        arr[..., :-1][pokemon[choice].get('primary_array').T] = primary
        arr[..., :-1][pokemon[choice].get('secondary_array').T] = secondary
        arr[..., :-1][pokemon[choice].get('outline_array').T] = outline

        # log the result
        if dna not in data:
            data[dna] = 1
            print(f'{choice} {dna} generated.', end='')
        else:
            data[dna] += 1
            data[f'Duplicate {choice}'] += 1
            print(f'Duplicate {choice} {dna} generated.', end='')

        # chance to randomly sample
        if randbelow(10001) == 0:
            output = Image.fromarray(arr)
            output.save(f'{output_dir}{choice}/{dna}.png')
            data["Sampled"] += 1
            print(f'.. sampled.')
            sleep(1)
        else:
            print('')
    except KeyboardInterrupt:
        running = False
delta = (datetime.datetime.now() - start).total_seconds()

print('\nGenerating file data.json...', end=' ')
with open(f'{output_dir}data.json', 'w') as f:
    json.dump(data, f, indent=4)
print('complete.\n')

total = data["Magikarp"]+data["Gyrados"]
magikarp_percent = data["Magikarp"]/total
gyrados_percent = data["Gyrados"]/total
i_magikarp_percent = data["Immune Magikarp"]/total
i_gyrados_percent = data["Immune Gyrados"]/total
d_magikarp_percent = data["Duplicate Magikarp"]/total
d_gyrados_percent = data["Duplicate Gyrados"]/total
sampled_percent = data["Sampled"]/total
print('REPORT')
print('-----------------------------')
print(f'Magikarp generated: {data["Magikarp"]} ({magikarp_percent:0.02%})')
print(f'Gyrados generated: {data["Gyrados"]} ({gyrados_percent:0.02%})')
print(f'Total generated: {total}')
print(f'Immune Magikarp generated: {data["Immune Magikarp"]} ({i_magikarp_percent:0.02%})')
print(f'Immune Gyrados generated: {data["Immune Gyrados"]} ({i_gyrados_percent:0.02%})')
print(f'Duplicate Magikarp generated: {data["Duplicate Magikarp"]} ({d_magikarp_percent:0.02%})')
print(f'Duplicate Gyrados generated: {data["Duplicate Gyrados"]} ({d_gyrados_percent:0.02%})')
print(f'Total sampled: {data["Sampled"]} ({sampled_percent:0.02%})')
print(f'Run time: {int(delta//3600)} hours, {int((delta // 60) % 60)} minutes, and {int(delta % 60)} seconds.')

exit()
