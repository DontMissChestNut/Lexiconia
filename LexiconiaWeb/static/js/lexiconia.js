class LexiconiaApp {
    constructor() {
        this.currentCard = null;
        this.allCards = [];
        this.currentIndex = 0;

        this.initializeElements();
        this.bindEvents();
        this.loadRandomCard();
    }

    initializeElements() {
        this.wordDisplay = document.getElementById('word-display');
        this.progressDisplay = document.getElementById('progressText');
        this.phoneticSymbol = document.getElementById('phonetic-symbol');
        this.phoneticAudio = document.getElementById('phonetic-audio');
        this.detailsSection = document.getElementById('details-section');

        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.randomBtn = document.getElementById('random-btn');
    }

    bindEvents() {
        this.prevBtn.addEventListener('click', () => this.prevCard());
        this.nextBtn.addEventListener('click', () => this.nextCard());
        this.randomBtn.addEventListener('click', () => this.loadRandomCard());

        // 键盘导航
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowLeft': this.prevCard(); break;
                case 'ArrowRight': this.nextCard(); break;
                case 'r': this.loadRandomCard(); break;
            }
        });
    }

    async loadCard(num = null) {
        try {
            this.showLoading();
            const url = num ? `/api/lexiconia?num=${num}` : '/api/lexiconia';
            const response = await fetch(url);
            this.currentCard = await response.json();
            this.displayCard();
        } catch (error) {
            console.error('Error loading card:', error);
            this.showError('加载单词失败，请重试');
        }
    }

    loadRandomCard() {
        this.loadCard();
    }

    displayCard() {
        // 显示单词基本信息
        this.wordDisplay.textContent = this.currentCard.word;
        this.progressDisplay.textContent = `${this.currentIndex + 1} / ${this.allCards.length}`;

        // 清空之前的释义
        this.detailsSection.innerHTML = '';

        // 动态生成每个释义的section
        this.currentCard.definitions.forEach((definition, index) => {
            this.createDefinitionSection(definition, index);
        });

        // 如果没有释义，显示提示
        if (this.currentCard.definitions.length === 0) {
            this.detailsSection.innerHTML = '<div class="no-definitions">暂无释义</div>';
        }
    }

    createDefinitionSection(definition, index) {
        const detailElement = document.createElement('div');
        detailElement.className = 'detail';
        detailElement.setAttribute('data-index', index);

        // 创建释义头部（等级|词性|补充）
        const header = document.createElement('div');
        header.className = 'definition-header';

        const levelSpan = document.createElement('span');
        levelSpan.className = 'level';
        levelSpan.textContent = definition.level || 'N/A';

        const partOfSpeechSpan = document.createElement('span');
        partOfSpeechSpan.className = 'part-of-speech';
        partOfSpeechSpan.textContent = definition.part_of_speech || 'N/A';

        header.appendChild(levelSpan);
        header.appendChild(document.createTextNode(' | '));
        header.appendChild(partOfSpeechSpan);

        // 如果有补充信息，添加到头部
        if (definition.addition && definition.addition !== '-') {
            const additionSpan = document.createElement('span');
            additionSpan.className = 'addition';
            additionSpan.textContent = ` | ${definition.addition}`;
            header.appendChild(additionSpan);
        }

        detailElement.appendChild(header);

        // 创建解释内容
        const explainDiv = document.createElement('div');
        explainDiv.className = 'explain';

        // 英文解释
        if (definition.explanation_e && definition.explanation_e !== '-') {
            const englishExplain = document.createElement('div');
            englishExplain.className = 'english-explanation';
            englishExplain.innerHTML = `----- ${definition.explanation_e}`;
            explainDiv.appendChild(englishExplain);
        }

        // 中文解释
        if (definition.explanation_c && definition.explanation_c !== '-') {
            const chineseExplain = document.createElement('div');
            chineseExplain.className = 'chinese-explanation';
            chineseExplain.innerHTML = `----- ${definition.explanation_c}`;
            explainDiv.appendChild(chineseExplain);
        }

        detailElement.appendChild(explainDiv);

        // 如果有例句，添加例句部分
        if (definition.example_sentence) {
            const sentenceDiv = document.createElement('div');
            sentenceDiv.className = 'illustrative sentence';
            sentenceDiv.textContent = definition.example_sentence;
            detailElement.appendChild(sentenceDiv);
        }

        this.detailsSection.appendChild(detailElement);
    }

    showLoading() {
        this.detailsSection.innerHTML = '<div class="loading">加载中...</div>';
    }

    showError(message) {
        this.detailsSection.innerHTML = `<div class="error">${message}</div>`;
    }

    prevCard() {
        if (this.allCards.length === 0) return;

        this.currentIndex = (this.currentIndex - 1 + this.allCards.length) % this.allCards.length;
        this.loadCard(this.allCards[this.currentIndex]);
    }

    nextCard() {
        if (this.allCards.length === 0) return;

        this.currentIndex = (this.currentIndex + 1) % this.allCards.length;
        this.loadCard(this.allCards[this.currentIndex]);
    }

    // 初始化加载卡片列表
    async initializeCardsList() {
        try {
            const response = await fetch('/api/lexiconia/list');        
            this.allCards = await response.json();

        } catch (error) {
            console.error('Error loading cards list:', error);
        }
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new LexiconiaApp();
    await app.initializeCardsList();
});