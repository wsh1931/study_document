# 热部署

添加此配置文件取消thymeleaf缓存

```yml
spring:
  thymeleaf:
    prefix: classpath:/static/templates
    suffix: .html
    cache: false
    mode: HTML5
```

![image-20250807153157819](images/image-20250807153157819.png)

![image-20250807153235870](images/image-20250807153235870.png)