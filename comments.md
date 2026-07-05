18-Apr-2026

Dear Miss Jia:

Manuscript ID TNET-2026-00030 entitled "COSMOS: Taming Heterogeneous Resource Demands in Serverless Functions with Complementary Swarming and Monotonic Scale-up" which you submitted to the IEEE Transactions on Networking, has been reviewed.  The comments of the reviewer(s) are included at the bottom of this letter. Based on my reading of the reviewers' comments, I recommend that major revisions should be made to the paper for the following reasons:

The reviewers have raised some concerns and comments with the paper, including the resource contention issue, justification of core assumptions underlying the design, clarification on novelty, overhead and side effects of beneficial swaps, more comprehensive evaluations to strengthen the effectiveness of COSMOS (e.g., compare against more state-of-the-art baselines such as Golgi), and so on. I would invite the authors to look into all of these comments in the reviews and respond to them accordingly

Please read the instructions below carefully since TNET has begun to transition to a new submission system for authors.  

If you originally submitted your manuscript through the IEEE Author Portal (these are manuscripts submitted on or after Jan. 10, 2022), you will also submit your revised manuscript through the IEEE Author Portal at https://ieee.atyponrex.com/journal/TNET.

If you originally submitted your manuscript through ScholarOne Manuscripts (these are manuscripts submitted before Jan. 10, 2022), you will also submit your revised manuscript through ScholarOne Manuscripts at https://mc.manuscriptcentral.com/tnet-ieee.

It is important that you submit your revision to the right place, so if you have any questions at all about where you should revise please contact tonea2020@gmail.com.


Please bear in mind while writing your revision that ToN prefers that papers exceeding 16 pages in length be separated into a main, self-contained paper and an online-only supplement available alongside the paper on Xplore.   Papers exceeding 16 pages to be published whole require the Associate Editor's approval.

When submitting your revised manuscript, you will be able to respond to the comments made by the reviewer(s) in the space provided.  You can use this space to document any changes you make to the original manuscript.  In order to expedite the processing of the revised manuscript, please be as specific as possible in your response to the reviewer(s).

Because we are trying to facilitate timely publication of manuscripts submitted to the IEEE Transactions on Networking, your revised manuscript should be uploaded as soon as possible.  If it is not possible for you to submit your revision by 17-Jul-2026, we may have to consider your paper as a new submission.  Please note that the time of the deadline on the due date UTC is the time of this decision - the time that this email was sent may be used as a guide - rather than the end of the day.

Once again, thank you for submitting your manuscript to the IEEE Transactions on Networking and I look forward to receiving your revision.

Sincerely,
Dr. Kai Chen
Associate Editor, IEEE Transactions on Networking
kaichen@cse.ust.hk

This decision was made by the Associate Editor.  However, as EiC, I am ultimately responsible for all editorial decisions, and any concerns about this decision should be raised directly with me.

Prof. Junshan Zhang
Editor-in-Chief, IEEE Transactions on Networking
toneic2024@gmail.com

Reviewer(s)' Comments to Author:
Reviewer: 1

Comments to the Author
Summary:

This paper presents COSMOS, a serverless resource-management system for clusters to suit the varying CPU and memory demands across functions. The key idea is to improve utilization at two levels. Across nodes, it places functions with complementary resource needs together, so that idle CPUs from memory-intensive loads can be used by compute-intensive loads, and vice versa. Within each node, it reorders requests so that a warm instance mostly scales up but avoids costly scale-down restarts. The paper claims this raises CPU and memory utilization and also improves throughput versus prior systems.



Strengths:

++ The paper addresses a very practical problem in serverless systems, which is the varying resource demands across functions. It is true that most serverless systems still assume fixed resource allocation for each function, without awareness of the load type and its actual demand, which causes resource fragmentation and performance downgrade.

++ The designs are well-motivated with corresponding insights, and are intuitively sound.

++ The experimental results show strong improvements in terms of utilization, latency, and throughput.

Weaknesses:

-- On page 1, line 50, the authors say that “54% of functions exhibit substantial variation in resource usage under different inputs.” However, on page 5, line 41, the authors claim that ”we assume this ratio remains invariant across requests of the same function.” If the resource usage varies across different inputs for the same function, is it really reasonable to set this ratio using a static value for each function? In most cases, will the CPU-to-memory ratio remain fixed if the input changes? Will there be some cases in which the function could switch between compute-intensive and memory-intensive if the input is different? For example, when using a transformer model to do an inference task, the function could be compute-intensive with a long input sequence in the prefill stage, or memory-intensive when the output sequence in the decoding stage is very long. I suggest the authors add a detailed clarification to justify this fixed ratio assumption.

-- I still have concerns about the resource contention issue. The paper also acknowledges that dynamic resizing and eviction can cause resource contention and eviction amplification on a node. The authors try to mitigate this by using complementary swarming and routing requests with similar demand to the same node. However, the evaluation mainly reports end-to-end utilization and latency improvements. It does not provide a detailed analysis of node-level contention behavior, such as eviction frequency, eviction cascades, or worst-case interference when workloads spike. If possible, is there any theoretical bound or backoff method on such contention impact? Without such analysis, it is hard to validate how the system behaves under extreme cases.

