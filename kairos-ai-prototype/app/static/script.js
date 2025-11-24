// API 엔드포인트
const API_BASE = '/api';

// DOM 요소
const stockSelector = document.getElementById('stockSelector');
const loadingScreen = document.getElementById('loadingScreen');
const emptyState = document.getElementById('emptyState');
const mainContent = document.getElementById('mainContent');

// 종목 선택 이벤트
stockSelector.addEventListener('change', async (e) => {
    const stockCode = e.target.value;
    
    if (!stockCode) {
        showEmptyState();
        return;
    }
    
    await loadStockAnalysis(stockCode);
});

// 빈 상태 표시
function showEmptyState() {
    emptyState.style.display = 'flex';
    mainContent.style.display = 'none';
}

// 로딩 표시
function showLoading() {
    loadingScreen.classList.add('active');
    emptyState.style.display = 'none';
    mainContent.style.display = 'none';
}

// 로딩 숨김
function hideLoading() {
    loadingScreen.classList.remove('active');
}

// 종목 분석 데이터 로드
async function loadStockAnalysis(stockCode) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/stock/${stockCode}`);
        
        if (!response.ok) {
            throw new Error('데이터를 불러올 수 없습니다.');
        }
        
        const data = await response.json();
        
        // 약간의 딜레이로 AI 분석 느낌 연출
        await new Promise(resolve => setTimeout(resolve, 800));
        
        renderStockAnalysis(data);
        
        hideLoading();
        mainContent.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading stock analysis:', error);
        alert('데이터를 불러오는 중 오류가 발생했습니다.');
        hideLoading();
        showEmptyState();
    }
}

// 데이터 렌더링
function renderStockAnalysis(data) {
    const { stock_info, news_summary, supply_demand, performance, investment_points, recent_issues, analyst_opinions, sector_name, sector_news, investment_metrics } = data;
    
    // 종목 헤더
    document.getElementById('stockName').textContent = stock_info.name;
    document.getElementById('stockCode').textContent = stock_info.code;
    document.getElementById('currentPrice').textContent = formatNumber(stock_info.current_price);
    
    // 등락 정보
    const changePrice = document.querySelector('.change-price');
    const changeRate = document.querySelector('.change-rate');
    const priceChange = document.querySelector('.price-change');
    const currentPrice = document.getElementById('currentPrice');
    
    const isUp = stock_info.change_rate > 0;
    const sign = isUp ? '+' : '';
    
    changePrice.textContent = `${sign}${formatNumber(stock_info.change_price)}`;
    changeRate.textContent = `(${sign}${stock_info.change_rate}%)`;
    
    // 색상 적용
    if (isUp) {
        priceChange.className = 'price-change price-up';
        currentPrice.className = 'current-price price-up';
    } else {
        priceChange.className = 'price-change price-down';
        currentPrice.className = 'current-price price-down';
    }
    
    // AI 시황 분석 (상단)
    const aiSummaryText = stock_info.ai_summary;
    const topSentimentMatch = aiSummaryText.match(/\[(긍정|부정|중립)\]/);
    const topSentiment = topSentimentMatch ? topSentimentMatch[1] : '중립';
    document.getElementById('aiSummary').textContent = aiSummaryText.replace(/\[(긍정|부정|중립)\]\s*/, '');
    renderSentimentBadge('topAiSummarySentiment', topSentiment);
    
    // AI 시황 요약 (메인) - 각 뉴스에 배지 추가
    let newsSummaryHTML = news_summary;
    
    // AI 분석 결론을 추출하고 맨 위로 이동
    const aiConclusionMatch = newsSummaryHTML.match(/<div class="ai-conclusion">(.*?)<\/div>/s);
    let aiConclusionHTML = '';
    if (aiConclusionMatch) {
        // 원본에서 제거
        newsSummaryHTML = newsSummaryHTML.replace(/<div class="ai-conclusion">.*?<\/div>/s, '');
        // "AI 분석 결론:"을 "두 줄 요약:"으로 변경
        aiConclusionHTML = aiConclusionMatch[1].replace(/💡\s*AI 분석 결론:\s*/, '💡 두 줄 요약: ');
    }
    
    // 전체 감성 분석
    const overallSentimentMatch = newsSummaryHTML.match(/class="news-item\s+(positive|negative|neutral)"/);
    const overallSentiment = overallSentimentMatch ? (overallSentimentMatch[1] === 'positive' ? '긍정' : overallSentimentMatch[1] === 'negative' ? '부정' : '중립') : '중립';
    renderSentimentBadge('aiMainSentiment', overallSentiment);
    
    // 각 news-item의 헤더에 배지를 추가 (같은 줄에 표시)
    // news-item 블록 전체를 처리하여 sentiment를 정확히 매칭
    newsSummaryHTML = newsSummaryHTML.replace(
        /<div class="news-item (positive|negative|neutral)">\s*<div class="news-header">/g,
        (match, sentiment) => {
            const sentimentIcon = sentiment === 'positive' ? '▲' : sentiment === 'negative' ? '▼' : '●';
            const sentimentLabel = sentiment === 'positive' ? '긍정' : sentiment === 'negative' ? '부정' : '중립';
            return `<div class="news-item ${sentiment}">
                    <div class="news-header">
                    <span class="news-sentiment-badge-inline sentiment-${sentiment}">
                        <span class="sentiment-icon">${sentimentIcon}</span>${sentimentLabel}
                    </span>`;
        }
    );
    
    // AI 분석 결론을 맨 위에 추가
    if (aiConclusionHTML) {
        newsSummaryHTML = `<div class="ai-conclusion">${aiConclusionHTML}</div>\n\n${newsSummaryHTML}`;
    }
    
    document.getElementById('newsSummary').innerHTML = newsSummaryHTML;
    
    // 수급 정보
    renderSupplyDemand(supply_demand);
    
    // 실적 정보
    renderPerformance(performance);
    
    // 투자 포인트
    const positiveList = document.getElementById('positivePoints');
    const negativeList = document.getElementById('negativePoints');
    
    positiveList.innerHTML = '';
    negativeList.innerHTML = '';
    
    investment_points.positive.forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        positiveList.appendChild(li);
    });
    
    investment_points.negative.forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        negativeList.appendChild(li);
    });

    
    // 섹터 동향
    document.getElementById('sectorName').textContent = sector_name;
    const sectorNewsList = document.getElementById('sectorNewsList');
    sectorNewsList.innerHTML = '';
    
    sector_news.forEach(news => {
        const item = document.createElement('div');
        const sentiment = news.sentiment || 'neutral';
        item.className = `sector-news-item sentiment-${sentiment}`;
        const sentimentIcon = sentiment === 'positive' ? '▲' : sentiment === 'negative' ? '▼' : '●';
        const sentimentLabel = sentiment === 'positive' ? '긍정' : sentiment === 'negative' ? '부정' : '중립';
        item.innerHTML = `
            <div class="sector-news-header">
                <span class="sector-news-date">${news.date}</span>
                <span class="sentiment-badge sentiment-${sentiment}">
                    <span class="sentiment-icon">${sentimentIcon}</span>
                    ${sentimentLabel}
                </span>
            </div>
            <div class="sector-news-title">${news.title}</div>
            <div class="sector-news-summary">${news.summary}</div>
        `;
        sectorNewsList.appendChild(item);
    });
    
    // 투자 지표 (상단 인라인)
    document.getElementById('perInline').textContent = investment_metrics.per;
    document.getElementById('pbrInline').textContent = investment_metrics.pbr;
    document.getElementById('roeInline').textContent = investment_metrics.roe;
    document.getElementById('dividendYieldInline').textContent = investment_metrics.dividend_yield;
    
    // 애널리스트 의견 (우측에도 표시)
    const analystListRight = document.getElementById('analystListRight');
    analystListRight.innerHTML = '';
    
    analyst_opinions.forEach(analyst => {
        const item = document.createElement('div');
        item.className = 'analyst-item';
        const trendIcon = analyst.trend === 'up' ? '↑' : analyst.trend === 'down' ? '↓' : '→';
        const trendClass = analyst.trend === 'up' ? 'trend-up' : analyst.trend === 'down' ? 'trend-down' : 'trend-neutral';
        item.innerHTML = `
            <div class="analyst-header">
                <span class="analyst-firm">${analyst.firm}</span>
                <span class="analyst-target">
                    ${analyst.target_price}
                    <span class="trend-indicator ${trendClass}">${trendIcon}</span>
                </span>
            </div>
            <div class="analyst-opinion">${analyst.opinion}</div>
        `;
        analystListRight.appendChild(item);
    });
}

// 숫자 포맷팅
function formatNumber(num) {
    return num.toLocaleString('ko-KR');
}

// 수급 정보 렌더링
function renderSupplyDemand(supply_demand) {
    // 기본 데이터 (1일)
    document.getElementById('foreignNet').textContent = supply_demand.foreign_net;
    document.getElementById('institutionNet').textContent = supply_demand.institution_net;
    document.getElementById('individualNet').textContent = supply_demand.individual_net;
    document.getElementById('supplySummary').textContent = supply_demand.summary;
    
    // 색상 적용
    applySupplyColor('foreignNet', supply_demand.foreign_net);
    applySupplyColor('institutionNet', supply_demand.institution_net);
    applySupplyColor('individualNet', supply_demand.individual_net);
    
    // 수급 값에 클래스 추가
    const foreignEl = document.getElementById('foreignNet');
    const instEl = document.getElementById('institutionNet');
    const indEl = document.getElementById('individualNet');
    
    if (supply_demand.foreign_net.startsWith('+')) {
        foreignEl.classList.add('positive');
    } else if (supply_demand.foreign_net.startsWith('-')) {
        foreignEl.classList.add('negative');
    }
    
    if (supply_demand.institution_net.startsWith('+')) {
        instEl.classList.add('positive');
    } else if (supply_demand.institution_net.startsWith('-')) {
        instEl.classList.add('negative');
    }
    
    if (supply_demand.individual_net.startsWith('+')) {
        indEl.classList.add('positive');
    } else if (supply_demand.individual_net.startsWith('-')) {
        indEl.classList.add('negative');
    }
    
    // 탭 이벤트 리스너
    const tabs = document.querySelectorAll('.supply-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const period = tab.dataset.period;
            const periodData = supply_demand.period_data?.find(p => p.period === period);
            
            if (periodData) {
                document.getElementById('foreignNet').textContent = periodData.foreign_net;
                document.getElementById('institutionNet').textContent = periodData.institution_net;
                document.getElementById('individualNet').textContent = periodData.individual_net;
                
                applySupplyColor('foreignNet', periodData.foreign_net);
                applySupplyColor('institutionNet', periodData.institution_net);
                applySupplyColor('individualNet', periodData.individual_net);
            } else if (period === '1일') {
                document.getElementById('foreignNet').textContent = supply_demand.foreign_net;
                document.getElementById('institutionNet').textContent = supply_demand.institution_net;
                document.getElementById('individualNet').textContent = supply_demand.individual_net;
                
                applySupplyColor('foreignNet', supply_demand.foreign_net);
                applySupplyColor('institutionNet', supply_demand.institution_net);
                applySupplyColor('individualNet', supply_demand.individual_net);
            }
        });
    });
}

// 수급 색상 적용
function applySupplyColor(elementId, value) {
    const element = document.getElementById(elementId);
    if (value.startsWith('+')) {
        element.style.color = 'var(--up-color)';
    } else if (value.startsWith('-')) {
        element.style.color = 'var(--down-color)';
    } else {
        element.style.color = 'var(--text-secondary)';
    }
}

// 실적 정보 렌더링
function renderPerformance(performance) {
    // 매출액: 컨센서스 값과 증가율 표시
    const revenueItem = document.getElementById('revenue').closest('.performance-item');
    if (performance.revenue) {
        document.getElementById('revenue').textContent = performance.revenue;
    }
    revenueItem.classList.add('has-comparison');
    if (performance.revenue_yoy) {
        document.getElementById('revenueYoy').textContent = `전년동기: ${performance.revenue_yoy}`;
        applyComparisonColor('revenueYoy', performance.revenue_yoy);
    }
    if (performance.revenue_qoq) {
        document.getElementById('revenueQoq').textContent = `직전분기: ${performance.revenue_qoq}`;
        applyComparisonColor('revenueQoq', performance.revenue_qoq);
    }
    
    // 영업이익: 컨센서스 값과 증가율 표시
    const operatingProfitItem = document.getElementById('operatingProfit').closest('.performance-item');
    if (performance.operating_profit) {
        document.getElementById('operatingProfit').textContent = performance.operating_profit;
    }
    operatingProfitItem.classList.add('has-comparison');
    if (performance.operating_profit_yoy) {
        document.getElementById('operatingProfitYoy').textContent = `전년동기: ${performance.operating_profit_yoy}`;
        applyComparisonColor('operatingProfitYoy', performance.operating_profit_yoy);
    }
    if (performance.operating_profit_qoq) {
        document.getElementById('operatingProfitQoq').textContent = `직전분기: ${performance.operating_profit_qoq}`;
        applyComparisonColor('operatingProfitQoq', performance.operating_profit_qoq);
    }
    // 컨센서스 비교는 숨김
    document.getElementById('operatingProfitConsensus').textContent = '';
    
    // 순이익: 컨센서스 값만 표시
    if (performance.net_profit) {
        document.getElementById('netProfit').textContent = performance.net_profit;
    }
    document.getElementById('performanceSummary').textContent = performance.summary;
    
    // 어닝서프라이즈는 항상 숨김
    document.getElementById('earningsSurpriseItem').style.display = 'none';
}

// 비교 데이터 색상 적용
function applyComparisonColor(elementId, value) {
    const element = document.getElementById(elementId);
    if (value && value.includes('+')) {
        element.style.color = 'var(--up-color)';
        element.style.fontWeight = '600';
    } else if (value && value.includes('-')) {
        element.style.color = 'var(--down-color)';
        element.style.fontWeight = '600';
    } else {
        element.style.color = 'var(--text-secondary)';
    }
}

// 감성 배지 렌더링
function renderSentimentBadge(elementId, sentiment) {
    const element = document.getElementById(elementId);
    if (!element) return;
    const sentimentIcon = sentiment === '긍정' || sentiment === 'positive' ? '▲' : sentiment === '부정' || sentiment === 'negative' ? '▼' : '●';
    const sentimentClass = sentiment === '긍정' || sentiment === 'positive' ? 'positive' : sentiment === '부정' || sentiment === 'negative' ? 'negative' : 'neutral';
    element.className = `sentiment-badge-large sentiment-${sentimentClass}`;
    element.innerHTML = `<span class="sentiment-icon">${sentimentIcon}</span>${sentiment}`;
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    showEmptyState();
});


