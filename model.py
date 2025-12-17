"""
商业模型模块
定义 BusinessModel 和空间环境
"""
from mesa import Model
from mesa_geo import GeoSpace
import random
from shapely.geometry import Point
from agents import CustomerAgent, StoreAgent, BusinessSurveyAgent


class BusinessModel(Model):
    """商业人流与经营潜力预测模型"""
    
    def __init__(self, n_customers=50, n_stores=3, n_surveys=2, width=20, height=20, seed=None):
        """
        初始化模型
        
        参数:
            n_customers: 顾客数量
            n_stores: 门店数量
            n_surveys: 测量点数量
            width: 空间宽度
            height: 空间高度
            seed: 随机种子
        """
        super().__init__()
        if seed is not None:
            random.seed(seed)
        
        # Mesa 3.x 使用 agents_list 代替 schedule
        self.agents_list = []
        # 设置 GeoSpace 使用相同的 CRS，避免坐标转换问题
        try:
            from pyproj import CRS
            space_crs = CRS.from_epsg(4326)
            self.space = GeoSpace(crs=space_crs)
            # 禁用 CRS 转换警告
            GeoSpace.warn_crs_conversion = False
        except:
            self.space = GeoSpace()
        self.width = width
        self.height = height
        self.n_customers = n_customers
        self.n_stores = n_stores
        self.n_surveys = n_surveys
        
        # 创建顾客智能体
        for i in range(n_customers):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            customer = CustomerAgent(f"customer_{i}", self, Point(x, y))
            self.space.add_agents(customer)
            self.agents_list.append(customer)
        
        # 创建门店智能体（集中在中心区域）
        store_positions = [
            (width/2 - 3, height/2),
            (width/2, height/2),
            (width/2 + 3, height/2)
        ]
        for i in range(n_stores):
            if i < len(store_positions):
                x, y = store_positions[i]
            else:
                x = random.uniform(width/4, 3*width/4)
                y = random.uniform(height/4, 3*height/4)
            store = StoreAgent(f"store_{i}", self, Point(x, y), radius=4, name=f"门店{i+1}")
            self.space.add_agents(store)
            self.agents_list.append(store)
        
        # 创建商业测量智能体（分布在关键区域）
        survey_positions = [
            (width/4, height/4),  # 左上
            (3*width/4, 3*height/4)  # 右下
        ]
        for i in range(n_surveys):
            if i < len(survey_positions):
                x, y = survey_positions[i]
            else:
                x = random.uniform(width/4, 3*width/4)
                y = random.uniform(height/4, 3*height/4)
            survey = BusinessSurveyAgent(
                f"survey_{i}", 
                self, 
                Point(x, y), 
                radius=6, 
                name=f"测量点{i+1}"
            )
            self.space.add_agents(survey)
            self.agents_list.append(survey)
        
        # 记录运行统计
        self.running = True
        self.step_count = 0
    
    def step(self):
        """执行一步模拟"""
        # Mesa 3.x: 随机打乱顺序后执行所有智能体的 step 方法
        random.shuffle(self.agents_list)
        for agent in self.agents_list:
            agent.step()
        self.step_count += 1
    
    def get_store_statistics(self):
        """获取门店统计信息"""
        stores = [a for a in self.space.agents if isinstance(a, StoreAgent)]
        return {
            store.name: {
                "exposure": store.exposure,
                "position": (getattr(store, '_original_x', store.geometry.x), 
                            getattr(store, '_original_y', store.geometry.y)),
                "radius": store.radius
            }
            for store in stores
        }
    
    def get_survey_results(self):
        """获取测量结果"""
        surveys = [a for a in self.space.agents if isinstance(a, BusinessSurveyAgent)]
        return {
            survey.name: survey.measurement_history[-1] if survey.measurement_history else {}
            for survey in surveys
        }

