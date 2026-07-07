# COSMOS 修订进度与后续清单

最后更新：2026-07-05

本文档根据当前源码和本轮讨论整理。状态含义：

- `[x]` 已写入论文或绘图代码并完成编译；
- `[~]` 已完成一部分，仍有明确后续工作；
- `[ ]` 尚未修改；
- `[-]` 经讨论决定不做。

时序实验的真实 offered load 为 45%。历史日志名中的 `scale=0.3` 只是旧尾标，后续不再将其视为论文问题。

## 一、已完成

### [x] 1. Routing-plan 更新周期统一为五分钟

- `sections/design.tex` 已从 every minute 改为 every five minutes；
- `sections/implementation.tex` 已改为 five-minute execution period；
- 已删除“与常见一分钟扩缩容周期一致”的旧表述；
- Figure 中的 routing-update 标记本身也是五分钟周期。

“为什么选五分钟”的回复信文本已记录在第 9 项。

### [x] 2. Figure 1 增加 ratio-stability 统计并修正 streaming 展示

- 所有子图均报告线性拟合 $R^2$ 和 per-input CPU-to-memory ratio CV；
- Video Proc. 使用从 0 开始的 memory 横轴，避免自动缩放夸大其微小内存变化；
- Uploader 的 memory 完全恒定，因此标注 $R^2=\mathrm{N/A}$；
- Video Proc. 和 Uploader 仍保留 CV，以统一统计口径并透明展示例外；
- Figure 1 的代码和 PDF 已重新生成。

相关文件：

- `FaaSSingle/scripts/ratio_profiling/analyze.py`
- `figures/fig_ratio_stability_grid.pdf`

### [x] 3. Background 增加 fixed-ratio 的实证说明

Background 当前已说明：

- 10 个函数随机选自 SeBS，覆盖 Web、Multimedia、Utility、ML 和 Scientific workloads；
- 测量任务执行期间的 CPU time 和 peak memory；
- 散点、线性拟合、$R^2$ 和 ratio CV 的含义；
- 8/10 benchmark 呈现较强 CPU--memory coupling，$R^2$ 为 0.974--0.999，ratio CV 为 5.2\%--29.7\%；
- 函数通常执行细粒度、单一目的任务，因此输入主要改变需求规模，而不常引起 compute-/memory-intensive 类型切换；
- Video Proc. 和 Uploader 是 constant-memory streaming 例外；
- graph-mst 因版面省略，但公开报告 $R^2=0.996$、CV=27.9\%。

Caption 已简化，避免与正文重复。

### [x] 4. Benchmark Table 与 Figure 1 的职责分离

主文 Table 1 已改为半栏表，仅保留：

- Workload；
- Type；
- Duration。

主文现在明确：

- Table 1 展示 benchmark 类型和执行特征；
- Figure 1 展示 task-level resource consumption；
- CPU/memory configuration 与 allocation ratio 是实验构造参数，不是 Figure 1 的实测斜率。

### [x] 5. 创建共享 Appendix A：实验资源配置

已创建：

- `sections/appendix_resource_configurations.tex`

Appendix A 报告：

- CPU configuration；
- memory configuration；
- specified allocation ratio。

配置被描述为：

> conservative empirical values selected according to the observed end-to-end runtime behavior

Evaluation 中 CPU allocation 的表述已改为：

> using the specified resource allocation ratio for each benchmark (Appendix A)

该 Appendix 同时被：

- 主论文末尾引用；
- 独立 `supplement.tex` 引用。

### [x] 6. Generality 主文压缩并迁移完整结果至 Appendix B

主文 Generality 目前只保留：

- 一段简短结论；
- 一个 0.9 栏宽的半栏汇总表；
- 100\% offered load 下的绝对值与相对提升。

汇总表分为四组：

1. Default configuration；
2. Resource distribution；
3. Number of functions；
4. Workload skew。

每个数据项采用：

> Best baseline / COSMOS (+relative gain)

提升比例统一保留两位小数。

