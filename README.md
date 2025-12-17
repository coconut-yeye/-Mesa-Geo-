# 基于 Mesa-Geo 的地理智能体商业人流与经营潜力预测模型

## 项目简介

本项目使用 Mesa-Geo 构建了一个基于智能体建模（ABM）的商业人流与经营潜力预测模型。通过模拟顾客、门店和商业测量智能体的交互，实现可解释、可扩展的商业分析工具。

## 项目背景与创新点

### 背景

在商业选址、门店运营和广告投放中，人流量的空间分布与动态变化是核心决策依据。传统方法依赖历史数据和黑盒预测模型，但难以解释"为什么这里人多、那里人少"，也难以模拟策略变化对整体商业环境的影响。

### 创新点

- **引入商业测量智能体（Business Survey Agent）**：将 ABM 输出直接映射为可解释的商业指标
- **输出指标包括**：区域人流密度、门店曝光频次、潜在顾客停留时间，可直接用于商业决策

## 应用场景

- 模拟城市商业区内多家门店竞争同一批潜在顾客的情景
- 评估不同位置的经营潜力差异
- 选址分析和门店扩张策略
- 促销区域测试

## 技术栈

- Python >= 3.9
- Mesa >= 2.1.0
- Mesa-Geo >= 0.2.0
- GeoPandas >= 0.13.0
- Shapely >= 2.0.0
- Matplotlib >= 3.7.0
- NumPy >= 1.24.0

## 模型设计

### 智能体类型

| 智能体 | 商业含义 | 行为逻辑 |
|--------|---------|---------|
| CustomerAgent | 潜在顾客 | 随机游走 |
| StoreAgent | 门店 | 吸引顾客并记录曝光 |
| BusinessSurveyAgent | 商业测量 | 统计区域人流与热度 |

### 空间表示

- **城市区域**：二维连续空间（默认 20x20）
- **顾客/门店**：Point 几何对象
- **影响范围**：基于距离衰减的圆形区域

## 项目结构

```
geo-business-abm/
├── agents.py          # 智能体定义（顾客、门店、测量）
├── model.py           # 模型定义和调度
├── run.py             # 运行脚本和可视化
├── requirements.txt   # 依赖包列表
└── README.md          # 项目说明文档
```

## 安装与运行

### ⚠️ 重要提示

**本项目是纯本地模拟，无需任何 API key、token 或外部服务配置！**

### 1. 安装依赖

打开终端，在项目目录下运行：

```bash
pip install -r requirements.txt
```

**Windows 用户注意**：如果安装 `geopandas` 失败，建议使用 conda：
```bash
conda install geopandas
# 或使用国内镜像加速
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 验证安装（可选但推荐）

运行测试脚本检查环境：

```bash
python test_installation.py
```

如果看到 "✅ 所有依赖包已正确安装！"，说明环境配置成功。

### 3. 运行模拟

```bash
python run.py
```

### 4. 查看结果

- **控制台输出**：模拟进度和统计结果
- **图片文件**：`simulation_result.png`（自动生成）
- **图表窗口**：如果支持 GUI 会自动弹出

### 5. 自定义参数（可选）

可以在 `run.py` 中修改以下参数：

```python
model = run_simulation(
    n_steps=50,        # 模拟步数
    n_customers=50,    # 顾客数量
    n_stores=3,        # 门店数量
    n_surveys=2,       # 测量点数量
    seed=42            # 随机种子（相同种子产生相同结果）
)
```

### 常见问题

- **依赖安装失败**：查看 `QUICKSTART.md` 获取详细解决方案
- **图表不显示**：图表会保存在 `simulation_result.png`，可以手动打开查看
- **需要帮助**：运行 `python test_installation.py` 诊断问题

## 输出指标

### 门店指标

- **累积曝光次数**：门店影响范围内经过的顾客总数
- **位置信息**：门店的空间坐标

### 区域指标

- **人流数量（customer_flow）**：测量范围内的顾客总数
- **门店数量（store_count）**：测量范围内的门店总数
- **人流密度（customer_density）**：单位面积内的顾客数量
- **商业热度（business_heat）**：人流与门店的比值，反映商业活跃度

## 可视化输出

运行后会生成 `simulation_result.png` 文件，包含：

1. **空间分布图**：显示顾客、门店和测量点的位置
2. **统计信息**：门店曝光排名和区域商业潜力分析

## 运行结果示例

### 控制台输出示例

运行 `python run.py` 后，你会看到类似以下的输出：

```
==================================================
Business Flow & Potential Prediction Model
==================================================

