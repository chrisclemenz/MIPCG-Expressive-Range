# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:06:08 2023

@author: Christian
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def setColors(boxplot, colorList):
    for i in range(len(b['boxes'])):
        b['boxes'][i].set_facecolor(colorList[i])


questions = ['How much experience do you have with Unity? [1 = I never used it before; 5 = I use it every day]',
             'How much experience do you have with level design? [1 = None; 5 = It is my main profession]',
             'How much did the auto-complete results align with the results that you expected? [1 = Not at all; 5 = Completely]',
             'How often did you actively try to influence the AI? [1 = Never; 5 = Very often]',
             'How often did you want to override parts of the level that the AI created? [1 = Never; 5 = Very often]',
             'How much time do you feel you could save when designing levels with the tool? [1 = No time; 5 = A lot of time]',
             'How responsive did  the auto-completion feel? [1 = Very unresponsive; 5 = Very responsive]',
             'How much did the tool affect the way you designed your levels?  [ 1 = Not at all; 5 = Very much]',
             'How difficult was it for you to evaluate the auto-completion result? [1 = Very easy; 5 = Very difficult]',
             'How similar do you think the auto-completion results were to how you would design the level yourself?\n[1 = Very different; 5 = Very simillar]',
             'Which scene did you prefer working with when using the tool?',
             'How well does the tool integrate into the engine workflow? [1 = Does not integrate well; 5 = Fits very well]',
             'Which team size do you think could benefit from the tool the most? [1 = Small; 5 = Large]',
             'How much experience with the engine do you think is needed to use the editor?\n[1 = No experience; 5 = A lot of experience]',
             'Could you see yourself using the tool for your own projects? [1 = No; 5 = Yes]'
]
q1 = [4, 4, 2, 1, 1, 5, 4]
q2 = [4, 1, 2, 1, 2, 4, 1]
q3 = [1, 2, 1, 3, 3, 2, 3]
q4 = [4, 4, 4, 4, 4, 5, 5]
q5 = [4, 4, 3, 5, 3, 5, 5]
q6 = [4, 3, 1, 2, 2, 3, 2]
q7 = [5, 2, 4, 5, 4, 4, 5]
q8 = [4, 4, 3, 4, 4, 2, 3]
q9 = [2, 4, 2, 3, 2, 5, 4]
q10 = [2, 2, 1, 2, 2, 2, 2]
q11 = ['Underground Dungeon', 'Forest Temple', 'Underground Dungeon',
    'Underground Dungeon', 'Underground Dungeon', 'Forest Temple', 'Forest Temple']
q12 = [5, 4, 3, 4, 3, 3, 4]
q13 = [3, 2, 3, 3, 2, 1, 1]
q14 = [1, 2, 2, 2, 2, 3, 2]
q15 = [2, 3, 1, 2, 3, 1, 3]

groupA = [q1, q2]
groupB = [q3, q4, q5, q6]
groupC = [q7, q8, q9, q10]
groupD = [q12, q13, q14, q15]
groups = [groupA, groupB, groupC, groupD]

groupAQuestions = [questions[0], questions[1]]
groupBQuestions = [questions[2], questions[3], questions[4], questions[5]]
groupCQuestions = [questions[6], questions[7], questions[8], questions[9]]
groupDQuestions = [questions[11], questions[12], questions[13], questions[14]]
groupsQuestions = [groupAQuestions, groupBQuestions, groupCQuestions, groupDQuestions]



colors = iter([plt.cm.Accent(i) for i in range(20)])


colorList = []
for i in range(8):
    colorList.append(next(colors))

meanpointprops = dict(marker='D', markeredgecolor='black',
                      markerfacecolor='firebrick')
medianprops = dict(linestyle='-', linewidth=2.5, color='royalblue')

plt.rcParams["figure.dpi"] = 200
titles = ['General Questions','Designer Control Questions', 'Design Process Questions', 'Workflow Questions']


for i in range(len(groups)):
    answers = groups[i]
    means = np.array(answers).mean(axis=1)
    standard_deviation = np.array(answers).std(axis=1)
    questions = groupsQuestions[i]
    b = plt.boxplot(answers, patch_artist = True,showmeans=True,meanprops=meanpointprops,medianprops=medianprops)
    setColors(b, colorList)
    plt.yticks([1, 2, 3, 4, 5])
    plt.hlines([1, 2, 3, 4, 5], 0, len(answers)+1, linestyles='dotted', colors=['gray'])
    #plt.xticks([], [])
    plt.ylabel('Rating')
    plt.xlabel('Question')
    plt.title(titles[i])
    for j, line in enumerate(b['means']):
        x, y = line.get_xydata()[0]
        text = ' μ={:.2f}'.format(means[j])
        plt.annotate(text, xy=(x+0.05, y))
        text2 = ' σ={:.2f}'.format(standard_deviation[j])
        plt.annotate(text2,xy=(x+0.05, y-0.3))
        
    plt.legend(b["boxes"], questions, loc='lower center',
               bbox_to_anchor=(.5, -0.55) if i!=0 else (.5, -0.35))
    # plt.xticks([1,2],labels = [questions[0],'q2'])
    plt.show()
counts = [q11.count('Underground Dungeon'),q11.count('Forest Temple')]
plt.bar([1,2],[counts[1],counts[0]],color=[colorList[0],colorList[1]])
plt.xticks([1,2],['Forest Temple','Underground Dungeon'])
plt.yticks(range(max(counts)+1))
plt.ylabel('Number of Votes')
plt.title('Which scene did you prefer working with when using the tool?')
plt.show()