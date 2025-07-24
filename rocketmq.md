## RocketMQ

###  [RocketMQ中文文档](https://rocketmq.apache.org/zh/docs/)

### 使用流程

#### 同步发送消息

```java
@Component
public class BpmProcessInstanceEventMQPublisher {
    public static final String TOPIC = "BPM_PROCESS_TOPIC";

    @Resource
    private RocketMQTemplate rocketMQTemplate;

    public void sendProcessInstanceResultEvent(@Valid BpmProcessInstanceStatusEvent event) {
        event.setTenantId(TenantContextHolder.getTenantId());
        rocketMQTemplate.syncSend(TOPIC +":"+ event.getProcessDefinitionKey(), event);
        // TOPIC为交主题相当于rabbit交换机，event.getProcessDefinitionKey()为标签，相当于rabbit消息队列队列
        // event 为发送消息的内容
    }
}
```

#### 接收消息

```java
@Component
@Slf4j
@RocketMQMessageListener(topic = REQUEST_CHANGE_TOPIC,
                        consumerGroup = REQUEST_CHANGEE_GROUP,
                        selectorExpression = REQUEST_CHANGE_TAG,
                        selectorType = SelectorType.TAG)
public class RequestApplicationListener implements RocketMQListener<BpmProcessInstanceStatusListenerEvent> {

    @Override
    public void onMessage(BpmProcessInstanceStatusListenerEvent event) {

    }
}
```

**topic**: 主题

**consumerGroup**：消费者组

**selectorExpression**：主题的下一级分类标签

**selectorType**: 消息以标签接收，只接收标签相同的数据

**BpmProcessInstanceStatusListenerEvent**：rocketmq会自动将传入的消息反序列化为BpmProcessInstanceStatusListenerEvent

