import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import numpy as np
from tqdm import tqdm
from game import Game

width = 400
height = 600

action_size = 3

class WatermelonNet(nn.Module):
    def __init__(self, width, height):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 4, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.SiLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(4 * (width // 2) * (height // 2), 32)
        self.relu2 = nn.SiLU()
        self.fc2 = nn.Linear(32, action_size)
        self.relu3 = nn.SiLU()


    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu2(x)
        x = self.fc2(x)
        x = self.relu3(x)
        x = F.sigmoid(x)
        x = x.view(action_size)
        return x
    

wmnet = WatermelonNet(width, height)
optimizer = optim.Adam(wmnet.parameters(), lr=0.01)

def draw_fruit(fruits, width, height, FRUIT_SIZE):
    m = np.zeros((width,height))
    dx = np.cos(np.arange(360)*np.pi/180)
    dy = np.sin(np.arange(360)*np.pi/180)
    for obj in fruits:
        x, y ,r = obj['x'], obj['y'], obj['r']
        for i in range(360):
            px = np.int32(x + r * dx[i])
            py = np.int32(y + r * dy[i])
            if px < 0 or px >= width or py < 0 or py >= height:
                continue 
            m[px][py] = r / FRUIT_SIZE
    return m


num_episodes = 1
MAX_FRAME = 10000
total_loss = []



for episode in range(num_episodes):
    k = 0
    action_dataset = []
    with open('data.txt', 'r') as file:
        for i in file.readlines():
            if k == 0:
                np.random.seed(int(i[:-1]))
                k = 1
                continue
            a = i[:-1]
            a = [a[0]=='1',a[1]=='1',a[2]=='1']
            action_dataset.append(a)
    env = Game(width,height)
    env.run('TRAIN')
    with tqdm(action_dataset,desc='TRAIN') as t:
        for action_data in t:
            if env.running == False:
                break
            state = env.state
            score = state['score']
            fruits = state['FRUIT']
            x = torch.from_numpy(draw_fruit(fruits, width, height,env.FRUIT_SIZE)).float().view(1, 1, width, height)
            p = wmnet(x)

            env.update(action_data)

            optimizer.zero_grad()

            criterion = nn.CrossEntropyLoss()
            loss=criterion(p, torch.Tensor(action_data).float())
            loss.backward()
            t.set_postfix(loss = loss)
            optimizer.step()

    print(env.state['score'])

print("Training complete.")

seed = np.random.randint(1000,9000)+1000
np.random.seed(seed)
action_list = []
game = Game(width,height)
game.run('TRAIN')
with tqdm(range(MAX_FRAME),desc='TEST') as t:
    for i in t:
        if game.running == False:
            break
        state = game.state
        score = state['score']
        t.set_postfix(score = score)
        fruits = state['FRUIT']
        x = torch.from_numpy(draw_fruit(fruits, width, height, game.FRUIT_SIZE)).float().view(1, 1, width, height)
        p = wmnet(x)
        action = torch.bernoulli(p).bool().detach().numpy()
        game.update(action)
        action_list.append(action)

print("Test Complete")

with open('action.txt', 'w') as fp:
    fp.write("%i\n" % seed)
    for action in action_list:
        # write each item on a new line
        fp.write("%i%i%i\n" % (action[0], action[1], action[2]))
    print('Write Done')


