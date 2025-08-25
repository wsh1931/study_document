# 线程池的使用

## 配置

```java
package org.yunshu.docking.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * @Author: 吴思豪
 * @CreateTime: 2025-08-25
 * @Description: 线程池配置类，用于定义应用中使用的线程池实例，集中管理线程资源
 */
@Slf4j  //  lombok注解，自动生成日志对象，用于打印线程池初始化信息
@Configuration  // 标识此类为Spring配置类，Spring启动时会扫描并加载其中的Bean定义
public class ThreadPoolConfig {

    /**
     * 批量质控线程池：专门用于处理批量质控任务的线程池
     * 注：通过@Bean注解将线程池实例注册到Spring容器，名称为"batchControlExecutor"
     * 其他组件可通过@Autowired + @Qualifier("batchControlExecutor")注入使用
     */
    @Bean("batchControlExecutor")  // 定义Bean名称，用于依赖注入时指定
    public Executor qualityControlExecutor() {
        // 创建Spring提供的线程池包装类（基于JDK的ThreadPoolExecutor）
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();

        // 1. 计算核心线程数：根据CPU核心数动态设置，充分利用硬件资源
        // 原理：CPU核心数决定了并行处理的基本能力，以此为基准设置核心线程数
        int corePoolSize = Runtime.getRuntime().availableProcessors();

        // 2. 核心线程数：线程池长期维持的最小线程数量，即使线程空闲也不会销毁
        // 此处设置为CPU核心数，适用于CPU密集型与IO密集型任务的平衡场景
        executor.setCorePoolSize(corePoolSize);

        // 3. 最大线程数：线程池允许创建的最大线程数量
        // 当核心线程都在工作且任务队列满时，会创建新线程直到达到此值
        // 此处设置为核心线程数的4倍，应对突发的任务峰值
        executor.setMaxPoolSize(corePoolSize * 4);

        // 4. 任务队列容量：当核心线程都在忙碌时，新任务会进入此队列等待
        // 容量1000表示最多可缓存1000个等待任务，超过则触发拒绝策略
        executor.setQueueCapacity(1000);

        // 5. 线程名称前缀：用于日志打印和线程监控，便于区分不同线程池的线程
        // 此处命名为"batch-control-"，可快速定位批量质控任务相关的线程
        executor.setThreadNamePrefix("batch-control-");

        // 6. 拒绝策略：当线程池、队列都满时，如何处理新提交的任务
        // ThreadPoolExecutor.CallerRunsPolicy：让提交任务的线程自己执行任务
        // 优点：不会丢弃任务，且通过阻塞提交线程减缓任务提交速度，起到流量控制作用
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());

        // 7. 关闭线程池时的等待策略：设置为true表示关闭前等待所有已提交的任务执行完成
        // 避免任务被强制中断，适用于需要保证任务完整性的场景（如质控任务必须执行完毕）
        executor.setWaitForTasksToCompleteOnShutdown(true);

        // 8. 等待超时时间：配合上面的参数，设置最长等待时间（单位：秒）
        // 若超过60秒任务仍未完成，则强制关闭线程池，防止应用退出阻塞
        executor.setAwaitTerminationSeconds(60);

        // 9. 初始化线程池：应用上述配置并创建线程池实例
        executor.initialize();

        // 打印线程池初始化日志，便于运维监控和问题排查
        log.info("质控处理线程池已创建，核心线程数: {}, 最大线程数: {}, 队列容量: {}",
            corePoolSize, corePoolSize * 4, 1000);

        return executor;
    }
}

```

## 使用