完整 load-sweep 图、场景定义和逐项分析已迁移到：

- `sections/appendix_generality.tex`

该文件作为 Appendix B 同时进入主论文末尾和独立 supplement。

### [x] 7. Figure 15 的预测误差定义与图例

已完成：

- 图例 `COSMOS (accurate)` 改为 `COSMOS (no injected error)`；
- 正文使用 `unperturbed setting`，不再暗示预测完全准确；
- $\pm x\%$ random error 定义为：每次 routing update 对每个函数预测负载独立乘以 $1+\epsilon$，其中 $\epsilon\sim U[-x,x]$；
- $\pm y\%$ systematic bias 定义为：所有函数预测负载持续乘以固定系数 $1+y$ 或 $1-y$；
- 补充说明随机扰动会放大函数间、更新周期间以及高负载下的性能波动；
- Figure 15 已重新生成并编译。

### [x] 8. 主论文与独立 supplement 共用附录源文件

- 主文正文、References 和 Bio 先结束；
- 使用 `\clearpage` 后再放 Appendix A/B；
- `supplement.tex` 独立生成 online supplement；
- 两份 PDF 共享同一组 appendix 源文件，避免内容漂移。

当前编译页码：

- Conclusion：第 16 页；
- Bio 结束：第 17 页；
- Appendices：第 18--19 页；
- 独立 supplement：2 页。

正文加 Bio 距离 16 页目标仍差约 1 页。

## 二、必须继续修改

### [x] 9. 解释为什么使用五分钟 routing-update interval

- `sections/implementation.tex` 已说明 routing-update interval 是可配置参数：负载波动较强时可缩短，负载稳定时可延长，以减少负载重新划分造成的性能扰动；
- Evaluation Setup 不再额外解释五分钟的选择；
- 回复信中说明：本次将周期调整为五分钟，是为了提供足够长的观察窗口，以更清楚地展示下一次 routing-plan update 之前周期内突发负载的影响，不声称五分钟是最优值。

拟用回复信文本：

> We changed the routing-plan update interval to five minutes to provide a sufficiently long observation window for more clearly evaluating the impact of bursty workload changes before the next plan update. This setting is intended to expose system behavior within an update period rather than to represent an empirically optimal update interval. We have also clarified in the Implementation section that the interval is configurable and can be adjusted according to workload volatility.

### [x] 10. 消除 beneficial swap 与 runtime pod eviction 的术语混淆

- `SwapCapacity` 的返回符号已从 $\mathcal E$ 统一改为 $\mathcal S$；
- 统一使用 `internal swap list`、`swapped fraction` 和 `swapped-out demand`；
- 已明确 internal swap 是 routing-plan computation 中对 assignment matrix 的逻辑重分配步骤，可以涉及从旧 plan 保留的 assignment 或当前 update 中产生的 assignment；
- 不再使用 `rollback`、`evicted functions`、`evicted load fraction` 或 `eviction list` 描述算法内部操作；
- 已明确 internal swaps 只修改 assignment matrix，不会直接触发 runtime pod migration 或 eviction。

最终 plan 的 net relocation、lazy runtime application 及实际系统影响由第 11--12 项继续处理。

拟用回复信文本：

> Thank you for pointing out the potential runtime side effects of beneficial swaps. We have clarified that a beneficial swap in `SwapCapacity` is an internal logical reassignment during routing-plan computation, rather than a runtime pod eviction or migration. It may involve assignments retained from the previous plan or assignments produced during the current update, but each internal operation only modifies the assignment matrix and is never deployed individually. To avoid the previous ambiguity, we rename the internal list from $\mathcal E$ to $\mathcal S$ and consistently use the terms `internal swap list` and `swapped fraction`. The runtime observes only the net difference between consecutive finalized routing plans, whose system-level effects are evaluated through demand relocation, pod eviction, cold starts, and tail latency.

### [x] 11. 将 swap 图明确为 net demand relocation

