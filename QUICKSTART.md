# 快速启动指南

## ✅ 好消息：无需任何配置！

这个项目是**纯本地模拟**，**不需要 API key、token 或任何外部服务**。

## 🚀 三步运行

### 步骤 1: 安装依赖

打开终端（PowerShell 或 CMD），在项目目录下运行：

```bash
pip install -r requirements.txt
```

如果安装较慢，可以使用国内镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 2: 运行模拟

```bash
python run.py
```

### 步骤 3: 查看结果

运行后会：
- 在控制台显示模拟进度和统计结果
- 自动生成 `simulation_result.png` 可视化图表
- 弹出图表窗口（如果支持 GUI）

## 📋 依赖包说明

项目需要的包都在 `requirements.txt` 中：
- `mesa` - 智能体建模框架
- `mesa-geo` - 地理空间扩展
- `geopandas` - 地理数据处理
- `shapely` - 几何操作
- `matplotlib` - 可视化
- `numpy` - 数值计算

**所有包都是开源免费的，无需注册或配置！**

## ⚙️ 自定义参数（可选）

如果想修改模拟参数，编辑 `run.py` 文件的最后几行：

```python
model = run_simulation(
    n_steps=50,        # 模拟步数（可以改成 100、200 等）
    n_customers=50,    # 顾客数量（可以改成 100、200 等）
    n_stores=3,        # 门店数量（可以改成 5、10 等）
    n_surveys=2,       # 测量点数量
    seed=42            # 随机种子（相同种子产生相同结果）
)
```

## 🐛 常见问题

### Q1: 安装依赖时出错？

**Windows 用户**：如果安装 `geopandas` 失败，可能需要先安装 GDAL：
```bash
# 方法1：使用 conda（推荐）
conda install geopandas

# 方法2：使用预编译的 wheel 文件
pip install geopandas -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 运行时提示缺少模块？

确保所有依赖都已安装：
```bash
pip install mesa mesa-geo geopandas shapely matplotlib numpy
```

### Q3: 图表不显示？

如果 `plt.show()` 不工作，可以注释掉这行，图表会保存在 `simulation_result.png` 文件中。

### Q4: 想要无 GUI 运行？

编辑 `run.py`，将第 170 行的 `plt.show()` 改为：
```python
# plt.show()  # 注释掉这行
```

## 📊 输出说明

运行成功后，你会看到：

1. **控制台输出**：
   - 模拟进度
   - 门店曝光排名
   - 区域商业潜力分析

2. **图片文件** (`simulation_result.png`)：
   - 左图：空间分布（顾客、门店、测量点）
   - 右图：统计信息

## 🎯 下一步

- 修改 `agents.py` 中的智能体行为逻辑
- 调整 `model.py` 中的空间大小和初始位置
- 添加更多可视化功能

**祝使用愉快！** 🎉