```java
// 注入线程池：通过@Resource和@Qualifier指定注入名称为"batchControlExecutor"的线程池
// @Resource：JDK提供的依赖注入注解，可按名称或类型注入
// @Qualifier("batchControlExecutor")：配合注入，明确指定要注入的Bean名称（与线程池配置类中@Bean的value一致）
@Resource
@Qualifier("batchControlExecutor")
private Executor batchControlExecutor;

/**
 * 批量执行病案质控规则
 * @Author: 吴思豪
 * @return 所有数据的质控错误记录列表
 */
@Override
public List<DpZhiKongCuoWuJiLuVo> zhikongGuiZeBatch(BingAnZhiKongBo bo) {
    // 获取请求参数：标准类型（如西医/中医病案）和待质控的数据列表
    String biaoZhunLeiXing = bo.getBiaoZhunLeiXing();
    List<Map<String, String>> dataList = bo.getDataList();

    // 边界校验：若待质控数据为空，直接返回空列表（避免无意义的后续处理）
    if (CollectionUtil.isEmpty(dataList)) {
        return List.of();
    }

    // 数据质控准备：获取并过滤适用的质控规则
    // 定义需要执行的质控规则类型（国考规则、DRG分组规则）
    List<String> guoKaoLeiXings = Arrays.asList(
        QualityControlRuleTypeEnum.NATIONAL_EXAMINATION_RULE.getCode(),  // 国考规则编码
        QualityControlRuleTypeEnum.DRG_GROUPING_RULE.getCode()          // DRG分组规则编码
    );
    // 从数据库查询符合类型的所有质控规则
    List<BaseZhiKongGuiZe> zhiKongGuiZe = baseZhiKongGuiZeService.getZhiKongGuiZeByLeiXingList(null, guoKaoLeiXings);
    
    // 过滤规则：仅保留与当前标准类型匹配且脚本非空的规则（只需过滤一次，减少重复计算）
    List<BaseZhiKongGuiZe> filterZhiKongGuiZe = zhiKongGuiZe.parallelStream()  // 并行流提高过滤效率（适用于规则数量多的场景）
        // 过滤条件1：规则的标准类型与当前请求的标准类型一致（如西医规则仅用于西医病案）
        .filter(baseZhiKongGuiZe -> biaoZhunLeiXing.equals(baseZhiKongGuiZe.getBiaoZhunLeiXing()))
        // 过滤条件2：规则脚本非空（避免执行无脚本的无效规则）
        .filter(baseZhiKongGuiZe -> StringUtils.isNotBlank(baseZhiKongGuiZe.getZhiKongGuiZeJiaoBen()))
        .toList();  // 收集过滤后的规则

    // 并行处理批量数据：使用CompletableFuture结合线程池实现多任务并行执行
    // 遍历待质控数据列表，为每条数据创建一个异步任务
    List<CompletableFuture<List<DpZhiKongCuoWuJiLuVo>>> futures = dataList.stream()
        .map(data -> CompletableFuture.supplyAsync(
            // 任务逻辑：为当前数据添加标准类型标识，然后执行质控处理
            () -> {
                // 给每条数据添加"病案类型"标识（供质控规则脚本使用）
                data.put("BINGANTYPE", biaoZhunLeiXing);
                // 调用具体的质控方法（处理单条数据的质控逻辑）
                return handleZhiKong(data, biaoZhunLeiXing, filterZhiKongGuiZe);
            },
            // 指定任务执行的线程池：使用注入的"batchControlExecutor"线程池
            // 好处：统一管理线程资源，避免创建过多线程导致系统开销增大
            batchControlExecutor
        ))
        .toList();  // 收集所有异步任务的Future对象

    // 等待所有异步任务完成并合并结果
    return futures.stream()
        // 等待单个任务完成：join()会阻塞当前线程，直到任务执行完成（正常返回结果或抛出异常）
        .map(CompletableFuture::join)
        // 扁平化结果：将"List<List<...>>"转换为"List<...>"（每个任务返回的是列表，需合并为一个列表）
        .flatMap(List::stream)
        // 收集最终结果为List
        .collect(Collectors.toList());
}
```

​	在 Java 中，`@Qualifier`注解是 Spring 框架提供的核心依赖注入（DI）注解之一，主要用于**解决依赖注入时的 “歧义性问题”**—— 当一个接口有多个实现类，或一个类型有多个 Bean 实例时，仅通过`@Qualifier`（默认按名称注入）无法确定要注入哪个具体实例，此时`@Qualifier`可通过指定 “Bean 的标识” 来明确注入目标。

## 结果

```
质控规则校验数据处理时间从 2460s -> 538s（使用缓存）-> 107s（使用线程池）
```