- Figure caption 已改为相邻 finalized routing plans 之间的 `net per-function demand relocation`；
- 已明确该指标是 partial updates、new-load allocation 和 internal beneficial swaps 的最终合成结果，而不是 internal swap count；
- 已说明 internal swaps 不会被单独部署，且可能在 plan computation 中被后续操作覆盖；
- routing-plan changes 随后续请求 lazy application，不会立即迁移所有受影响实例；
- 已将 plan-level net relocation 与 runtime pod eviction、cold-start rate 和 update-aligned P99 连成证据链。

### [x] 12. 明确 eviction amplification 与 instance churn 的评价边界

- 正文中的 `eviction amplification` 指一次 scale-up 直接驱逐多个 co-located pods，而不是递归 eviction cascade；
- 论文原文未声称直接测量 eviction cascade，因此不增加“撤回旧 claim”的表述；
- request-level recursive cascade 缺少可定义的 pod reconstruction lineage，因为 pod 被多个 invocation 共享，且被驱逐 pod 无法与后续同函数 pod 一一对应；
- function-level eviction peaks 只能提供时序相关性，不能唯一识别递归传播链；
- Evaluation 使用 scale-up-triggered eviction、overall pod-eviction rate、cold starts、P99 和 instance lifetime 评价直接 eviction pressure 及 aggregate instance churn；
- 已将 routing-update 结论限定为当前 trace 和 update configuration，并将 monotonic scale-up 结论限定为 evaluated workloads；
- lifetime 图展示四个 representative functions，另外六个函数也观察到相同趋势。

拟用回复信文本：

> Thank you for raising the concern about node-level contention and eviction amplification under dynamic resizing. In our paper, eviction amplification refers to the direct fan-out of a scale-up event, where one resize may evict multiple co-located pods. To evaluate whether this risk translates into runtime instability, the revised manuscript reports the fraction of scale-up events that trigger pod eviction, the overall pod-eviction rate, cold-start rate, tail latency, and instance-lifetime distributions. From 45\% to 100\% offered load, the number of scale-up events in COSMOS increases by 6.34$\times$, whereas the number causing eviction increases by only 1.48$\times$; consequently, their fraction falls from 5.05\% to 1.18\%. Across all evaluated systems, fewer than 15\% of scale-up events cause pod eviction. COSMOS also achieves a pod-eviction rate of 1.433 events/min, 60.6\% below the best baseline in the burst experiment, while exhibiting longer instance lifetimes and no routing-update-aligned tail-latency spikes outside the burst window.
>
> We distinguish this directly observable eviction amplification from a recursive request-level eviction cascade. Tracing such a cascade would require a causal lineage from an evicted pod to its reconstruction and subsequent evictions. However, a serverless pod is shared across multiple invocations, and an evicted pod has no one-to-one correspondence with a subsequently created pod of the same function. Therefore, a unique request-level reconstruction chain is not defined by the execution model. At the function level, correlated eviction peaks can be observed, but they do not identify a unique recursive chain. Accordingly, we evaluate the directly observable eviction pressure and its aggregate operational consequences rather than treating recursive cascades as a separate performance metric. We have also revised the corresponding conclusions to state that COSMOS does not increase observable instance churn under the evaluated workloads and configuration.

### [x] 13. 完成 fixed CPU-to-memory ratio 的适用范围说明

- Background 用 $R^2$、ratio CV、8/10 coupling 和两个 streaming exceptions 说明实测现象；
- Design 在引入 fixed-ratio assumption 时引用 Figure 1，并将适用范围指向 Discussion；
- Discussion 明确当前模型主要面向需求规模变化但 resource profile 近似稳定的函数；
- 对 single-resource-dominant streaming functions，当前方案仍能工作，但 fixed ratio 可能过度分配变化较小的资源；
- 对同一函数内无法分离的定性 profile 切换，单一 ratio 不足，未来需要 multiple profiles 和 request-level classification；
- 将独立 CPU/memory demand modeling 称为 `a natural extension`，并说明还需要 serverless platform 暴露可独立调节的 per-resource allocation。

