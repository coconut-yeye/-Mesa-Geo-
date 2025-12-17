"""
测试脚本：检查所有依赖是否正确安装
运行此脚本可以快速验证环境是否配置正确
"""
import sys

def test_imports():
    """测试所有必需的导入"""
    print("=" * 50)
    print("检查依赖包安装状态...")
    print("=" * 50)
    
    required_packages = {
        "mesa": "Mesa 智能体建模框架",
        "mesa_geo": "Mesa-Geo 地理空间扩展",
        "geopandas": "GeoPandas 地理数据处理",
        "shapely": "Shapely 几何操作",
        "matplotlib": "Matplotlib 可视化",
        "numpy": "NumPy 数值计算"
    }
    
    failed_imports = []
    
    for package, description in required_packages.items():
        try:
            if package == "mesa_geo":
                __import__("mesa_geo")
            else:
                __import__(package)
            print(f"[OK] {package:15s} - {description}")
        except ImportError as e:
            print(f"[X] {package:15s} - 未安装或导入失败")
            print(f"   错误信息: {e}")
            failed_imports.append(package)
    
    print("\n" + "=" * 50)
    
    if failed_imports:
        print("[X] 以下包未正确安装:")
        for pkg in failed_imports:
            print(f"   - {pkg}")
        print("\n请运行以下命令安装缺失的包:")
        print(f"   pip install {' '.join(failed_imports)}")
        print("\n或安装所有依赖:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("[OK] 所有依赖包已正确安装！")
        print("\n可以运行主程序了:")
        print("   python run.py")
        return True

def test_basic_functionality():
    """测试基本功能"""
    print("\n" + "=" * 50)
    print("测试基本功能...")
    print("=" * 50)
    
    try:
        # 测试导入项目模块
        from agents import CustomerAgent, StoreAgent, BusinessSurveyAgent
        print("[OK] 成功导入智能体类")
        
        from model import BusinessModel
        print("[OK] 成功导入模型类")
        
        # 测试创建简单模型（不运行完整模拟）
        from shapely.geometry import Point
        from mesa import Model
        from mesa_geo import GeoSpace
        
        print("[OK] 成功导入所有核心模块")
        
        # 尝试创建一个最小模型测试
        print("\n测试创建模型...")
        model = BusinessModel(n_customers=5, n_stores=1, n_surveys=1, width=10, height=10)
        print(f"[OK] 成功创建模型（{len(model.space.agents)} 个智能体）")
        
        # 运行一步测试
        model.step()
        print("[OK] 成功执行一步模拟")
        
        print("\n" + "=" * 50)
        print("[OK] 所有基本功能测试通过！")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n[X] 功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n开始测试安装环境...\n")
    
    # 测试导入
    imports_ok = test_imports()
    
    if imports_ok:
        # 测试基本功能
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n[成功] 环境配置完全正确！可以开始使用项目了！\n")
            sys.exit(0)
        else:
            print("\n[警告] 基本功能测试失败，请检查错误信息\n")
            sys.exit(1)
    else:
        print("\n[警告] 依赖包未完全安装，请先安装缺失的包\n")
        sys.exit(1)

