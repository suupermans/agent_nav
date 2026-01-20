def _parse_response(self, response: str, request: TripRequest) -> TripPlan:
    """
    解析Agent响应

    Args:
        response: Agent响应文本
        request: 原始请求

    Returns:
        旅行计划
    """
    try:
        # 尝试从响应中提取JSON
        # 查找JSON代码块
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "{" in response and "}" in response:
            # 直接查找JSON对象
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            json_str = response[json_start:json_end]
        else:
            raise ValueError("响应中未找到JSON数据")

        print(json_str, 'json_str')
        # 解析JSON
        data = json.loads(json_str)

        # 转换为TripPlan对象
        trip_plan = TripPlan(**data)

        return trip_plan

    except Exception as e:
        print(f"⚠️  解析响应失败: {str(e)}")
        print(f"   将使用备用方案生成计划")
        return self._create_fallback_plan(request)