拟用回复信文本：

> Thank you for raising this important question. We agree that a single CPU-to-memory ratio cannot fully represent functions whose requests switch between qualitatively different resource profiles, such as the transformer prefill and decoding behaviors highlighted by the reviewer. We have strengthened the empirical validation of our assumption by measuring CPU and memory demands across multiple inputs. As shown in the revised Figure 1, eight of the ten evaluated benchmarks retain a stable function-specific resource direction as their demand magnitude changes. We have also clarified the scope of the model in the revised Discussion. COSMOS primarily targets fine-grained functions with an approximately stable resource profile. Complex applications with distinct execution phases are commonly decomposed into separate functions, allowing each phase to be provisioned independently. If qualitatively different phases are inseparably embedded within one function, the current single-ratio model is insufficient; supporting such workloads would require multiple resource profiles and request-level profile classification. For the two single-resource-dominant streaming benchmarks in our evaluation, the current design remains applicable but may over-allocate the less variable resource. Independently modeling CPU and memory demand is a natural extension, whose full benefit would also require serverless platforms to expose independently adjustable per-resource allocations.

### [x] 14. 明确 vertical scaling 值得使用的 workload regime

Discussion 已明确 size-specific prewarmed pools 的核心难点是为每个函数确定 size-class boundaries：

- 划分过粗会保留较大的类内需求差异，因而仍需过度分配；
- 划分过细会将 warm capacity 分散到多个 pool，降低实例复用率；
- vertical scaling 无需预先确定 size boundaries，因而能避免这一 granularity trade-off；
- 当函数只有少数稳定请求类型，或调用量足以保证每个细粒度 pool 都有高复用率时，size-specific pools 仍然合适；
- 不用 Routing* 消融来宣称 vertical scaling 在所有 workload 中都必不可少。

拟用回复信文本：

> We agree that predictive horizontal scaling with size-specific prewarmed pools may recover much of the benefit of vertical scaling in some regimes. However, the central challenge of this approach is determining function-specific boundaries for partitioning requests into resource-size classes. Coarse classes preserve substantial within-class demand variation and therefore require over-provisioning, while fine-grained classes fragment warm capacity and reduce instance reuse. Size-specific pools are particularly suitable when a function serves only a few stable request types, or when its invocation volume is high enough to maintain reuse within every fine-grained pool. COSMOS targets workloads outside these regimes, where heterogeneous request demands make this granularity trade-off significant. Monotonic vertical scaling avoids predefined size boundaries by allowing a warm instance to serve requests with different demands. We have added this distinction to the revised Discussion and clarified that vertical scaling is not universally required.

### [x] 15. 完成 prediction-error 实验的覆盖边界说明

已完成随机误差分布、逐函数逐更新采样、systematic bias、no-injected-error 基准和性能波动说明。该段已明确限定为 predicted-load error，不再额外插入 fixed-ratio 限制；resource-profile scope 由第 13 项的独立实证和 Discussion 处理。

### [x] 16. 加强 Scheduling* 吞吐率更高的解释

当前 Scheduling* throughput 比完整 COSMOS 高 6.21\%。需要说明：COSMOS 的目标不是只最大化完成任务数，而是联合考虑资源效率、公平性、cold starts 和 churn。

若没有额外 P99/cold-start/eviction 数据支撑，对原因的解释使用：

- `suggests`；或
- `we attribute this to`。

不要写成已直接证明的因果结论。

### [-] 17. 明确 CPU/memory utilization 指标口径

经讨论决定不再增加定义。正文沿用系统论文中 CPU/memory utilization 表示实际任务资源占用的常规含义，resource breakdown 已进一步区分 task execution、cold start、standby instance 和 idle resource。

### [x] 18. 修正实验重复次数声明

已删除与 `performance.csv` 中 `n_runs=1--4` 不一致的 `averaged from three half-hour test run` 声明，改为所有实验均运行半小时，并排除前五分钟 warm-up 数据。不为各 case 虚构统一的重复次数。

