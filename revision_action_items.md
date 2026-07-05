# COSMOS 论文修改清单

本文档汇总当前论文针对三位审稿人意见需要完成的修改。清单分为必须修改、建议补强和可选实验。本文档不再把时序实验日志名中的 `scale=0.3` 当作问题：该实验实际负载为 45%，只是历史日志尾标错误。

## 一、必须修改

### 1. 明确五分钟 routing-plan 更新周期的实验目的

涉及位置：

- `sections/design.tex` 的 `Low Overhead via Partial Updates`
- `sections/implementation.tex` 的 scheduler 实现说明
- `sections/experiments.tex` 的动态负载分析

当前 Design 和 Implementation 已经从一分钟更新为五分钟，后续还应在实验设置或动态负载段落中解释：五分钟不是经过调参得到的最优周期，而是一个固定、非调优参数，用于观察 routing plan 在更新间隔内暂时过时时，COSMOS 能否处理突发负载。

建议表达：

> We use a fixed five-minute routing-update interval throughout the experiments. This interval is not selected as an empirically optimal configuration; rather, it provides a sufficiently long window for evaluating whether COSMOS can tolerate workload changes before the next routing-plan update.

动态负载实验需要明确区分两个阶段：

1. 突发刚发生、旧 routing plan 尚未更新时，COSMOS 依靠已有的 complementary partition 和 node-local scheduling 吸收变化；
2. 到达下一次五分钟更新后，系统重新调整 load partition，以适应持续的负载变化。

不要声称五分钟是最优周期，也不要声称实验已经证明 COSMOS 对任意更新周期或任意快速变化都鲁棒。

### 2. 消除 beneficial swap 与运行时 pod eviction 的术语混淆

涉及位置：

- `sections/design.tex` 的 `SwapCapacity` 算法及其解释
- `sections/experiments.tex` 的 `Impact of routing updates`

必须明确：`SwapCapacity` 中的 eviction/swap 是 routing-plan 生成过程中对 assignment matrix 的逻辑回退与重新分配，不会在每个内部迭代步骤触发 pod eviction。只有算法完成后，新旧 routing plan 的最终差异才会对运行系统产生影响。

建议将以下术语替换或限定：

- `evicted functions` → `logically displaced functions` 或 `rolled-back assignments`
- `evicted load fraction` → `displaced load fraction`
- 第一次出现变量 $\mathcal{E}$ 时注明它是规划阶段的逻辑 displacement list，不是 runtime pod-eviction list

建议加入：

> The “evictions” in `SwapCapacity` are logical rollbacks of tentative assignments during routing-plan computation, rather than runtime pod evictions. Intermediate swaps only modify the assignment matrix and are never deployed individually. Only the difference between the final routing plan and the currently deployed plan may affect the destinations of subsequent requests.

同时解释为什么不报告内部 `swaps per update`：内部 swap 次数依赖启发式搜索路径，同一 assignment 可能被多次修改，不能对应真实迁移、pod eviction 或运行时开销。因此，最终的 net demand relocation 才是有系统意义的指标。

### 3. 重新定义 swap 图的证据对象

涉及位置：

- Figure `fig:swap_analysis` 的 caption
- `Impact of routing updates` 的正文

该图应称为 consecutive routing plans 之间的 `net per-function demand relocation`，而不是 beneficial swap frequency。它表示一次算法运行中 partial update、新负载重新分配和所有内部 beneficial swaps 的最终合成结果。

需要形成以下证据链：

1. per-function relocated demand：最终 routing plan 改动的范围和幅度；
2. pod eviction rate：最终 plan 变化在运行时造成的实例驱逐；
3. minute-level cold-start rate 与 P99：routing update 是否形成性能尖峰；
4. instance lifetime CDF：是否导致更严重的 instance churn。

建议加入：

> Counting internal beneficial-swap operations would not reflect runtime disruption because intermediate assignment changes are never deployed and may be overwritten by subsequent iterations. We therefore measure the net demand relocation between consecutive deployed routing plans, which captures the routing changes visible to the running system.

### 4. 将 eviction-cascade 论证改为 instance-churn 论证

涉及位置：

- `Instance eviction under monotonic scale-up`
- `Bursty workloads handling`
- 对 Reviewer 1 和 Reviewer 3 的回复

原型无法为 eviction 标记可靠的级联因果关系，因此不要声称直接测量或排除了 eviction cascades。改为测量其可观察后果：

- eviction rate；
- scale-up-triggered eviction fraction；
- cold-start rate；
- instance lifetime；
- update-aligned P99 latency。

推荐表述：

> Although our prototype does not causally label eviction cascades, their operational consequences would appear as elevated eviction rates, shorter instance lifetimes, and increased cold starts. COSMOS exhibits the opposite trends across all three metrics under the evaluated workloads.