-- The overhead and side effects of beneficial swaps are not clearly analyzed. The routing algorithm allows beneficial swaps, which may evict already placed workloads to improve resource utilization. While the paper reports the overall routing-plan generation overhead and claims it is small, it does not analyze how often these swaps happen in practice or how much overhead they introduce. For example, swaps could disturb warm placements or trigger additional rescheduling overhead. A more detailed evaluation of swap frequency and its impact on system stability would strengthen the paper.



Some minor typo issues:





Fig. 10, “Comsupmtion“ → “Consumption “



Fig. 6, “acale-up“ → “scale-up“



On page 4, line 22, “a increment-only strategy“ → “an increment-only strategy“




Reviewer: 2

Comments to the Author
This paper proposes COSMOS, a two-level orchestration framework that combines request routing with monotonic scale-up scheduling, to address resource inefficiency in serverless platforms caused by heterogeneous and request-varying resource demands. Evaluation shows that COSMOS improves CPU utilization, memory utilization, and throughput over the baselines. The key idea is sound and this paper is well written. But authors could further strengthen the paper in the following aspects:

1. This paper assumes that the CPU-to-memory ratio remains invariant within the same function. However, in Section 2.1, the analysis of real-world functions only shows that resource demand varies across requests; it does not establish that the CPU-to-memory ratio is invariant for a function. So, I am concerned about whether this assumption is valid and, if not, how it may affect the design of COSMOS. Further, you state in the related work section that, unlike Golgi, COSMOS considers per-request resource demand variation. However, the current design appears to consider only variations in the magnitude of resource demand, rather than variations in the CPU-to-memory ratio itself. This makes the difference less clear.

2. It would be better to clarify the novelty. Each design components, i.e., request routing, resource-aware placement, and in-place vertical scaling— do not appear entirely new in isolation. For example, in terms of request routing, I think it is almost similar to Golgi. It would be better to clear which part constitutes the real technical novelty, and which part is mainly an integration of existing ideas. I would encourage the authors to sharpen this distinction; otherwise, it will be difficult to know what the real contribution is. Further, the performance breakdown of COSMOS helps understand each components’ performance gains.

3. More comprehensive evaluations would strengthen the effectiveness of COSMOS.
COSMOS relies on periodically generated routing plans, and this paper reports that plan generation is fast. It also uses steady-rate invocations in the experiments to avoid interference from burstiness. This makes me concerns about the effectiveness of COSMOS when the workload is rapidly shifting or difficult to predict? In realistic serverless environments, function popularity and request characteristics may change quickly, in which case a periodically generated routing plan may become stale. So, it would be better to explain and test more dynamic scenarios to demonstrate that COSMOS remains effective beyond relatively stable conditions.

4. Since the related work section discusses many relevant systems, it would strengthen the evaluation to include comparisons against more state-of-the-art baselines, such as Golgi.

Reviewer: 3

Comments to the Author
Thanks for submitting your work to ToN.

The paper is an interesting read. I like the idea of serverless function provisioning considering diverse resource footprints both at the function and request level. I feel the paper has enough novelty and tech depth in general. Please find some of my detailed questions below:

1. I hope the authors could explicitly characterize the regime in which vertical scaling is fundamentally needed/ worth the extra management complexity. If requests are highly predictable and cleanly splittable/mergeable into a small number of size classes, then predictive horizontal scaling with prewarmed size-specific pools may recover most of the benefit without in-place vertical resizing? In that case, is vertical scaling still essential? The paper needs to explain why that regime is insufficient or too costly in practice.

2. I hope the authors could better justify several core assumptions underlying the design. In particular, COSMOS relies on a per-function demand profile ⟨r_i,V_i,D_i⟩, where r_i is assumed to be a fixed CPU-to-memory ratio across all requests of the same function, and requests are routed based on their position in the historical demand distribution D_i. This is a strong assumption that is currently asserted rather than validated. I believe it may hold when request demands vary mostly in scale, but it is less convincing for functions whose inputs induce qualitatively different CPU/memory behavior across requests. Since both the complementary routing policy and the monotonic queue ordering depend on this structure, the paper should clarify when this assumption is expected to hold and how sensitive the design is when it does not.

Also, the evaluation seems to assume accurate demand knowledge: it obtains “accurate demand estimates” from benchmark input characteristics, but does not justify how such estimates would be available in realistic deployments, or evaluate what happens when demand prediction is noisy, stale, or wrong. In addition, the evaluation assumes that CPU demand scales proportionally with a fixed CPU-to-memory ratio for each benchmark. I think the paper would be much stronger if it either justified why these assumptions are realistic for its target workloads, or included a robustness study showing how performance changes under imperfect demand estimation and non-constant per-request resource ratios.

3. The scale-up scheduling avoids downscaling at the function level, but at a node level eviction may have to be triggered frequently if no downscaling is performed. It is not clear how much the proposed policy actually resolves the dynamic resource allocation problem, rather than shifting intra-function scaling overhead into inter-function contention and eviction pressure. I think the paper should better clarify this distinction and quantify how often scale-up can be absorbed by slack versus causing eviction or delayed execution.