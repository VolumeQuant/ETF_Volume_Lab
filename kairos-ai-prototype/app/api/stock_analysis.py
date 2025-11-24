from fastapi import APIRouter, HTTPException
from app.models.stock_data import StockAnalysis, StockInfo, SupplyDemand, SupplyDemandPeriod, Performance, InvestmentPoint, NewsItem, AnalystOpinion, SectorNews, InvestmentMetrics
from typing import Dict

router = APIRouter()

# 시연용 목 데이터
MOCK_DATA: Dict[str, StockAnalysis] = {
    "005930": StockAnalysis(
        stock_info=StockInfo(
            code="005930",
            name="삼성전자",
            current_price=99200,
            change_rate=2.15,
            change_price=2100,
            volume=18200000,
            ai_summary="[긍정] 최근 삼성전자 관련 긍정 뉴스가 지속적으로 올라오고 있습니다. 11/23 HBM3E 12단 엔비디아 공급 승인으로 AI 메모리 시장 본격 진입, 11/22 파운드리 2나노 공정 개발 순조, 11/21 4분기 영업이익 10조원 돌파 전망(컨센서스 대비 +7.3% 어닝서프라이즈), 11/20 갤럭시 S25 사전 예약 호조 등이 주요 긍정 요인입니다. 수급 측면에서는 외국인과 기관의 동반 매수세가 이어지며 최근 1개월간 외국인 순매수 1.2조원을 기록했습니다. 반도체 섹터도 전반적으로 긍정적인 흐름으로, AI 반도체 중심 성장세 지속, HBM 수요 폭발, 미국 반도체 보조금 집행 본격화 등이 긍정 요인입니다. 증권가 목표가는 평균 125,000원 수준으로 상향 추세이며, KB증권 130,000원(상향), NH투자증권 125,000원(상향), 미래에셋증권 120,000원(중립)으로 제시하고 있습니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/23 HBM3E 엔비디아 공급 승인 <span class="news-importance">★★★★★</span></div>
<div class="news-content">삼성전자가 HBM3E 12단 제품의 엔비디아 품질 테스트를 통과하며 AI 메모리 시장 본격 진입에 성공했습니다. SK하이닉스가 독점하던 HBM 시장에 삼성전자가 진입하면서 2026년 HBM 시장 점유율 30% 목표를 현실화할 수 있게 되었습니다. 애널리스트들은 이번 승인으로 연간 5조원 이상의 추가 매출이 가능할 것으로 전망하고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/22 중국 반도체 규제 강화 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">중국 정부가 반도체 수입 규제를 강화하면서 삼성전자의 중국 시장 매출에 일부 영향이 예상됩니다. 다만 고부가 제품 중심 포트폴리오로 인해 전체적인 영향은 제한적일 것으로 보입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/21 4분기 영업이익 10조원 돌파 전망 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">증권가는 삼성전자 4분기 영업이익을 10.2조원으로 추정하고 있으며, 이는 시장 컨센서스 9.5조원을 크게 상회하는 수치입니다. HBM 비중 확대(전체 메모리 매출의 15% → 20%), DDR5 가격 상승(전분기 대비 8%), NAND 재고 감소 등이 주요 요인입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/20 갤럭시 S25 사전 예약 호조 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">온디바이스 AI 기능을 대폭 강화한 갤럭시 S25 시리즈의 사전 예약이 전작 대비 18% 증가했습니다. 특히 울트라 모델의 예약률이 40%를 넘어서며 평균 판매가(ASP) 상승에 기여할 전망입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/19 파운드리 2나노 공정 양산 준비 완료 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">삼성전자가 차세대 2나노 파운드리 공정의 양산 준비를 완료했습니다. 주요 고객사들과의 선주문 계약이 체결되면서 2026년 파운드리 매출이 전년 대비 25% 이상 성장할 것으로 전망됩니다. 특히 AI 반도체용 고성능 칩 수요가 급증하면서 삼성전자의 파운드리 시장 점유율 확대가 기대됩니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/18 메모리 반도체 가격 상승세 지속 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">DDR5와 HBM 가격이 전월 대비 각각 8%와 12% 상승했습니다. AI 서버 수요 급증과 공급 부족이 지속되면서 메모리 반도체 업황이 개선되고 있습니다. 증권가는 이번 가격 상승세가 최소 2분기 이상 지속될 것으로 전망하고 있으며, 삼성전자의 메모리 사업부 수익성이 크게 개선될 것으로 예상됩니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/17 글로벌 경기 둔화 우려 <span class="news-importance">★★☆☆☆</span></div>
<div class="news-content">글로벌 경기 둔화 우려가 제기되면서 소비자 전자제품 수요 감소 가능성이 있습니다. 다만 삼성전자는 프리미엄 제품 중심 포트폴리오로 인해 영향이 제한적일 것으로 보입니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: HBM3E 엔비디아 공급 승인, 4분기 영업이익 10조원 돌파 전망, 파운드리 2나노 공정 양산 준비 완료 등 주요 긍정 뉴스가 지속됩니다. 다만 중국 반도체 규제 강화와 글로벌 경기 둔화 우려는 부정 요인입니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+250억원",
            institution_net="+180억원",
            individual_net="-430억원",
            summary="외국인과 기관의 동반 매수세가 이어지며 개인 투자자의 차익실현 물량을 흡수하는 모습입니다. 최근 1개월간 외국인 순매수 누적액은 1.2조원으로 AI 반도체 기대감이 반영되고 있습니다.",
            period_data=[
                SupplyDemandPeriod(period="1주일", foreign_net="+1,200억원", institution_net="+850억원", individual_net="-2,050억원"),
                SupplyDemandPeriod(period="1개월", foreign_net="+1.2조원", institution_net="+3,200억원", individual_net="-1.52조원")
            ]
        ),
        performance=Performance(
            revenue="72.5조원",
            operating_profit="10.2조원",
            net_profit="7.8조원",
            summary="2025년 4분기 실적 컨센서스는 메모리 반도체 부문의 지속적인 회복과 HBM3E 엔비디아 공급 승인으로 전년 동기 대비 큰 폭의 성장이 예상됩니다. 특히 HBM과 DDR5 고부가 제품 비중 확대로 영업이익률이 크게 개선될 것으로 전망됩니다.",
            revenue_yoy="+15.2%",
            revenue_qoq="+7.6%",
            operating_profit_yoy="+25.3%",
            operating_profit_qoq="+54.5%",
            operating_profit_vs_consensus="+7.3%",
            earnings_surprise="컨센서스 대비 +7.3%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "HBM3E 엔비디아 공급 승인으로 AI 메모리 시장 진입 본격화",
                "메모리 반도체 업황 회복과 가격 상승세 지속 전망",
                "파운드리 2나노 공정 개발로 기술 경쟁력 강화",
                "갤럭시 AI 탑재로 프리미엄 스마트폰 수요 증가",
                "배당 확대 정책으로 주주환원율 개선 기대"
            ],
            negative=[
                "중국 반도체 규제 강화로 일부 매출 영향 우려",
                "파운드리 사업 수율 개선 지연 시 실적 부담 가능",
                "환율 변동성 확대로 영업이익 변동성 존재",
                "글로벌 경기 둔화 시 IT 수요 감소 리스크"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.23",
                title="삼성전자, HBM3E 12단 엔비디아 공급 승인",
                summary="SK하이닉스에 이어 HBM3E 제품 엔비디아 테스트 통과, AI 메모리 시장 본격 진입",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.22",
                title="2나노 파운드리 공정 개발 순조",
                summary="TSMC 추격 위한 2나노 GAA 공정 기술 개발 가속화, 2026년 양산 목표",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.21",
                title="4분기 영업이익 10조 돌파 전망",
                summary="메모리 가격 상승과 HBM 비중 확대로 4분기 실적 서프라이즈 기대",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.20",
                title="갤럭시 S25 출시 준비, AI 기능 대폭 강화",
                summary="온디바이스 AI 탑재로 프리미엄 모델 판매 증가, 평균 판매가 상승 기여",
                url="#",
                sentiment="positive"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="130,000원",
                opinion="HBM3E 양산 본격화와 파운드리 수율 개선으로 실적 개선 기대. 목표주가 상향",
                firm="KB증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="125,000원",
                opinion="AI 반도체 시장 성장과 메모리 업황 회복세 지속. 투자의견 Buy 유지",
                firm="NH투자증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="120,000원",
                opinion="4분기 실적 개선 전망. HBM 비중 확대로 수익성 개선 예상",
                firm="미래에셋증권",
                trend="neutral"
            )
        ],
        sector_name="반도체",
        sector_news=[
            SectorNews(
                date="2025.11.24",
                title="글로벌 반도체 시장, AI 반도체 중심 성장세 지속",
                summary="2025년 글로벌 반도체 시장 규모는 전년 대비 16% 성장한 6,110억 달러 전망. AI GPU와 HBM이 주도",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.23",
                title="중국 반도체 굴기, 한국 기업에 위기이자 기회",
                summary="중국 SMIC 7나노 공정 양산 개시. 한국 반도체 기업들은 첨단 공정으로 격차 유지 전략",
                sentiment="neutral"
            ),
            SectorNews(
                date="2025.11.22",
                title="HBM 수요 폭발, 2026년까지 공급 부족 지속 전망",
                summary="엔비디아, AMD, 구글 등 빅테크의 AI 인프라 투자 확대로 HBM 수요 급증. 공급 부족 2026년까지 지속",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.21",
                title="미국 반도체 보조금 집행 본격화, 삼성·SK 수혜",
                summary="미국 CHIPS Act 보조금 집행 본격화. 삼성 텍사스, SK 인디애나 공장에 각각 60억, 4억 달러 지원 확정",
                sentiment="positive"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="15.2배",
            pbr="1.28배",
            roe="8.5%",
            dividend_yield="2.31%",
            market_cap="597조원",
            shares_outstanding="59.7억주"
        )
    ),
    "000660": StockAnalysis(
        stock_info=StockInfo(
            code="000660",
            name="SK하이닉스",
            current_price=538700,
            change_rate=3.42,
            change_price=17800,
            volume=3650000,
            ai_summary="[긍정] 최근 SK하이닉스 관련 긍정 뉴스가 지속적으로 올라오고 있습니다. 11/23 HBM4 개발 순조로 2026년 샘플 출하 계획, 11/22 미국 인디애나 패키징 공장 본격 가동, 11/21 4분기 영업이익 7조 중반 전망(컨센서스 대비 +5.2% 어닝서프라이즈), 11/19 엔비디아 GB200 슈퍼칩에 HBM3E 독점 공급 확정 등이 주요 긍정 요인입니다. 수급 측면에서는 외국인의 강력한 매수세가 지속되며 최근 2주간 8,000억원 이상 순매수를 기록했고, 최근 1개월간 외국인 순매수 누적액은 2.8조원에 달합니다. 반도체 섹터도 전반적으로 긍정적인 흐름으로, AI 반도체 중심 성장세 지속, HBM 수요 폭발, 미국 반도체 보조금 집행 본격화 등이 긍정 요인입니다. 증권가 목표가는 평균 623,000원 수준으로 상향 추세이며, 삼성증권 650,000원(상향), 한국투자증권 620,000원(상향), 키움증권 600,000원(상향)으로 제시하고 있습니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/23 HBM4 개발 순조, 2026년 샘플 출하 <span class="news-importance">★★★★★</span></div>
<div class="news-content">차세대 HBM4 제품 개발이 계획보다 빠르게 진행되고 있습니다. 2026년 상반기 엔비디아에 샘플 제공 예정이며, 하반기부터 본격 양산 시작 계획입니다. HBM4는 HBM3E 대비 대역폭 50% 향상, 전력 효율 30% 개선으로 AI GPU 성능 혁신을 이끌 전망입니다. 삼성전자와의 기술 격차를 최소 2년 이상 유지할 수 있을 것으로 보입니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/22 삼성전자 HBM 진입으로 경쟁 심화 우려 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">삼성전자가 HBM3E 엔비디아 공급 승인을 받으면서 SK하이닉스의 독점적 지위에 변화가 예상됩니다. 다만 기술력과 생산 능력 면에서 여전히 우위를 유지하고 있어 단기적인 영향은 제한적일 것으로 보입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/21 4분기 영업이익 7조 중반 전망 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">증권가는 SK하이닉스 4분기 영업이익을 7.4조원으로 추정하고 있습니다. HBM3E 출하량이 전분기 대비 40% 증가하고, DDR5 가격도 10% 이상 상승하면서 영업이익률 40%를 지속할 것으로 예상됩니다. 특히 HBM 매출 비중이 전체 매출의 30%를 넘어서며 수익성 개선을 주도하고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/19 엔비디아 GB200용 HBM3E 12단 독점 공급 <span class="news-importance">★★★★★</span></div>
<div class="news-content">엔비디아의 차세대 AI 슈퍼칩 GB200에 HBM3E 12단 제품을 독점 공급하는 계약을 체결했습니다. GB200 한 대당 HBM 탑재량이 H100 대비 3배 증가하면서, 2026년 HBM 매출이 20조원을 넘어설 것으로 전망됩니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: HBM4 개발 순조와 엔비디아 GB200용 HBM3E 독점 공급, 4분기 영업이익 7조 중반 전망 등 긍정 뉴스가 이어집니다. 다만 삼성전자의 HBM 시장 진입으로 경쟁 심화 우려가 있습니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+520억원",
            institution_net="+310억원",
            individual_net="-830억원",
            summary="외국인의 강력한 매수세가 지속되며 최근 2주간 8,000억원 이상 순매수를 기록했습니다. AI 반도체 업사이클에 대한 기대감으로 기관도 동반 매수 중입니다.",
            period_data=[
                SupplyDemandPeriod(period="1주일", foreign_net="+8,000억원", institution_net="+2,100억원", individual_net="-10,100억원"),
                SupplyDemandPeriod(period="1개월", foreign_net="+2.8조원", institution_net="+5,200억원", individual_net="-3.32조원")
            ]
        ),
        performance=Performance(
            revenue="20.5조원",
            operating_profit="8.8조원",
            net_profit="7.2조원",
            summary="2025년 4분기 실적 컨센서스는 HBM4 개발 순조와 엔비디아 GB200용 HBM3E 12단 독점 공급으로 전년 동기 대비 폭발적인 성장이 예상됩니다. HBM 매출 비중이 35%를 넘어서며 영업이익률 43%를 기록할 것으로 전망됩니다.",
            revenue_yoy="+65.2%",
            revenue_qoq="+16.5%",
            operating_profit_yoy="+220.5%",
            operating_profit_qoq="+25.7%",
            operating_profit_vs_consensus="+8.5%",
            earnings_surprise="컨센서스 대비 +8.5%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "HBM 시장 점유율 50% 이상 유지하며 독점적 지위 확보",
                "엔비디아 H200, GB200 등 차세대 AI GPU용 HBM 독점 공급",
                "2025년 HBM 매출 20조원 이상 전망, 전년 대비 2배 성장",
                "HBM4 개발 선도하며 기술 격차 확대",
                "미국 패키징 공장 가동으로 공급망 안정성 강화"
            ],
            negative=[
                "HBM 가격 인상 여력 제한적, 수익성 정점 논란",
                "삼성전자의 HBM 시장 진입으로 경쟁 심화 우려",
                "AI 투자 사이클 둔화 시 재고 증가 리스크",
                "높은 밸류에이션 부담, 주가 변동성 확대 가능"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.23",
                title="HBM4 개발 순조, 2026년 샘플 출하 계획",
                summary="차세대 HBM4 제품 개발 가속화, 엔비디아 차세대 GPU용 독점 공급 예상",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.22",
                title="미국 패키징 공장 본격 가동",
                summary="인디애나주 첨단 패키징 공장 가동 시작, 미국 AI 공급망 핵심 파트너로 부상",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.21",
                title="4분기 영업이익 7조 중반 예상",
                summary="HBM 출하 확대와 DDR5 가격 상승으로 실적 모멘텀 지속",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.19",
                title="엔비디아 GB200 슈퍼칩에 HBM3E 공급 확정",
                summary="엔비디아 차세대 AI 슈퍼칩용 HBM3E 12단 독점 공급 계약 체결",
                url="#",
                sentiment="positive"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="650,000원",
                opinion="HBM 시장 독점적 지위와 AI 반도체 수퍼사이클 수혜. 목표가 상향 조정",
                firm="삼성증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="620,000원",
                opinion="HBM4 개발 순조, 2026년 매출 성장 가속화 전망. 투자의견 매수",
                firm="한국투자증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="600,000원",
                opinion="AI GPU 수요 증가로 HBM 출하 확대 지속. 실적 모멘텀 강력",
                firm="키움증권",
                trend="up"
            )
        ],
        sector_name="반도체",
        sector_news=[
            SectorNews(
                date="2025.11.24",
                title="글로벌 반도체 시장, AI 반도체 중심 성장세 지속",
                summary="2025년 글로벌 반도체 시장 규모는 전년 대비 16% 성장한 6,110억 달러 전망. AI GPU와 HBM이 주도",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.23",
                title="중국 반도체 굴기, 한국 기업에 위기이자 기회",
                summary="중국 SMIC 7나노 공정 양산 개시. 한국 반도체 기업들은 첨단 공정으로 격차 유지 전략",
                sentiment="neutral"
            ),
            SectorNews(
                date="2025.11.22",
                title="HBM 수요 폭발, 2026년까지 공급 부족 지속 전망",
                summary="엔비디아, AMD, 구글 등 빅테크의 AI 인프라 투자 확대로 HBM 수요 급증. 공급 부족 2026년까지 지속",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.21",
                title="미국 반도체 보조금 집행 본격화, 삼성·SK 수혜",
                summary="미국 CHIPS Act 보조금 집행 본격화. 삼성 텍사스, SK 인디애나 공장에 각각 60억, 4억 달러 지원 확정",
                sentiment="positive"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="9.8배",
            pbr="1.85배",
            roe="19.2%",
            dividend_yield="1.68%",
            market_cap="392조원",
            shares_outstanding="7.3억주"
        )
    ),
    "006800": StockAnalysis(
        stock_info=StockInfo(
            code="006800",
            name="미래에셋증권",
            current_price=21900,
            change_rate=2.81,
            change_price=600,
            volume=4200000,
            ai_summary="[긍정] 최근 미래에셋증권 관련 긍정 뉴스가 지속적으로 올라오고 있습니다. 11/23 AI 투자정보 플랫폼 '엠파워' 출시로 디지털 경쟁력 강화, 11/22 해외주식 수수료 0.07%로 업계 최저 인하, 11/20 웰스케어 자산관리 고객 1.5만명 돌파, 11/18 3분기 순이익 1.4조원으로 컨센서스 대비 +8% 어닝서프라이즈 등이 주요 긍정 요인입니다. 수급 측면에서는 외국인의 꾸준한 매수세가 이어지며 최근 1개월간 외국인 순매수 누적액은 520억원으로 증권주 중 가장 선호도가 높습니다. 증권 섹터는 혼재된 흐름으로, AI 투자 플랫폼 경쟁 본격화와 IB 부문 실적 호조는 긍정이나, 해외주식 수수료 인하 경쟁 심화는 부정 요인입니다. 증권가 목표가는 평균 24,167원 수준으로 상향 추세이며, 하나증권 25,000원(상향), 신한투자증권 24,000원(상향), 대신증권 23,500원(중립)으로 제시하고 있습니다."
        ),
        news_summary="""<div class="news-item positive">
<div class="news-header">📈 11/23 AI 투자정보 플랫폼 '엠파워' 출시 <span class="news-importance">★★★★★</span></div>
<div class="news-content">생성형 AI 기반 투자 정보 분석 서비스 '엠파워(M-Power)'를 출시했습니다. 실시간 뉴스 분석, 종목 리포트 요약, AI 포트폴리오 추천 등 종합 서비스를 제공하며, 업계 최초로 GPT-4 기반 투자 상담 기능을 도입했습니다. MZ세대 고객 유치를 위한 핵심 전략으로, 출시 3일 만에 가입자 5만명을 돌파했습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/22 해외주식 수수료 0.07%로 업계 최저 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">미국 주식 거래 수수료를 기존 0.12%에서 0.07%로 대폭 인하했습니다. 이는 업계 최저 수준이며, 해외주식 거래량을 20% 이상 끌어올릴 것으로 기대됩니다. 최근 3개월간 해외주식 거래 고객이 15만명 증가하면서 브로커리지 수익이 크게 개선되고 있습니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/20 웰스케어 자산관리 고객 1.5만명 돌파 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">고액 자산가 대상 프리미엄 자산관리 서비스인 '웰스케어'의 고객이 1.5만명을 넘어섰습니다. 평균 예탁자산이 50억원으로, 총 관리자산이 75조원에 달합니다. 고수익 고객 확보로 수익성이 크게 개선되고 있으며, 2026년 목표는 고객 3만명, 관리자산 150조원입니다.</div>
</div>

<div class="news-item positive">
<div class="news-header">📈 11/18 3분기 순이익 1.4조원, 컨센서스 8% 초과 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">3분기 순이익이 1.4조원을 기록하며 시장 예상을 크게 웃돌았습니다. 브로커리지 부문은 해외주식 거래 급증으로 전년 동기 대비 25% 성장했고, IB 부문도 대형 IPO 수수료 수입으로 호조를 보였습니다. 특히 ROE가 15.2%로 증권업계 최고 수준을 유지하고 있습니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: AI 투자정보 플랫폼 '엠파워' 출시, 해외주식 수수료 0.07%로 업계 최저 인하, 웰스케어 자산관리 고객 1.5만명 돌파, 3분기 순이익 컨센서스 8% 초과 등 전반적으로 긍정 뉴스가 지속됩니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="+85억원",
            institution_net="-42억원",
            individual_net="-43억원",
            summary="외국인의 꾸준한 매수세가 이어지고 있으며, 기관과 개인은 일부 차익실현 중입니다. 최근 1개월간 외국인 순매수 누적액은 520억원으로 증권주 중 가장 선호도가 높습니다.",
            period_data=[
                SupplyDemandPeriod(period="1주일", foreign_net="+520억원", institution_net="-180억원", individual_net="-340억원"),
                SupplyDemandPeriod(period="1개월", foreign_net="+520억원", institution_net="-420억원", individual_net="-100억원")
            ]
        ),
        performance=Performance(
            revenue="5.8조원",
            operating_profit="2.1조원",
            net_profit="1.6조원",
            summary="2025년 4분기 실적 컨센서스는 AI 플랫폼 '엠파워' 출시와 해외주식 거래 급증으로 전년 동기 대비 18% 증가가 예상됩니다. 브로커리지 수수료 수입 증가와 IB 부문 호조가 지속되며 ROE 16%를 기록할 것으로 전망됩니다.",
            revenue_yoy="+18.5%",
            revenue_qoq="+11.5%",
            operating_profit_yoy="+25.3%",
            operating_profit_qoq="+16.7%",
            operating_profit_vs_consensus="+10.2%",
            earnings_surprise="컨센서스 대비 +10.2%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "국내 1위 증권사 지위와 글로벌 네트워크 경쟁력",
                "해외주식 거래 플랫폼 강화로 MZ세대 유입 지속",
                "웰스케어 자산관리 서비스 확대로 고액 자산가 확보",
                "디지털 자산 사업 진출로 신성장 동력 확보",
                "안정적인 배당 정책으로 주주환원율 4% 이상 유지"
            ],
            negative=[
                "증시 거래대금 감소 시 브로커리지 수익 타격",
                "금리 변동성 확대 시 IB 실적 불확실성",
                "경쟁 격화로 수수료 인하 압력 지속",
                "규제 강화 리스크 (가상자산, 공매도 등)"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.23",
                title="미래에셋증권, AI 투자정보 플랫폼 '엠파워' 출시",
                summary="생성형 AI 기반 투자 정보 분석 서비스로 개인투자자 의사결정 지원 강화",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.22",
                title="해외주식 거래 수수료 추가 인하",
                summary="미국 주식 거래 수수료 0.07%로 인하, 경쟁력 강화로 거래량 20% 증가 기대",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.20",
                title="웰스케어 자산관리 고객 1.5만명 돌파",
                summary="고액 자산가 대상 프리미엄 자산관리 서비스 성장세, 평균 예탁자산 50억원",
                url="#",
                sentiment="positive"
            ),
            NewsItem(
                date="2025.11.18",
                title="3분기 순이익 1.4조원, 시장 예상 상회",
                summary="브로커리지와 IB 부문 동반 성장으로 컨센서스 대비 8% 초과 달성",
                url="#",
                sentiment="positive"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="25,000원",
                opinion="해외주식 거래 플랫폼 경쟁력과 웰스케어 사업 성장. 투자의견 Buy",
                firm="하나증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="24,000원",
                opinion="디지털 자산 사업 확대와 MZ세대 고객 유입 지속. 실적 개선 전망",
                firm="신한투자증권",
                trend="up"
            ),
            AnalystOpinion(
                target_price="23,500원",
                opinion="브로커리지 및 IB 부문 안정적 실적. 배당 매력도 높음",
                firm="대신증권",
                trend="neutral"
            )
        ],
        sector_name="증권",
        sector_news=[
            SectorNews(
                date="2025.11.24",
                title="증권업계, AI 투자 플랫폼 경쟁 본격화",
                summary="미래에셋·삼성·NH투자증권 등 주요 증권사들이 AI 기반 투자 정보 서비스 출시 경쟁. 고객 확보 주력",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.23",
                title="해외주식 거래 수수료 인하 경쟁 심화",
                summary="증권업계 해외주식 수수료 인하 경쟁 가속. 미국 주식 평균 수수료 0.1% 이하로 하락",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.22",
                title="증권사 IB 부문 실적 호조, 대형 IPO 대기 증가",
                summary="2025년 하반기 대형 IPO 대기 기업 증가. 증권사 IB 부문 수수료 수입 증가 전망",
                sentiment="positive"
            ),
            SectorNews(
                date="2025.11.20",
                title="자산관리 플랫폼 경쟁, 웰스테크 투자 확대",
                summary="증권사들의 디지털 자산관리 플랫폼 투자 확대. MZ세대 고액 자산가 확보 경쟁",
                sentiment="positive"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="8.3배",
            pbr="0.75배",
            roe="9.1%",
            dividend_yield="4.11%",
            market_cap="14.2조원",
            shares_outstanding="6.5억주"
        )
    ),
    "373220": StockAnalysis(
        stock_info=StockInfo(
            code="373220",
            name="LG에너지솔루션",
            current_price=385000,
            change_rate=-3.52,
            change_price=-14000,
            volume=1200000,
            ai_summary="[부정] 최근 LG에너지솔루션 관련 부정 뉴스가 지속적으로 올라오고 있습니다. 11/23 중국 배터리 기업 가격 경쟁 심화로 수익성 압박, 11/22 전기차 수요 둔화로 배터리 주문 감소, 11/21 3분기 영업이익 컨센서스 대비 -12% 미달, 11/20 미국 IRA 세부 규정 변경으로 보조금 혜택 축소 등이 주요 부정 요인입니다. 수급 측면에서는 외국인과 기관의 매도세가 지속되며 최근 1개월간 외국인 순매도 8,500억원을 기록했습니다. 배터리 섹터도 전반적으로 부정적인 흐름으로, 중국 배터리 기업 가격 경쟁 심화, 전기차 수요 둔화, 원자재 가격 상승 등이 부정 요인입니다. 증권가 목표가는 평균 420,000원 수준으로 하향 추세이며, 하나증권 450,000원(하향), 신한투자증권 430,000원(하향), 대신증권 400,000원(중립)으로 제시하고 있습니다."
        ),
        news_summary="""<div class="news-item negative">
<div class="news-header">📉 11/23 중국 배터리 기업 가격 경쟁 심화 <span class="news-importance">★★★★★</span></div>
<div class="news-content">CATL, BYD 등 중국 배터리 기업들이 글로벌 시장에서 공격적인 가격 인하를 단행하면서 LG에너지솔루션의 수익성에 압박이 가해지고 있습니다. 중국 기업들의 배터리 단가는 LG에너지솔루션 대비 15-20% 낮은 수준으로, 고객사들의 가격 재협상 요구가 증가하고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/22 전기차 수요 둔화로 배터리 주문 감소 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">글로벌 전기차 시장 성장세가 둔화되면서 주요 고객사들의 배터리 주문이 예상보다 감소하고 있습니다. 특히 유럽 시장의 전기차 보조금 축소와 중국 시장의 경기 둔화가 주요 원인으로 지적되고 있습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/21 3분기 영업이익 컨센서스 대비 -12% 미달 <span class="news-importance">★★★★☆</span></div>
<div class="news-content">3분기 영업이익이 2,850억원을 기록하며 시장 컨센서스 3,240억원을 크게 하회했습니다. 배터리 단가 하락과 원자재 가격 상승이 동시에 발생하면서 수익성이 악화되었습니다. 영업이익률은 전년 동기 대비 2.3%p 하락한 3.2%를 기록했습니다.</div>
</div>

<div class="news-item negative">
<div class="news-header">📉 11/20 미국 IRA 세부 규정 변경으로 보조금 혜택 축소 <span class="news-importance">★★★☆☆</span></div>
<div class="news-content">미국 인플레이션 감소법(IRA)의 세부 규정이 변경되면서 한국 배터리 기업들의 보조금 혜택이 예상보다 축소될 가능성이 높아졌습니다. 특히 중국산 원자재 사용 비율 제한이 강화되면서 공급망 재구성 비용이 증가할 전망입니다.</div>
</div>

<div class="ai-conclusion">💡 AI 분석 결론: 중국 배터리 기업 가격 경쟁 심화, 전기차 수요 둔화로 배터리 주문 감소, 3분기 영업이익 컨센서스 대비 -12% 미달, 미국 IRA 규정 변경으로 보조금 혜택 축소 등 부정 뉴스가 지속됩니다.</div>""",
        supply_demand=SupplyDemand(
            foreign_net="-320억원",
            institution_net="-180억원",
            individual_net="+500억원",
            summary="외국인과 기관의 매도세가 지속되며 개인 투자자들이 하락세를 매수하고 있습니다. 최근 1개월간 외국인 순매도 누적액은 8,500억원으로 배터리 업황 악화 우려가 반영되고 있습니다.",
            period_data=[
                SupplyDemandPeriod(period="1주일", foreign_net="-1,200억원", institution_net="-650억원", individual_net="+1,850억원"),
                SupplyDemandPeriod(period="1개월", foreign_net="-8,500억원", institution_net="-2,300억원", individual_net="+10,800억원")
            ]
        ),
        performance=Performance(
            revenue="7.8조원",
            operating_profit="2,200억원",
            net_profit="1,500억원",
            summary="2025년 4분기 실적 컨센서스는 중국 배터리 기업들의 가격 경쟁 심화와 전기차 수요 둔화로 전년 동기 대비 영업이익 35% 감소가 예상됩니다. 영업이익률은 2.8%로 전년 동기 대비 크게 악화될 것으로 전망되며, 컨센서스 대비 -15% 미달할 가능성이 높습니다.",
            revenue_yoy="+3.2%",
            revenue_qoq="-4.9%",
            operating_profit_yoy="-35.5%",
            operating_profit_qoq="-22.8%",
            operating_profit_vs_consensus="-15.0%",
            earnings_surprise="컨센서스 대비 -15.0%"
        ),
        investment_points=InvestmentPoint(
            positive=[
                "글로벌 전기차 시장 장기 성장 트렌드 지속",
                "고성능 배터리 기술력과 고객 포트폴리오 다각화",
                "미국 현지 생산 확대로 공급망 안정화",
                "양극재 등 핵심 소재 자체 생산 확대"
            ],
            negative=[
                "중국 배터리 기업들의 가격 경쟁 심화",
                "전기차 수요 둔화로 배터리 주문 감소",
                "원자재 가격 상승으로 수익성 압박",
                "미국 IRA 규정 변경으로 보조금 혜택 축소 우려",
                "고객사들의 가격 재협상 압력 증가"
            ]
        ),
        recent_issues=[
            NewsItem(
                date="2025.11.23",
                title="중국 배터리 기업 가격 경쟁 심화",
                summary="CATL, BYD 등 중국 기업들의 공격적 가격 인하로 수익성 압박",
                url="#",
                sentiment="negative"
            ),
            NewsItem(
                date="2025.11.22",
                title="전기차 수요 둔화로 배터리 주문 감소",
                summary="글로벌 전기차 시장 성장세 둔화로 주요 고객사 주문 감소",
                url="#",
                sentiment="negative"
            ),
            NewsItem(
                date="2025.11.21",
                title="3분기 영업이익 컨센서스 대비 -12% 미달",
                summary="배터리 단가 하락과 원자재 가격 상승으로 수익성 악화",
                url="#",
                sentiment="negative"
            ),
            NewsItem(
                date="2025.11.20",
                title="미국 IRA 세부 규정 변경으로 보조금 혜택 축소",
                summary="IRA 규정 변경으로 한국 배터리 기업 보조금 혜택 축소 가능성",
                url="#",
                sentiment="negative"
            )
        ],
        analyst_opinions=[
            AnalystOpinion(
                target_price="450,000원",
                opinion="중국 기업 가격 경쟁과 전기차 수요 둔화로 단기 실적 부담. 목표가 하향",
                firm="하나증권",
                trend="down"
            ),
            AnalystOpinion(
                target_price="430,000원",
                opinion="배터리 업황 악화와 수익성 압박 지속. 투자의견 Hold로 전환",
                firm="신한투자증권",
                trend="down"
            ),
            AnalystOpinion(
                target_price="400,000원",
                opinion="단기 실적 부담 지속 예상. 중장기 회복 가능성은 있으나 신중 접근 필요",
                firm="대신증권",
                trend="neutral"
            )
        ],
        sector_name="배터리",
        sector_news=[
            SectorNews(
                date="2025.11.24",
                title="중국 배터리 기업, 글로벌 시장 점유율 확대",
                summary="CATL, BYD 등 중국 배터리 기업들이 가격 경쟁력을 바탕으로 글로벌 시장 점유율을 빠르게 확대 중",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.23",
                title="전기차 시장 성장세 둔화, 배터리 수요 감소",
                summary="글로벌 전기차 시장 성장률이 전년 대비 둔화되면서 배터리 수요 증가세도 함께 둔화",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.22",
                title="리튬 등 원자재 가격 상승, 배터리 제조사 수익성 압박",
                summary="리튬, 니켈 등 배터리 핵심 원자재 가격이 상승하면서 배터리 제조사들의 수익성에 압박",
                sentiment="negative"
            ),
            SectorNews(
                date="2025.11.21",
                title="미국 IRA 규정 변경, 한국 배터리 기업 영향 불가피",
                summary="미국 IRA 세부 규정 변경으로 한국 배터리 기업들의 보조금 혜택이 축소될 가능성",
                sentiment="negative"
            )
        ],
        investment_metrics=InvestmentMetrics(
            per="45.2배",
            pbr="2.85배",
            roe="6.3%",
            dividend_yield="0.85%",
            market_cap="89조원",
            shares_outstanding="23.1억주"
        )
    )
}

@router.get("/stock/{stock_code}", response_model=StockAnalysis)
async def get_stock_analysis(stock_code: str):
    """
    종목 코드로 AI 시황 분석 데이터 조회
    
    - **stock_code**: 종목 코드 (예: 005930)
    """
    if stock_code not in MOCK_DATA:
        raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
    
    return MOCK_DATA[stock_code]

@router.get("/stocks/list")
async def get_stock_list():
    """시연 가능한 종목 목록 조회"""
    return {
        "stocks": [
            {"code": "005930", "name": "삼성전자"},
            {"code": "000660", "name": "SK하이닉스"},
            {"code": "006800", "name": "미래에셋증권"},
            {"code": "373220", "name": "LG에너지솔루션"}
        ]
    }


