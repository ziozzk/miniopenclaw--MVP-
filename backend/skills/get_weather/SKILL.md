---
name: get_weather
description: 获取指定城市的实时天气信息
---

# 获取天气

## 功能
查询指定城市的当前天气状况，包括温度、湿度和天气描述。

## 使用方式
提供城市名称，返回该城市的实时天气数据。

## 示例
- 输入：北京
- 输出：北京当前天气为晴，温度 25°C，湿度 60%

## 数据源
使用 fetch_url 工具从天气 API 获取数据：
- https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_cn

## 返回格式
```
{城市}当前天气为{天气描述}，温度{温度}°C，湿度{湿度}%，风速{风速}m/s
```
