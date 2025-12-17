"""
商业智能体模块
包含顾客智能体、门店智能体和商业测量智能体
"""
from mesa_geo.geoagent import GeoAgent
from shapely.geometry import Point
import random

# 默认坐标系（使用 EPSG:4326 WGS84，适合地理坐标）
try:
    from pyproj import CRS
    DEFAULT_CRS = CRS.from_epsg(4326)
except:
    DEFAULT_CRS = None


def get_nearby_agents(agent, radius):
    """
    获取指定半径内的附近智能体
    兼容不同版本的 Mesa-Geo API
    """
    try:
        # 尝试使用 distance 参数（新版本 API）
        return agent.model.space.get_neighbors(agent, distance=radius)
    except TypeError:
        try:
            # 尝试直接传递距离值（旧版本 API）
            return agent.model.space.get_neighbors(agent, radius)
        except:
            # 如果都不行，手动计算距离
            nearby = []
            for other_agent in agent.model.space.agents:
                if other_agent != agent:
                    dist = agent.geometry.distance(other_agent.geometry)
                    if dist <= radius:
                        nearby.append(other_agent)
            return nearby


class CustomerAgent(GeoAgent):
    """顾客智能体：模拟潜在顾客的随机游走行为"""
    
    def __init__(self, unique_id, model, geometry, crs=DEFAULT_CRS):
        super().__init__(model, geometry, crs)
        self.unique_id = unique_id  # 保存 ID
        self.visited_stores = []  # 记录访问过的门店
        self._original_x = geometry.x  # 保存原始坐标
        self._original_y = geometry.y
        
    def step(self):
        """每步随机移动"""
        # 随机选择移动方向（-1, 0, 1）
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        # 更新位置
        new_x = self.geometry.x + dx
        new_y = self.geometry.y + dy
        
        # 边界检查（使用模型的空间范围）
        new_x = max(0, min(self.model.width, new_x))
        new_y = max(0, min(self.model.height, new_y))
        
        # 更新原始坐标
        self._original_x = new_x
        self._original_y = new_y
        
        self.geometry = Point(new_x, new_y)


class StoreAgent(GeoAgent):
    """门店智能体：吸引顾客并记录曝光次数"""
    
    def __init__(self, unique_id, model, geometry, radius=4, name=None, crs=DEFAULT_CRS):
        super().__init__(model, geometry, crs)
        self.unique_id = unique_id  # 保存 ID
        self.radius = radius  # 影响半径
        self.exposure = 0  # 累积曝光次数
        self.name = name or f"Store_{unique_id}"
        self.daily_exposure = []  # 记录每日曝光
        self._original_x = geometry.x  # 保存原始坐标
        self._original_y = geometry.y
        
    def step(self):
        """每步统计附近的顾客数量（曝光）"""
        # 获取附近的智能体
        nearby = get_nearby_agents(self, self.radius)
        
        # 统计顾客数量
        customer_count = sum(1 for a in nearby if isinstance(a, CustomerAgent))
        self.exposure += customer_count
        
        # 记录本次曝光
        self.daily_exposure.append(customer_count)
        
        # 如果顾客在影响范围内，可以记录访问
        for agent in nearby:
            if isinstance(agent, CustomerAgent):
                if self.unique_id not in agent.visited_stores:
                    agent.visited_stores.append(self.unique_id)


class BusinessSurveyAgent(GeoAgent):
    """商业测量智能体：统计区域人流与热度指标"""
    
    def __init__(self, unique_id, model, geometry, radius=6, name=None, crs=DEFAULT_CRS):
        super().__init__(model, geometry, crs)
        self.unique_id = unique_id  # 保存 ID
        self.radius = radius  # 测量半径
        self.name = name or f"Survey_{unique_id}"
        self.measurement_history = []  # 历史测量记录
        self._original_x = geometry.x  # 保存原始坐标
        self._original_y = geometry.y
        
    def measure(self):
        """测量当前区域的人流和商业指标"""
        # 获取附近的智能体
        nearby = get_nearby_agents(self, self.radius)
        
        # 统计指标
        customer_count = sum(1 for a in nearby if isinstance(a, CustomerAgent))
        store_count = sum(1 for a in nearby if isinstance(a, StoreAgent))
        
        # 计算门店总曝光（如果有门店在范围内）
        total_exposure = 0
        for agent in nearby:
            if isinstance(agent, StoreAgent):
                total_exposure += agent.exposure
        
        # 计算人流密度（每单位面积）
        area = 3.14159 * self.radius ** 2  # 近似圆形面积
        customer_density = customer_count / area if area > 0 else 0
        
        # 计算商业热度（人流/门店比）
        business_heat = customer_count / store_count if store_count > 0 else customer_count
        
        measurement = {
            "customer_flow": customer_count,  # 人流数量
            "store_count": store_count,  # 门店数量
            "customer_density": customer_density,  # 人流密度
            "total_exposure": total_exposure,  # 总曝光
            "business_heat": business_heat  # 商业热度
        }
        
        # 记录历史
        self.measurement_history.append(measurement)
        
        return measurement
    
    def step(self):
        """每步执行测量"""
        self.measure()

