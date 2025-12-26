import matplotlib.pyplot as plt
import numpy as np

# 1. 创建背景数据
requests = np.arange(1, 9)
demands = np.random.uniform(0.5, 1.5, 8) # 随机需求

# 2. 创建画布和子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
fig.suptitle('Inefficiencies of Baseline Scaling Strategies')

# 3. 绘制背景直方图（两个子图相同）
for ax in (ax1, ax2):
    bars = ax.bar(requests, demands, color='lightgray', edgecolor='black')
    ax.set_xlabel('Request Index')
    ax.set_ylim(0, 2.5)

# 4. 子图(a): 添加虚线表示超额配置
overprovision_height = 2.0
ax1.hlines(overprovision_height, 0.5, 8.5, colors='r', linestyles='dashed', label='Static Allocation')
ax1.fill_between([0.5, 8.5], demands.max(), overprovision_height, color='r', alpha=0.1, label='Excess Headroom')
ax1.legend()
ax1.set_title('(a) Over-provisioning')

# 5. 子图(b): 添加箭头表示频繁调整
ax2.set_title('(b) Frequent Resizing')
for i, d in enumerate(demands):
    # 模拟一个剧烈波动的“实际分配”线
    allocated = d + np.random.uniform(-0.7, 0.7)
    # 绘制箭头
    arrow_color = 'green' if allocated >= d else 'red'
    arrow_width = 0.05 if allocated >= d else 0.1
    ax2.arrow(i+1, d, 0, allocated-d, head_width=0.2, head_length=0.1, 
              fc=arrow_color, ec=arrow_color, width=arrow_width)
    
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()