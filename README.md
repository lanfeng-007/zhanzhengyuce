# 美以伊战争建模预测平台

这是一个基于 Word 文档要求实现的全栈 Python 项目，提供完整的前端页面、后端服务、接口以及运行说明。项目将文档中的研究框架落成一个可运行原型，核心围绕三层能力展开：

- 战略层：事件大数据 + 舆情信号的冲突概率预警
- 战役层：目标威胁评估、意图识别与优先级分层
- 决策层：多智能体情景推演与综合处置建议

## 技术栈

- 后端：FastAPI
- 前端：Jinja2 模板 + 原生 JavaScript + CSS
- 测试：pytest

## 项目结构

```text
app/
  main.py                    # FastAPI 入口
  services/
    analysis.py              # 三层预测与综合评估逻辑
    data_factory.py          # 研究型样本数据生成
  static/
    css/styles.css           # 完整页面样式
    js/app.js                # 前端交互逻辑
  templates/
    index.html               # 主页面
tests/
  test_dashboard.py          # 基础接口测试
requirements.txt
README.md
```

## 功能说明

### 1. 首页研究看板

访问首页后可以看到：

- 综合风险指数与预警等级
- 战略层风险概率
- 战役层威胁指数
- 决策层情景一致性
- 月度冲突信号表
- 关键驱动因子面板
- 战役层目标优先级卡片
- 多情景推演结果
- 综合处置建议
- 三方智能体约束画像

### 2. 后端接口

- `GET /`：前端页面
- `GET /api/dashboard`：完整仪表盘数据
- `GET /api/health`：健康检查

## 安装与运行

建议使用项目自带虚拟环境，或者新建一个独立虚拟环境。

### 1. 安装依赖

```powershell
pip install -r requirements.txt
```

### 2. 启动服务

```powershell
python main.py
```

默认访问地址：

```text
http://127.0.0.1:8000
```

## 测试

```powershell
pytest
```

## 实现映射到 Word 文档

本项目没有把文档内容做成静态说明页，而是把其核心研究设计实现成一个可交互原型：

- `DataFactory` 对应文档中的多源数据获取与预处理
- `ConflictForecastService._strategic_layer()` 对应 LSTM/随机森林风格的战略层预警
- `ConflictForecastService._operational_layer()` 对应 DBN、TOPSIS、VIKOR 风格的战役层评估
- `ConflictForecastService._simulation_layer()` 对应多智能体推演与情景预测
- `ConflictForecastService._integrated_assessment()` 对应模型集成与分级预警输出

## 说明

当前实现是研究原型，不直接接入真实的 GDELT、Twitter/X、OSINT 或大模型 API，而是按文档结构构建了可复现实验样本和可运行逻辑。这样做的目的是先把系统架构、接口、前端展示和预测流程完整落地，后续可以继续替换为真实数据源和真实模型。
