from __future__ import annotations

from datetime import date
from math import cos, pi, sin
from typing import Dict, List


class DataFactory:
    """Build deterministic synthetic research data for the prototype."""

    def __init__(self, seed: int = 20260513) -> None:
        self.seed = seed

    def build_timeline(self, months: int = 24) -> List[Dict[str, float | int | str]]:
        timeline: List[Dict[str, float | int | str]] = []
        start_year = 2024
        start_month = 1

        for idx in range(months):
            month = ((start_month - 1 + idx) % 12) + 1
            year = start_year + ((start_month - 1 + idx) // 12)
            phase = idx / max(1, months - 1)
            seasonal = 0.5 + 0.5 * sin((idx / 6.0) * pi)
            pressure = 0.45 + phase * 0.35 + seasonal * 0.12
            rhetoric = min(1.0, pressure + 0.08 * cos(idx / 4.0))
            q1 = int(40 - phase * 8 + seasonal * 4)
            q2 = int(28 - phase * 6 + seasonal * 3)
            q3 = int(22 + phase * 18 + seasonal * 8)
            q4 = int(10 + phase * 20 + seasonal * 10)
            negative_sentiment = min(0.95, 0.32 + phase * 0.34 + seasonal * 0.12)
            military_mobility = min(0.98, 0.3 + phase * 0.42 + seasonal * 0.18)
            proxy_activity = min(0.98, 0.24 + phase * 0.45 + seasonal * 0.14)
            osint_alerts = int(3 + phase * 8 + seasonal * 4)

            timeline.append(
                {
                    "month": f"{year}-{month:02d}",
                    "q1": q1,
                    "q2": q2,
                    "q3": q3,
                    "q4": q4,
                    "goldstein": round(-1.4 - phase * 2.1 - seasonal * 0.8, 2),
                    "avg_tone": round(-2.8 - phase * 3.7 - seasonal * 1.3, 2),
                    "negative_sentiment": round(negative_sentiment, 3),
                    "military_mobility": round(military_mobility, 3),
                    "proxy_activity": round(proxy_activity, 3),
                    "rhetoric": round(rhetoric, 3),
                    "osint_alerts": osint_alerts,
                    "event_intensity": round((q3 * 0.42 + q4 * 0.58) / max(1, q1 + q2 + q3 + q4), 3),
                }
            )

        return timeline

    def build_structural_indicators(self) -> List[Dict[str, float | str]]:
        return [
            {
                "actor": "美国",
                "gdp_trillion": 27.2,
                "military_spending_pct_gdp": 3.4,
                "political_pressure": 0.61,
                "alliance_commitment": 0.88,
                "energy_exposure": 0.38,
            },
            {
                "actor": "以色列",
                "gdp_trillion": 0.53,
                "military_spending_pct_gdp": 5.3,
                "political_pressure": 0.76,
                "alliance_commitment": 0.92,
                "energy_exposure": 0.31,
            },
            {
                "actor": "伊朗",
                "gdp_trillion": 0.41,
                "military_spending_pct_gdp": 2.8,
                "political_pressure": 0.82,
                "alliance_commitment": 0.47,
                "energy_exposure": 0.71,
            },
        ]

    def build_operational_targets(self) -> List[Dict[str, float | str]]:
        return [
            {
                "name": "黎凡特防空走廊",
                "type": "一体化防空节点",
                "mobility": 0.41,
                "weapon_range": 0.72,
                "detection": 0.84,
                "intent": 0.65,
                "altitude": 0.58,
                "speed": 0.34,
                "distance": 0.46,
                "approach_angle": 0.62,
                "battlefield_value": 0.81,
                "strike_cost": 0.69,
            },
            {
                "name": "代理人导弹发射网络",
                "type": "代理人打击集群",
                "mobility": 0.67,
                "weapon_range": 0.64,
                "detection": 0.59,
                "intent": 0.84,
                "altitude": 0.36,
                "speed": 0.77,
                "distance": 0.52,
                "approach_angle": 0.71,
                "battlefield_value": 0.76,
                "strike_cost": 0.44,
            },
            {
                "name": "海湾物流咽喉节点",
                "type": "后勤与海上通道节点",
                "mobility": 0.22,
                "weapon_range": 0.48,
                "detection": 0.66,
                "intent": 0.58,
                "altitude": 0.29,
                "speed": 0.21,
                "distance": 0.81,
                "approach_angle": 0.37,
                "battlefield_value": 0.88,
                "strike_cost": 0.73,
            },
            {
                "name": "战略网络压制单元",
                "type": "网络与电子战单元",
                "mobility": 0.79,
                "weapon_range": 0.57,
                "detection": 0.33,
                "intent": 0.74,
                "altitude": 0.12,
                "speed": 0.82,
                "distance": 0.64,
                "approach_angle": 0.69,
                "battlefield_value": 0.63,
                "strike_cost": 0.28,
            },
        ]

    def build_scenarios(self) -> List[Dict[str, str | float]]:
        return [
            {
                "name": "威慑稳定",
                "probability": 0.18,
                "summary": "军事信号维持高位，但通过幕后协调压制了直接正面冲突。",
            },
            {
                "name": "代理人压力升级",
                "probability": 0.36,
                "summary": "海上与边境方向的代理人袭击增强，主要行为体仍尽量避免直接互击。",
            },
            {
                "name": "有限空袭行动",
                "probability": 0.29,
                "summary": "精确打击指向基础设施和导弹节点，外溢范围有限但地区冲击明显。",
            },
            {
                "name": "区域多线冲突",
                "probability": 0.17,
                "summary": "战略克制失效，冲突在多个方向扩展并形成区域性联动。",
            },
        ]

    def metadata(self) -> Dict[str, str]:
        return {
            "dataset_name": "美以伊冲突研究样本数据集",
            "generated_on": date.today().isoformat(),
            "method": "依据文档研究结构生成的可复现实验样本数据。",
        }
