import sys
import os
sys.path.append(os.path.abspath('./plot/'))
from option import *
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plot
import matplotlib.ticker as ticker
import numpy as np
import csv

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height + 0.01,
                '%0.1f' % float(height),
#                '%d' % int(height),
                ha='center', va='bottom')

GROUP_NUM = 2
GROUP_NAMES = ["SuRF", "SuRF-Real8"]

GROUP_SIZE = 7
CATEGORY_NAMES = ["Uncompressed", "Single", "Double", "3-Grams, 65536", "4-Grams, 65536", "ALM-Improved, 4096", "ALM-Improved, 65536"]

CSV_SURF_FILE_PATH = "results/SuRF/point/final_fpr_email_surf.csv"
CSV_SURFREAL_FILE_PATH = "results/SuRF_real/point/final_fpr_email_surfreal.csv"
GRAPH_OUTPUT_PATH = "figures/SuRF/point/fpr_email_surf_point.pdf"

COLORS = ['#ffffff', '#fff7ec', '#fee8c8', '#fc8d59', '#d7301f', '#7f0000', '#4c0000']

Y_LABEL = "False Positive Rate (%)"

X_TICK_FONT_SIZE = 20
Y_TICK_FONT_SIZE = 16

LEGEND_FONT_SIZE = 18
LEGEND_POS = 'upper left'

f_in_surf = open(CSV_SURF_FILE_PATH)
reader = csv.reader(f_in_surf)
csvrows = list(reader)
data_surf = []
for row in csvrows :
    for item in row :
        data_surf.append(float(item) * 100)

f_in_surfreal = open(CSV_SURFREAL_FILE_PATH)
reader = csv.reader(f_in_surfreal)
csvrows = list(reader)
data_surfreal = []
for row in csvrows :
    for item in row :
        data_surfreal.append(float(item) * 100)

data = []
for i in range(0, GROUP_SIZE) :
    data.append([data_surf[i], data_surfreal[i]])

#========================================================================================
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True
mpl.rcParams['text.usetex'] = False

mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]
#========================================================================================

width = GRAPH_WIDTH  / (((GROUP_SIZE + 1) * GROUP_NUM) + 1.0)

fig = plot.figure(figsize=(GRAPH_WIDTH, 4))
ax = fig.add_subplot(111)

rect = []

for i in range(0, GROUP_SIZE) :
    if i == 0: # baseline
       hatch=HATCH
    else:
       hatch = ""
    pos = []
    for j in range(0, GROUP_NUM) :
        pos.append(width + width * i + width * j * (GROUP_SIZE + 1))
    rect.append(ax.bar(pos, data[i], width, color=COLORS[i], label=CATEGORY_NAMES[i],  linewidth = BORDER_SIZE, edgecolor = BORDER_COLOR, hatch=hatch))
    autolabel(rect[i])

xtick_pos = []
for j in range(0, GROUP_NUM) :
    xtick_pos.append(width + width * (GROUP_SIZE / 2.0) + width * j * (GROUP_SIZE + 1) - 0.5 * width)

ax.set_xticks(xtick_pos)
ax.set_xticklabels(GROUP_NAMES)

for label in ax.get_xticklabels():
    label.set_fontsize(X_TICK_FONT_SIZE)

y_ticks = [0, 10, 20, 30, 40]
ax.set_yticks(y_ticks)
ax.set_ylim(0, 40)

for label in ax.get_yticklabels():
    label.set_fontsize(Y_TICK_FONT_SIZE)

ax.set_ylabel(Y_LABEL, fontsize=Y_LABEL_FONT_SIZE - 4)

#ax.legend(loc=LEGEND_POS, prop={'size':LEGEND_FONT_SIZE})

outFile = GRAPH_OUTPUT_PATH
plot.savefig(outFile, bbox_inches='tight')
