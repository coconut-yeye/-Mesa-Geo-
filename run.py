"""
运行脚本：执行模拟并可视化结果
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from model import BusinessModel
import warnings

# 配置 matplotlib 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 忽略 CRS 转换警告
warnings.filterwarnings('ignore', category=UserWarning, module='mesa_geo')


def visualize_model(model, step_num=0, save_path=None):
    """可视化模型状态"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左图：空间分布
    ax1 = axes[0]
    ax1.set_xlim(0, model.width)
    ax1.set_ylim(0, model.height)
    ax1.set_aspect('equal')
    ax1.set_title(f'Business Simulation - Step {step_num}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('X Coordinate', fontsize=12)
    ax1.set_ylabel('Y Coordinate', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 导入智能体类型
    from agents import CustomerAgent, StoreAgent, BusinessSurveyAgent
    
    # 获取各类智能体
    
    customers = [a for a in model.space.agents if isinstance(a, CustomerAgent)]
    stores = [a for a in model.space.agents if isinstance(a, StoreAgent)]
    surveys = [a for a in model.space.agents if isinstance(a, BusinessSurveyAgent)]
    
    # 绘制顾客（蓝色点）- 使用原始坐标
    for customer in customers:
        try:
            x = getattr(customer, '_original_x', customer.geometry.x)
            y = getattr(customer, '_original_y', customer.geometry.y)
            # 检查坐标是否在合理范围内
            if 0 <= x <= model.width and 0 <= y <= model.height:
                ax1.plot(x, y, 'bo', markersize=4, alpha=0.6)
        except:
            continue
    
    # 绘制门店（红色圆圈，带影响范围）
    for store in stores:
        try:
            x = getattr(store, '_original_x', store.geometry.x)
            y = getattr(store, '_original_y', store.geometry.y)
            if 0 <= x <= model.width and 0 <= y <= model.height:
                circle = patches.Circle(
                    (x, y),
                    store.radius,
                    color='red',
                    fill=False,
                    linewidth=2,
                    linestyle='--',
                    alpha=0.5
                )
                ax1.add_patch(circle)
                ax1.plot(x, y, 'rs', markersize=10, label='Store' if store == stores[0] else '')
                ax1.text(x, y + store.radius + 0.5, 
                        f'{store.name}\nExposure:{store.exposure}', 
                        ha='center', fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        except:
            continue
    
    # 绘制测量点（绿色圆圈）
    for survey in surveys:
        try:
            x = getattr(survey, '_original_x', survey.geometry.x)
            y = getattr(survey, '_original_y', survey.geometry.y)
            if 0 <= x <= model.width and 0 <= y <= model.height:
                circle = patches.Circle(
                    (x, y),
                    survey.radius,
                    color='green',
                    fill=False,
                    linewidth=2,
                    linestyle=':',
                    alpha=0.5
                )
                ax1.add_patch(circle)
                ax1.plot(x, y, 'g^', markersize=10, label='Survey' if survey == surveys[0] else '')
        except:
            continue
    
    ax1.legend(loc='upper right')
    
    # 右图：统计信息
    ax2 = axes[1]
    ax2.axis('off')
    
    # 门店统计
    store_stats = model.get_store_statistics()
    survey_results = model.get_survey_results()
    
    stats_text = f"Simulation Statistics\n{'='*30}\n\n"
    stats_text += f"Total Steps: {model.step_count}\n"
    stats_text += f"Customers: {model.n_customers}\n"
    stats_text += f"Stores: {model.n_stores}\n"
    stats_text += f"Survey Points: {model.n_surveys}\n\n"
    
    stats_text += "Store Exposure Stats:\n"
    stats_text += "-" * 30 + "\n"
    for name, stats in store_stats.items():
        stats_text += f"{name}:\n"
        stats_text += f"  Position: ({stats['position'][0]:.1f}, {stats['position'][1]:.1f})\n"
        stats_text += f"  Total Exposure: {stats['exposure']}\n\n"
    
    stats_text += "Survey Results:\n"
    stats_text += "-" * 30 + "\n"
    for name, result in survey_results.items():
        if result:
            stats_text += f"{name}:\n"
            stats_text += f"  Customer Flow: {result.get('customer_flow', 0)}\n"
            stats_text += f"  Store Count: {result.get('store_count', 0)}\n"
            stats_text += f"  Customer Density: {result.get('customer_density', 0):.3f}\n"
            stats_text += f"  Business Heat: {result.get('business_heat', 0):.2f}\n\n"
    
    ax2.text(0.1, 0.9, stats_text, transform=ax2.transAxes, 
             fontsize=10, verticalalignment='top', family='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    return fig


def run_simulation(n_steps=50, n_customers=50, n_stores=3, n_surveys=2, seed=42):
    """运行模拟"""
    print("=" * 50)
    print("Business Flow & Potential Prediction Model")
    print("=" * 50)
    
    # 创建模型
    model = BusinessModel(
        n_customers=n_customers,
        n_stores=n_stores,
        n_surveys=n_surveys,
        seed=seed
    )
    
    print(f"\nInitialization Complete:")
    print(f"  - Customers: {n_customers}")
    print(f"  - Stores: {n_stores}")
    print(f"  - Survey Points: {n_surveys}")
    print(f"\nStarting simulation for {n_steps} steps...")
    
    # 运行模拟
    for step in range(n_steps):
        model.step()
        if (step + 1) % 10 == 0:
            print(f"  Completed {step + 1}/{n_steps} steps")
    
    print("\nSimulation Complete!")
    
    # 可视化初始状态
    print("\nGenerating visualization...")
    visualize_model(model, step_num=n_steps, save_path='simulation_result.png')
    
    # 打印最终统计
    print("\n" + "=" * 50)
    print("Final Statistics")
    print("=" * 50)
    
    store_stats = model.get_store_statistics()
    survey_results = model.get_survey_results()
    
    print("\nStore Exposure Ranking:")
    sorted_stores = sorted(store_stats.items(), key=lambda x: x[1]['exposure'], reverse=True)
    for i, (name, stats) in enumerate(sorted_stores, 1):
        print(f"  {i}. {name}: {stats['exposure']} exposures")
    
    print("\nRegional Business Potential Analysis:")
    for name, result in survey_results.items():
        if result:
            print(f"\n  {name}:")
            print(f"    Customer Flow: {result.get('customer_flow', 0)}")
            print(f"    Store Count: {result.get('store_count', 0)}")
            print(f"    Customer Density: {result.get('customer_density', 0):.4f}")
            print(f"    Business Heat: {result.get('business_heat', 0):.2f}")
    
    # 显示图表
    plt.show()
    
    return model


if __name__ == "__main__":
    # 运行模拟
    model = run_simulation(
        n_steps=50,
        n_customers=50,
        n_stores=3,
        n_surveys=2,
        seed=42
    )