### [x] 19. 收紧主实验因果表述

- `lower resource consumption results from fewer cold starts` 已改为 `is primarily associated with fewer cold starts`；
- Golgi 高 tail latency 已改为 `suggesting that its relatively aggressive overcommitment involves a tail-latency trade-off`，不将其写成已证明的因果关系。

### [x] 20. 完善 Golgi baseline 的公平性说明

- 已明确同时评估两种实现：用资源配置调整近似 concurrency control 的 Golgi，以及省略该机制的 Golgi-NoCC；
- 保留原 Golgi 论文中“禁用 concurrency control 最多改变 14\% 性能”的结果，用于说明 performance detection 和 Mondrian Forest routing 构成其主要收益；
- Baselines 段后已说明所有方法均依据原论文在同一 prototype 中重实现，其他系统组件保持一致。

### [x] 21. 完善 scalability 的真实/模拟边界

已完成：全文 overhead 数字已统一为当前结果，Evaluation 报告 routing-plan generation below 60 ms。

仍需说明：

- 16-worker 是真实 CloudLab 实验；
- 64--1024 workers 是 scheduler-load simulation；
- simulation 保留哪些 routing/scheduling 计算；
- 未包含哪些 Kubernetes control-plane、网络或 RPC 开销。

### [x] 22. 增加简短 Discussion/Limitations

已在 Evaluation 后新增 Discussion，完成：

- fixed-ratio 适用范围与 streaming exceptions；
- independent resource modeling 和 multi-profile extension；
- 算法扩展与 serverless platform allocation interface 之间的依赖。

不再在 Discussion 中额外引入 eviction-cascade limitation；正文原本未声称测量 recursive cascade，相关评价边界由第 12 项的 Evaluation 文本和回复信处理。

五分钟 update interval 的选择动机只放在回复信，正文 Implementation 仅说明该参数可配置。

## 三、建议补强

### [x] 23. 重写 Evaluation 开头的证据链

已用三句话按当前实验结构概括：主实验对比与 resource breakdown、bursty workload 与 relocation/eviction/lifetime churn 证据，prediction robustness、generality、ablation 和 scalability。

### [-] 24. 限定动态负载实验的代表性

将其称为：

> a representative burst episode in the evaluated trace

不要从单一窗口推广为对所有动态 workload 的普遍保证。

### [x] 25. 检查 instance-lifetime 外推

正文仍有：

> We observe the same trend for the other functions and offered loads.

只有确实检查全部函数和负载后才能保留；否则删除，或仅描述图中的四个 representative functions。

### [x] 26. Generality 的范围已限定

主文与 Appendix B 均明确只沿三类维度评估：

- node-capacity distribution；
- function-set size；
- function-popularity skew。

## 四、经讨论决定不新增的实验或图

### [-] 27. 不新增 routing interval sensitivity

不比较 1/5/10 分钟。回复信说明调整为五分钟是为了更清楚地观察更新周期内突发负载的影响；正文只说明该周期可根据 workload volatility 调整，不声称五分钟最优。

### [-] 28. 不新增 fixed-ratio sensitivity 系统实验

使用 Figure 1 的 $R^2$、ratio CV、streaming exceptions，以及 Discussion 中的适用范围说明回应。不能声称已经验证资源 profile 定性切换。

### [-] 29. 不新增 eviction-cascade 图

由于原型无法可靠标记 cascade 因果关系，使用 eviction rate、cold starts、P99 和 lifetime CDF 论证 instance churn。

### [-] 30. 不新增 internal swap-count / NoSwap 图

内部 swap 是不可独立部署的启发式步骤，计数依赖搜索路径，且 partial update、新负载重分配与 SwapCapacity 无法分离。使用最终 net relocation 及运行时影响作为系统级证据。

### [-] 31. 不新增 size-class prewarmed-pool baseline

通过 Discussion 明确承认其适用场景，并限定 COSMOS 的目标 regime。

### [-] 32. 不新增其他主文图表

