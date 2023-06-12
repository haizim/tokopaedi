import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

# baca data csv
df = pd.read_csv('./tokopaedi.csv')
df = df[df.discount != 0]

kosong = {'discount': [0.0], 'quantity': [0.0], 'profit': [0.0]}
kosong = pd.DataFrame(kosong)

df = df.merge(kosong, how='outer')

# bersihkan dari outlier
q1 = df['profit'].quantile(q=0.25)
q2 = df['profit'].quantile(q=0.5)
q3 = df['profit'].quantile(q=0.75)
iqr = q3 - q1
low_th = q1 - (1.5 * iqr)
top_th = q3 + (1.5 * iqr)

clean = df[(df['profit'] >= low_th) & (df['profit'] <= top_th)]

# pisahkan antara rugi dan untung
rugi = clean[clean.profit < 0]
untung = clean[clean.profit >= 0]

# inisiasi plot
fig = plt.figure(figsize=plt.figaspect(0.5))

ax1 = fig.add_subplot(2, 4, 1, projection='3d')

# buat plot rugi
ax1.scatter(rugi.quantity, rugi.discount, rugi.profit, marker="v", color='red')
# buat plot untung
ax1.scatter(untung.quantity, untung.discount, untung.profit, marker="^")

# set nama axis
ax1.set(xlabel='quantity', ylabel='discount', zlabel='profit')
ax1.set_title('full')

rugi2 = rugi[rugi.discount == 0.2]
untung2 = untung[untung.discount == 0.2]

ax2 = fig.add_subplot(2, 4, 5)

# buat plot rugi
ax2.scatter(rugi2.quantity, rugi2.profit, marker="v", color='red')
# buat plot untung
ax2.scatter(untung2.quantity, untung2.profit, marker="^")

# set nama axis
ax2.set(xlabel='quantity', ylabel='profit')
ax2.set_title('discount = 0.2')

# group quantity & diskon
rugig = rugi.groupby(['discount', 'quantity']).agg({'profit':'sum'}).reset_index()
untungg = untung.groupby(['discount', 'quantity']).agg({'profit':'sum'}).reset_index()

# 
ax3 = fig.add_subplot(2, 4, 2, projection='3d')

# buat plot rugi
ax3.scatter(rugig.quantity, rugig.discount, rugig.profit, marker="v", color='red')
# buat plot untung
ax3.scatter(untungg.quantity, untungg.discount, untungg.profit, marker="^")

# set nama axis
ax3.set(xlabel='quantity', ylabel='discount', zlabel='profit')
ax3.set_title('grouped')

# 
rugig2 = rugig[rugig.discount == 0.2]
untungg2 = untungg[untungg.discount == 0.2]

ax4 = fig.add_subplot(2, 4, 6)

# buat plot rugi
ax4.scatter(rugig2.quantity, rugig2.profit, marker="v", color='red')
# buat plot untung
ax4.scatter(untungg2.quantity, untungg2.profit, marker="^")

# set nama axis
ax4.set(xlabel='quantity', ylabel='profit')
ax4.set_title('grouped discount = 0.2')

# summed
summed = clean.groupby(['discount', 'quantity']).agg({'profit':'sum'}).reset_index()

srugi = summed[summed.profit < 0]
suntung = summed[summed.profit >= 0]

ax5 = fig.add_subplot(2, 4, 3, projection='3d')

# buat plot rugi
ax5.scatter(srugi.quantity, srugi.discount, srugi.profit, marker="v", color='red')
# buat plot untung
ax5.scatter(suntung.quantity, suntung.discount, suntung.profit, marker="^")

# set nama axis
ax5.set(xlabel='quantity', ylabel='discount', zlabel='profit')
ax5.set_title('summed')

# grafik summed diskon 0.2
srugi2 = srugi[srugi.discount == 0.2]
suntung2 = suntung[suntung.discount == 0.2]

ax6 = fig.add_subplot(2, 4, 7)

# buat plot rugi
ax6.scatter(srugi2.quantity, srugi2.profit, marker="v", color='red')
# buat plot untung
ax6.scatter(suntung2.quantity, suntung2.profit, marker="^")

# set nama axis
ax6.set(xlabel='quantity', ylabel='profit')
ax6.set_title('summed discount = 0.2')

# grafik summed diskon 0.3
srugi3 = srugi[srugi.discount == 0.3]
suntung3 = suntung[suntung.discount == 0.3]

ax8 = fig.add_subplot(2, 4, 8)

# buat plot rugi
ax8.scatter(srugi3.quantity, srugi3.profit, marker="v", color='red')
# buat plot untung
ax8.scatter(suntung3.quantity, suntung3.profit, marker="^")

# set nama axis
ax8.set(xlabel='quantity', ylabel='profit', mouseover=True)
ax8.set_title('summed discount = 0.3')

# tabel 
urut = summed[summed.discount > 0]
urut = urut.sort_values(by=['profit'], ascending=False)
urut3h = urut.head(3)
urut3t = urut.tail(3)
urutm = urut3h.merge(kosong, how='outer')
urutm = urutm.merge(urut3t, how='outer')

ax7 = fig.add_subplot(2, 4, 4)

table = ax7.table(cellText=urutm.values, colLabels=urutm.columns, loc='center')
table[(4, 0)].set_facecolor("#111111")
table[(4, 1)].set_facecolor("#111111")
table[(4, 2)].set_facecolor("#111111")
table.auto_set_font_size(False)
table.set_fontsize(8)
# ax7.set_frame_on(False)
ax7.set(frame_on=False, xticks=[], yticks=[])
ax7.set_title('summed table head & tail')

# tampilkan plot
fig.tight_layout()
plt.show()