将过强的结论：

> monotonic scale-up does not cause frequent eviction

调整为：

> monotonic scale-up does not increase instance churn under the evaluated workloads

同样，将：

> neither load partitioning nor demand relocation introduces observable performance instability

限定为：

> under this trace and update configuration, we observe no routing-update-aligned latency spikes

### 5. 定量验证固定 CPU-to-memory ratio 假设

涉及位置：

- `sections/background.tex` 的 Figure `fig:ratio_stability_scatter`
- `sections/design.tex` 的 demand-profile 假设
- 新增 Discussion/Limitations 段落

背景图除每个函数的线性拟合 $R^2$ 外，还应补充 per-request CPU-to-memory ratio 的 CV。正文需要总结：

- 大多数目标函数具有较高的 $R^2$ 和较低的 ratio CV，资源变化主要体现为 demand magnitude 的变化；
- $R^2$ 说明 CPU 和 memory 是否共同变化；
- ratio CV 直接刻画固定 $r_i$ 的稳定程度。

正文必须避免把该假设写成对所有 serverless 函数均成立，而应明确它是 COSMOS 的目标 workload regime。

### 6. 增加 CPU-to-memory ratio 假设的适用范围与局限

建议按三类 workload 说明：

1. **近似同比变化的函数**：CPU 和 memory 随输入规模共同变化，是当前 COSMOS 的主要目标；
2. **单资源主导函数**：例如 memory working set 基本稳定而 CPU 随工作量变化。当 memory 按经过 profiling 的 working-set bound 配置且不构成活跃约束时，可以主要按 CPU 需求排序；
3. **资源类型发生转换的函数**：例如在 compute-intensive 和 memory-intensive 阶段间切换的函数，不满足当前单一 $r_i$ 模型。

不要使用“给实例配备较低比例的内存”，应使用“按经过 profiling 的稳定 working-set bound 配置内存”，避免被理解为可能导致 OOM 的激进压缩。

不要在没有数据或引用的情况下声称“完全流式 serverless 函数不是主流”。可以改为：

> such workloads are outside the dominant regime observed in our characterization

未来扩展可以表述为：每个函数维护多个 resource profiles，将请求分类到不同 profile，再把每个 profile 作为逻辑 function class 参与 routing，同时允许这些 classes 共享相同代码和 warm state。称其为 `a natural extension`，不要称为仅需 `minor changes`。

### 7. 澄清预测误差实验的误差模型与覆盖边界

涉及位置：

- `Impact of demand-prediction errors`
- Evaluation Setup 中 demand estimation 的说明

必须说明：

- 随机误差施加在 per-request demand、aggregate volume $\mathbf{V}_i$ 还是二者上；
- 随机误差的分布，例如 `±20%` 是均匀范围还是其他定义；
- 误差是逐请求、逐函数还是逐窗口采样；
- systematic bias 的施加方式；
- default/accurate predictor 的含义。

还要主动说明：该实验验证的是需求大小预测误差，并没有模拟 CPU-to-memory ratio 在请求之间发生定性转换，不能用它宣称已经验证 fixed-ratio violation。

### 8. 明确 vertical scaling 的适用场景，而非声称普遍必要

涉及位置：

- Background/Design 的 motivation
- Discussion/Limitations
- 对 Reviewer 3 Comment 1 的回复

需要承认：当请求可以稳定划分为少数 size classes，且各 class 的 popularity 高度可预测时，size-specific prewarmed pools 可能获得相当一部分收益。

COSMOS 主要适用于：

- 请求需求近似连续；
- size classes 较多；
- size mix 随时间变化；
- 为每个 class 维护独立 warm pool 会造成 warm-capacity fragmentation。

Routing* 与完整 COSMOS 的差距可以作为当前 workload 中 monotonic scale-up 有效的辅助证据，但不能单独证明 vertical scaling 在所有场景下都不可替代。

### 9. 加强消融实验中 Scheduling* 的解释

涉及位置：

- `Effectiveness of COSMOS`

当前 Scheduling* 的 throughput 比完整 COSMOS 高 6.21%，必须清楚解释为什么完整 COSMOS 仍然更好。需要强调 COSMOS 的目标不是单独最大化完成任务数，而是在 throughput、资源效率、请求公平性、cold starts 和 churn 之间取得平衡。

当前关于 Scheduling* 会优先执行立即可调度请求、使资源密集型请求主要依赖 starvation avoidance 的解释，如果没有 P99、cold-start 或 eviction 数据支撑，应使用 `suggests` 或 `we attribute this to`，不要写成已经直接证明的因果结论。

### 10. 定义 CPU/memory utilization 的准确口径