当前图组已经覆盖 reviewer 关注点。后续重点是定义、证据链、限制和 rebuttal，而不是增加实验数量。

## 五、文字、排版与页数

### [x] 33. 修复已知拼写和语法

已完成：

- `acale-up` → `scale-up`；
- `a increment-only strategy` → `an increment-only strategy`；
- `Mapping incompletement` → `Incomplete mapping`；
- `The sum invocation count ... are adjusted` → `The total invocation counts ... are adjusted`；
- `shows the Minute-level` → `shows the minute-level`；
- `These scheduling policies are largely ignore` → `These scheduling policies largely ignore`；
- 最终 PDF 文本中未发现 `Comsupmtion`。

### [x] 34. 统一 swap/relocation/eviction/churn 术语

- `routing-plan update`：每五分钟执行的 partial update；
- `global routing-plan recomputation`：每十分钟执行的全局重算；
- `beneficial swap`：规划算法内部对 assignment matrix 的逻辑 replacement，不使用 `rollback` 或 `eviction` 描述；
- `internal swap list` $\mathcal S$ / `swapped fraction` $\beta_k$：`SwapCapacity` 的内部输出；
- `demand relocation`：相邻 routing plans 之间 per-function assignment 的净差异；
- `pod eviction`：资源压力下真实发生的 runtime pod removal；
- `instance churn`：由 pod eviction、cold start 和 instance lifetime 体现的 aggregate instance turnover。

### [~] 35. 控制主文在 16 页以内

已完成：

- Benchmark Table 改为半栏；
- resource configurations 移入 Appendix A；
- Generality 完整图与分析移入 Appendix B；
- 16-worker large-cluster 完整图与分析移入 Appendix B，主文仅保留 100\% load 结论；
- Appendix 强制从正文和 Bio 之后的新页面开始。

当前状态：Bio 结束于第 17 页，仍需节省约 1 页。后续优先考虑：

- 压缩 Design 中 SwapCapacity 的重复解释；
- 压缩 benchmark/workload setup 与 Related Work 的重复文字；
- 完成 Discussion 后重新评估总页数。

## 六、Reviewer—证据映射

| Reviewer concern | 主文证据与后续动作 |
|---|---|
| R1/R2/R3：fixed ratio 是否合理 | Figure 1 的 $R^2$ + ratio CV 已完成；仍需 Design scope 与 Discussion limitations |
| R1：node contention / eviction amplification | burst cold start/P99、eviction rate、scale-up absorption、lifetime CDF；改用 instance-churn 论证 |
| R1：beneficial swap 频率与副作用 | internal logical swap 解释、net relocation、runtime churn、routing overhead；正文术语仍待改 |
| R2：novelty 与组件贡献 | Routing*/Scheduling* 消融；仍需收紧 Scheduling* 解释及 Introduction/response 中的 novelty 表述 |
| R2：stale routing plan | 五分钟窗口内 burst + 下一次 update；周期选择的回复信文本已记录 |
| R2：Golgi baseline | 主实验已有 Golgi/Golgi-NoCC；公平性说明仍待完善 |
| R3：vertical scaling 何时值得 | Discussion 中限定 regime；Routing* 差距仅作辅助证据 |
| R3：prediction error | Figure 15 的随机/系统误差定义已完成；仍需声明不覆盖 profile 类型转换 |
| R3：scale-up 是否转化为 eviction pressure | scale-up-triggered eviction、eviction rate、lifetime CDF、cold starts；改写为 churn 证据链 |

## 七、下一步建议顺序

1. 修改 beneficial swap / relocation / pod eviction 术语（第 10--12 项）；
2. 增加 Discussion/Limitations，集中完成 fixed ratio 与 vertical scaling scope（第 13、14、22 项）；
3. 修正 metric、重复次数和主实验因果表述（第 17--19 项）；
4. 完善 Golgi 与 scalability 公平性/边界（第 20--21 项）；
5. 统一拼写、术语和页数（第 33--35 项）；
6. 最后撰写逐条 reviewer response。