Initialization Complete:
  - Customers: 50
  - Stores: 3
  - Survey Points: 2

Starting simulation for 50 steps...
  Completed 10/50 steps
  Completed 20/50 steps
  Completed 30/50 steps
  Completed 40/50 steps
  Completed 50/50 steps

Simulation Complete!

Generating visualization...
图表已保存至: simulation_result.png

==================================================
Final Statistics
==================================================

Store Exposure Ranking:
  1. 门店3: 342 exposures
  2. 门店2: 263 exposures
  3. 门店1: 230 exposures

Regional Business Potential Analysis:

  测量点1:
    Customer Flow: 12
    Store Count: 1
    Customer Density: 0.1061
    Business Heat: 12.00

  测量点2:
    Customer Flow: 16
    Store Count: 1
    Customer Density: 0.1415
    Business Heat: 16.00
```

### 结果解读

#### 门店曝光排名

- **门店3** 获得最高曝光（342次），说明该位置人流量最大，商业潜力最高
- **门店2** 和 **门店1** 的曝光次数分别为 263 和 230，可以用于对比分析不同位置的经营潜力

#### 区域商业潜力分析

- **Customer Flow（人流数量）**：测量范围内经过的顾客总数
- **Store Count（门店数量）**：测量范围内的门店数量
- **Customer Density（人流密度）**：单位面积内的顾客数量，数值越大表示该区域越活跃
- **Business Heat（商业热度）**：人流与门店的比值，反映商业活跃度

### 可视化图表说明

生成的 `simulation_result.png` 包含两个部分：

**左图 - 空间分布图：**
- 🔵 蓝色点：顾客智能体的位置
- 🔴 红色方块：门店位置（虚线圆圈表示影响范围）
- 🟢 绿色三角：测量点位置（点线圆圈表示测量范围）

**右图 - 统计信息：**
- 模拟参数汇总（步数、智能体数量等）
- 门店曝光统计（位置、累积曝光次数）
- 区域测量结果（人流、密度、热度等指标）

### 结果应用建议

1. **选址分析**：对比不同门店的曝光次数，选择曝光高的位置
2. **竞争分析**：分析测量点内的门店密度和人流比例
3. **策略优化**：调整门店位置或影响半径，观察曝光变化
4. **区域评估**：使用商业热度指标评估不同区域的商业潜力

## 核心代码说明

### 顾客智能体

```python
class CustomerAgent(GeoAgent):
    def step(self):
        # 随机游走
        dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
        self.geometry = Point(self.geometry.x + dx, self.geometry.y + dy)
```

### 门店智能体

```python
class StoreAgent(GeoAgent):
    def step(self):
        # 统计附近顾客（曝光）
        nearby = self.model.space.get_neighbors(self, self.radius)
        self.exposure += sum(1 for a in nearby if isinstance(a, CustomerAgent))
```

### 商业测量智能体

```python
class BusinessSurveyAgent(GeoAgent):
    def measure(self):
        # 测量区域指标
        nearby = self.model.space.get_neighbors(self, self.radius)
        return {
            "customer_flow": ...,
            "store_count": ...,
            "customer_density": ...,
            "business_heat": ...
        }
```

## 可扩展方向

1. **引入真实地理数据**：使用真实 POI / 商圈 Shapefile
2. **顾客偏好建模**：添加价格/品类偏好
3. **与真实数据校准**：使用真实客流数据进行模型校准
4. **动态门店策略**：模拟促销、价格调整等策略
5. **多时段模拟**：考虑不同时间段的人流变化

## 参考文献

- Mesa-Geo 官方文档: https://mesa-geo.readthedocs.io/
- Mesa 官方文档: https://mesa.readthedocs.io/

## 许可证

本项目仅供学习和研究使用。

## 作者

椰椰乐基于 Mesa-Geo 的商业智能体建模项目