涉及位置：

- Evaluation Setup 的 Metric
- 主实验结果
- resource breakdown

`performance.csv` 中的 `cpu_usage`/`memory_usage` 在 resource breakdown 中被解释为 task execution，而 `pod_usage` 表示实例生命周期总占用。论文必须明确主实验中的 utilization 究竟是：

- 实际任务执行资源占集群容量的比例；还是
- pod allocated resource；还是
- 系统监控得到的物理资源利用率。

如果主图使用的是 task-execution share，就应避免让读者误以为它是普通的节点总利用率，并保证主实验、breakdown 和所有 improvement 数值使用一致定义。

### 11. 修正实验重复次数声明

涉及位置：

- Evaluation Setup 的 Metric

正文当前称每个数据点均由三次半小时实验平均得到，但 `performance.csv` 的 `n_runs` 在不同点之间为 1–4 次不等。必须二选一：

1. 补跑至每个数据点至少三次，并报告 mean 及误差；或
2. 按真实数据修改重复次数说明，不能继续写所有点都是三次平均。

如果补跑，建议在主要曲线或附录中报告标准差或置信区间；否则“三次平均”本身仍不足以展示波动。

### 12. 收紧主实验中的因果表述

涉及位置：

- `Benefits of COSMOS`

例如：

> This lower resource consumption results from fewer cold starts.

主实验图本身不能直接证明该因果关系，应引用紧随其后的 resource breakdown，或者改成：

> As analyzed in Figure X, this reduction is primarily associated with fewer cold starts.

Golgi 的高 tail latency 归因于 aggressive overcommitment 时，也应使用 `suggesting` 而非确定因果，除非有单独的 breakdown 数据。

### 13. 完善 Golgi baseline 的公平性说明

涉及位置：

- Evaluation Setup 的 Baselines
- revision response

需要明确：

- Golgi 是依据论文重实现，而非使用原作者实现；
- concurrency control 使用资源配置调整近似实现；
- Golgi-NoCC 是用于隔离该近似机制影响的变体，不是另一个独立 state-of-the-art baseline；
- 所有系统共享哪些公共组件、workload、resource limits 和测量代码。

避免用 Golgi 论文中“禁用 concurrency control 最多变化 14%”直接证明当前近似实现等价；它只能说明该组件在原论文中的影响范围，为当前实现提供辅助依据。

### 14. 限定 Generality 的含义

涉及位置：

- `Generality` 开头

建议明确本文只沿三个部署维度评估 generality：

- node-capacity distribution；
- function-set size；
- function-popularity skew。

不要让该标题暗示已经覆盖 CPU-to-memory ratio 转换、预测误差或任意动态负载；这些分别由 robustness、dynamic-load 和 limitation 段落处理。

### 15. 完善 scalability 的真实实验/模拟实验边界

涉及位置：

- `Scalability`

需要清楚区分：

- 16-worker 是真实 CloudLab 实验；
- 32–1024 workers 是 scheduler-load simulation；
- 模拟保留了哪些 routing/scheduling 计算；
- 模拟没有包含哪些 Kubernetes/control-plane 或网络开销。

同时核对全文 overhead 数字：Overview 中的 `under 110 ms` 与 Evaluation 中的 `below 60 ms` 是否来自不同配置。若不是，应统一；若是，应解释配置差异。

## 二、建议补强

### 16. 在 Evaluation 开头建立完整证据链

建议将实验章节结构明确概括为：

1. 主实验证明总体收益并完成 Golgi 对比；
2. resource breakdown 解释收益来源；
3. dynamic-load experiment 验证旧 plan 在更新窗口内仍能工作；
4. routing-update、eviction 和 lifetime 分析验证收益没有转化为更严重的 churn；
5. prediction robustness 验证需求大小估计不准确时仍有效；
6. generality 验证不同部署条件；
7. ablation 区分两个核心组件的贡献；
8. scalability 验证控制开销与规模扩展。

### 17. 量化 per-function relocation 的广度

Figure `fig:swap_analysis` 已经按函数展示 relocated demand，因此不需要新增 `displaced functions per swap` 指标。正文可以直接说明多个函数会被共同调整，因为 COSMOS 优先保持 function concentration 和 complementary packing，而不是最小化增量 plan changes。

如果版面允许，可以从现有图或 CSV 报告每次 update 中 relocation 非零的函数数量，但这是可选统计，不需要新增实验。

### 18. 保留但限定动态负载实验的代表性

当前实验展示一个代表性 burst episode。应写成 `a representative burst episode in the evaluated trace`，不要从单一窗口推广为所有动态 workload 的普遍保证。

### 19. 检查 instance-lifetime 外推语句

正文称：

