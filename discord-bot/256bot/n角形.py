import matplotlib.pyplot as plt
import numpy as np

# 内角の数と大きさを定義
n = 100  # 内角の数（多めに設定）
angle = 360 / 3.5  # n角形の部分　input

# 頂点の座標を計算
vertices = []
for i in range(n):
    theta = np.radians(i * angle)
    x = np.cos(theta)
    y = np.sin(theta)
    vertices.append((x, y))

# プロット領域の作成
fig, ax = plt.subplots()

# 頂点を結ぶ辺を描画
for i in range(n):
    ax.plot([vertices[i][0], vertices[(i + 1) % n][0]],
            [vertices[i][1], vertices[(i + 1) % n][1]], color='b')

# 頂点をプロットしない
ax.set_xticks([])
ax.set_yticks([])

# グラフの設定
ax.set_aspect('equal')

# 背景色を透明に設定
ax.set_facecolor((0, 0, 0, 0))  # 背景色を透明に設定

# 枠線を非表示に
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

# 目盛りを非表示に
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# グリッドを非表示に
ax.grid(False)

# 透明なPNG画像として保存
plt.savefig("transparent_polygon_no_labels.png", transparent=True, bbox_inches='tight', pad_inches=0)
plt.show()
