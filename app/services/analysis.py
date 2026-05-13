from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Dict, List

from .data_factory import DataFactory


@dataclass
class RiskSlice:
    label: str
    score: float
    description: str


class ConflictForecastService:
    """Research-oriented analytics service aligned to the Word document."""

    def __init__(self, data_factory: DataFactory | None = None) -> None:
        self.data_factory = data_factory or DataFactory()
        self.timeline = self.data_factory.build_timeline()
        self.structural_indicators = self.data_factory.build_structural_indicators()
        self.operational_targets = self.data_factory.build_operational_targets()
        self.scenarios = self.data_factory.build_scenarios()

    def dashboard(self) -> Dict[str, object]:
        strategic = self._strategic_layer()
        operational = self._operational_layer()
        simulation = self._simulation_layer()
        integrated = self._integrated_assessment(
            strategic["risk_probability"],
            operational["threat_index"],
            simulation["consistency_score"],
        )

        return {
            "metadata": self.data_factory.metadata(),
            "timeline": self.timeline,
            "structural_indicators": self.structural_indicators,
            "strategic": strategic,
            "operational": operational,
            "simulation": simulation,
            "integrated": integrated,
        }

    def _strategic_layer(self) -> Dict[str, object]:
        recent = self.timeline[-6:]
        q4_avg = mean(item["q4"] for item in recent)
        sentiment_avg = mean(item["negative_sentiment"] for item in recent)
        proxy_avg = mean(item["proxy_activity"] for item in recent)
        rhetoric_avg = mean(item["rhetoric"] for item in recent)

        lstm_like_score = min(0.99, 0.24 + q4_avg / 100.0 + sentiment_avg * 0.28)
        forest_like_score = min(0.99, 0.18 + proxy_avg * 0.35 + rhetoric_avg * 0.31)
        risk_probability = round((lstm_like_score * 0.56 + forest_like_score * 0.44), 3)

        factors = [
            RiskSlice("代理人袭击频次", round(proxy_avg, 3), "分布式代理人行动会持续推高升级压力。"),
            RiskSlice("负面情绪占比", round(sentiment_avg, 3), "网络舆情可作为事件预警的重要校验项。"),
            RiskSlice("敌对言论强度", round(rhetoric_avg, 3), "领导人对抗性言论会放大短期波动。"),
            RiskSlice("实质冲突活动", round(q4_avg / 40.0, 3), "持续的动能事件意味着更高的风险基线。"),
        ]
        factors.sort(key=lambda item: item.score, reverse=True)

        risk_level = self._risk_level(risk_probability)
        return {
            "risk_probability": risk_probability,
            "risk_level": risk_level,
            "lstm_signal": round(lstm_like_score, 3),
            "forest_signal": round(forest_like_score, 3),
            "top_factors": [factor.__dict__ for factor in factors],
            "summary": self._strategic_summary(risk_probability, risk_level, factors),
        }

    def _operational_layer(self) -> Dict[str, object]:
        ranked_targets: List[Dict[str, object]] = []
        for target in self.operational_targets:
            intent_confidence = round(
                0.18
                + target["intent"] * 0.26
                + target["mobility"] * 0.17
                + target["speed"] * 0.11
                + target["approach_angle"] * 0.08,
                3,
            )
            threat = round(
                0.14
                + target["weapon_range"] * 0.17
                + target["detection"] * 0.12
                + target["intent"] * 0.18
                + (1 - target["distance"]) * 0.14
                + target["speed"] * 0.09
                + target["battlefield_value"] * 0.16,
                3,
            )
            value_score = round(
                target["battlefield_value"] * 0.34
                + threat * 0.38
                + (1 - target["strike_cost"]) * 0.28,
                3,
            )
            ranked_targets.append(
                {
                    **target,
                    "intent_confidence": min(intent_confidence, 0.99),
                    "threat": min(threat, 0.99),
                    "value_score": min(value_score, 0.99),
                    "priority_tier": self._tier(value_score),
                }
            )

        ranked_targets.sort(key=lambda item: (item["priority_tier"], -item["value_score"]))
        threat_index = round(mean(item["threat"] for item in ranked_targets), 3)
        return {
            "threat_index": threat_index,
            "risk_level": self._risk_level(threat_index),
            "targets": ranked_targets,
            "summary": self._operational_summary(threat_index, ranked_targets),
        }

    def _simulation_layer(self) -> Dict[str, object]:
        scenarios = sorted(self.scenarios, key=lambda item: item["probability"], reverse=True)
        consistency_score = round(sum(s["probability"] * (idx + 1) for idx, s in enumerate(scenarios)) / 6.5, 3)
        agent_briefs = [
            {
                "agent": "美国",
                "bias": "优先维持联盟信誉与地区威慑稳定",
                "constraint": "避免陷入长期地面军事介入",
            },
            {
                "agent": "以色列",
                "bias": "倾向对高置信度威胁实施先发制人打击",
                "constraint": "控制本土关键基础设施持续受损",
            },
            {
                "agent": "伊朗",
                "bias": "通过可控报复维持政权安全与地区影响力",
                "constraint": "保护战略设施免遭决定性摧毁",
            },
        ]

        return {
            "consistency_score": consistency_score,
            "dominant_scenario": scenarios[0],
            "scenarios": scenarios,
            "agent_briefs": agent_briefs,
            "summary": self._simulation_summary(consistency_score, scenarios),
        }

    def _integrated_assessment(self, strategic: float, operational: float, simulation: float) -> Dict[str, object]:
        overall = round(strategic * 0.42 + operational * 0.33 + simulation * 0.25, 3)
        slices = [
            RiskSlice("Strategic warning", strategic, "Event trend and structural signal aggregation."),
            RiskSlice("Operational threat", operational, "Intent recognition and weighted target threat."),
            RiskSlice("Decision simulation", simulation, "Scenario convergence across multi-agent policy play."),
        ]
        return {
            "overall_score": overall,
            "overall_level": self._risk_level(overall),
            "slices": [item.__dict__ for item in slices],
            "recommendations": self._recommendations(overall),
        }

    @staticmethod
    def _risk_level(score: float) -> str:
        if score >= 0.78:
            return "Red"
        if score >= 0.62:
            return "Orange"
        if score >= 0.45:
            return "Yellow"
        return "Blue"

    @staticmethod
    def _tier(value_score: float) -> str:
        if value_score >= 0.72:
            return "Tier 1"
        if value_score >= 0.58:
            return "Tier 2"
        return "Tier 3"

    @staticmethod
    def _strategic_summary(risk_probability: float, risk_level: str, factors: List[RiskSlice]) -> str:
        factor_names = ", ".join(f.label for f in factors[:3])
        return (
            f"战略层冲突概率为 {risk_probability:.1%}，当前预警等级为 {risk_level}。"
            f"主要驱动因素包括：{factor_names}。"
        )

    @staticmethod
    def _operational_summary(threat_index: float, targets: List[Dict[str, object]]) -> str:
        leading = targets[0]["name"]
        return (
            f"战役层威胁指数为 {threat_index:.1%}。"
            f"在加权 DBN 风格评估中，{leading} 当前具有最高优先级。"
        )

    @staticmethod
    def _simulation_summary(consistency_score: float, scenarios: List[Dict[str, object]]) -> str:
        dominant = scenarios[0]["name"]
        return (
            f"决策层情景一致性得分为 {consistency_score:.1%}。"
            f"当前最可能的演化路径为 {dominant}，说明局势更可能沿有限但持续加压的方向升级。"
        )

    @staticmethod
    def _recommendations(overall: float) -> List[str]:
        if overall >= 0.78:
            return [
                "进入红色预警监测状态，将态势更新频率提升到日内级别。",
                "同步准备外交降温方案与关键基础设施连续性预案。",
                "优先处置代理人网络扩散风险与海上通道安全风险。",
            ]
        if overall >= 0.62:
            return [
                "提升为强化监测状态，执行按日跨源校验。",
                "重点跟踪敌对言论强度变化与代理人打击聚集趋势。",
                "预置物流中断与区域撤离支持预案。",
            ]
        if overall >= 0.45:
            return [
                "保持按周观察清单刷新与异常复核。",
                "聚焦高关注事件后的情绪突增与扩散链路。",
                "复核能源与交通关键依赖暴露面。",
            ]
        return [
            "维持基线监测与按月结构性复盘。",
            "沉淀稳定期样本，用于后续阈值校准。",
        ]
