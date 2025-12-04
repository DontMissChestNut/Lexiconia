class LexiconiaApp {
    constructor() {
        
    }
    // 初始化加载卡片列表
    init() {
        console.log('init');
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new LexiconiaApp();
    app.init();
});