> We observe the same trend for the other functions and offered loads.

只有在确实检查全部函数与负载后才能保留。若没有系统统计，应删除或改成仅描述图中四个 representative functions。

### 20. 增加 Discussion/Limitations

当前论文没有独立 Discussion。建议在 Evaluation 后或 Conclusion 前增加简短章节，至少覆盖：

- fixed CPU-to-memory ratio 的适用范围；
- streaming/single-resource-dominant functions；
- multi-profile future extension；
- size-class horizontal scaling 可能足够的场景；
- routing-update interval 未做最优调参；
- prototype 无法对 eviction cascade 建立逐事件因果标记。

该章节的目的不是削弱论文，而是主动限定贡献边界，避免审稿人认为作者忽略了核心假设。

## 三、可选实验

### 21. Routing-update interval sensitivity（可选，不是必须）

可比较 1、5、10 分钟下的 throughput、P99 和 net relocated demand，用于展示 responsiveness 与 routing churn 的权衡。

只有在希望声称“五分钟是合理折中或接近最优”时才需要该实验。若论文仅将五分钟定义为固定、非调优参数，并用它测试周期内 stale-plan 行为，则现有动态负载实验已经能够回答 Reviewer 2 Comment 3。

### 22. Fixed-ratio sensitivity（可选但有价值）

可以构造 per-request CPU-to-memory ratio perturbation，观察 throughput、P99 和 utilization。该实验会直接回答 ratio assumption violation，但如果背景章节已有充分的 $R^2$ 与 ratio CV 数据，并在 Discussion 中明确适用范围，可以不增加完整系统实验。

### 23. Size-class prewarmed-pool baseline（可选、成本较高）

该实验可直接回答 Reviewer 3 Comment 1，但不是当前修订的必要条件。若不做，需要通过 Discussion 明确承认少量稳定 size classes 下 horizontal scaling 可能足够，并说明 COSMOS 主要针对连续、多样和动态变化的 request sizes。

## 四、文字与排版检查

### 24. 修复审稿人指出的拼写和语法

- `Comsupmtion` → `Consumption`
- `acale-up` → `scale-up`
- `a increment-only strategy` → `an increment-only strategy`
- `three half-hour test run` → `three half-hour test runs`（仅在真实实验次数确实为三次时）
- `The sum invocation count ... are adjusted` → `The total invocation counts ... are adjusted`
- `These scheduling policies are largely ignore` → `These scheduling policies largely ignore`
- `shows the Minute-level` → `shows the minute-level`
- 检查算法注释中的 `Mapping incompletement`，改成 `Incomplete mapping`

### 25. 统一术语

全文统一以下概念：

- `routing plan update`：五分钟一次的 partial update；
- `global re-placement`：十分钟一次的全局重算；
- `beneficial swap`：规划算法内部的逻辑 assignment rollback/replacement；
- `demand relocation`：相邻已部署 routing plans 的净差异；
- `pod eviction`：运行时真实实例驱逐；
- `instance churn`：由 eviction、cold start 和 lifetime 共同反映的运行时抖动。

不要在同一段中将上述概念都简称为 `swap` 或 `eviction`。

## 五、建议的审稿意见映射

| 审稿意见 | 主要回应位置 |
|---|---|
| R1：固定 ratio 是否合理 | Background 的 $R^2$ + ratio CV；Design scope；Discussion limitations |
| R1：node contention、eviction amplification | burst cold start/P99；eviction rate；scale-up absorption；lifetime CDF |
| R1：beneficial swap 频率和副作用 | 解释 internal logical swap；net relocation；runtime churn evidence；routing overhead |
| R2：ratio assumption 与 Golgi 区别 | Background characterization；Design scope；Related Work/Introduction 的 novelty clarification |
| R2：组件创新与 breakdown | Routing*/Scheduling* 消融；明确两层机制的耦合贡献 |
| R2：动态负载与 stale plan | 五分钟周期内 burst experiment；下一次更新后的 realignment |
| R2：增加 Golgi | 主实验 Golgi/Golgi-NoCC 与实现限制说明 |
| R3：vertical scaling 何时必要 | Discussion 中的适用 regime；Routing* 与 COSMOS 作为辅助证据 |
| R3：预测错误 | prediction-noise/bias robustness 及误差模型定义 |
| R3：scale-up 是否转移为 eviction pressure | scale-up-triggered eviction fraction；eviction rate；lifetime CDF；cold starts |

## 六、当前已完成

- Design 中 routing-plan partial update 周期已从一分钟改为五分钟；
- Implementation 中 routing-plan generator 周期已从一分钟改为五分钟；
- 已删除与“一分钟工业扩缩容周期一致”的旧表述，避免与当前配置矛盾。

