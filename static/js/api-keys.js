// API 키 관리 유틸리티

// API 키 가져오기
function getApiKeys() {
    return {
        dart: localStorage.getItem('OPEN_DART_API_KEY'),
        finnhub: localStorage.getItem('FINNHUB_API_KEY'),
        gemini: localStorage.getItem('GEMINI_API_KEY')
    };
}

// API 키 확인
function checkApiKeys(required = []) {
    const keys = getApiKeys();
    const missing = [];

    if (required.includes('dart') && !keys.dart) {
        missing.push('Open DART API');
    }
    if (required.includes('finnhub') && !keys.finnhub) {
        missing.push('Finnhub API');
    }
    if (required.includes('gemini') && !keys.gemini) {
        missing.push('Gemini AI API');
    }

    if (missing.length > 0) {
        const message = `다음 API 키가 필요합니다: ${missing.join(', ')}\n\n설정 페이지로 이동하시겠습니까?`;
        if (confirm(message)) {
            window.location.href = '/settings';
        }
        return false;
    }

    return true;
}

// 페이지 로드 시 API 키 확인 배너 표시
window.addEventListener('DOMContentLoaded', function() {
    const keys = getApiKeys();
    
    // API 키가 하나도 없으면 알림 배너 표시
    if (!keys.dart && !keys.finnhub) {
        showApiKeyBanner();
    }
});

function showApiKeyBanner() {
    const banner = document.createElement('div');
    banner.id = 'api-key-banner';
    banner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #fef5e7;
        border-bottom: 2px solid #f9e79f;
        padding: 15px;
        text-align: center;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;
    banner.innerHTML = `
        <span style="color: #7d6608; font-weight: 600;">
            🔑 서비스를 사용하려면 API 키 설정이 필요합니다.
        </span>
        <button onclick="window.location.href='/settings'" style="
            margin-left: 15px;
            padding: 8px 16px;
            background: #3182ce;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        ">
            API 키 설정하기
        </button>
        <button onclick="document.getElementById('api-key-banner').remove()" style="
            margin-left: 10px;
            padding: 8px 16px;
            background: #e2e8f0;
            color: #2d3748;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        ">
            닫기
        </button>
    `;
    document.body.prepend(banner);
}
