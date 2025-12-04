class DailyReviewApp {
    constructor() {
        this.numofGroup = 20;
        this.numofTask = 5;

        this.currentCard = null;
        this.originRepo = [];       // 所有单词(origin) - all
        this.finishedRoot = [];     // 已完成单词 - Root


        this.dailyRepo = [];        // 所有单词 - all
        this.displayTask = 0;
        this.dailyProcess = 0;      // 今日复习进度 process / daily

        this.currentRepo = [];      // 当前复习单词 - 20
        this.currentTask = 0;
        this.currentProcess = 0;    // 本次复习进度 process / 20

        this.currentGroup = [];     // 当前显示的5个单词
        this.currentIndex = 0;      // 本组复习进度 index / 5

        this.currentCard = null;

        // this.reviewQueue = []; // 复习队列

        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.wordDisplay = document.getElementById('word-display');
        this.progressDisplay = document.getElementById('progress');
        this.phoneticSymbol = document.getElementById('phonetic-symbol');
        this.phoneticAudio = document.getElementById('phonetic-audio');
        this.detailsSection = document.getElementById('details-section');

        // this.prevBtn = document.getElementById('prevBtn');
        // this.nextBtn = document.getElementById('nextBtn');
        // this.randomBtn = document.getElementById('randomBtn');

        this.fmlBtn = document.getElementById('fmlBtn');
        this.unfmlBtn = document.getElementById('unfmlBtn');
    }

    bindEvents() {
        // this.prevBtn.addEventListener('click', () => this.prevCard());
        // this.nextBtn.addEventListener('click', () => this.nextCard());
        // this.randomBtn.addEventListener('click', () => this.loadReviewRepo());

        this.fmlBtn.addEventListener('click', () => this.markFamiliar());
        this.unfmlBtn.addEventListener('click', () => this.markUnfamiliar());

        // 键盘导航
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowLeft': this.prevCard(); break;
                case 'ArrowRight': this.nextCard(); break;
                case 'r': this.loadReviewRepo(); break;
            }
        });
    }

    initDailyReviewApp() {
        this.loadReviewRepo();              // load inital review repo, display current group
    }

    loadReviewRepo() {
        this.initializeCardsList();
    }

    // 初始化加载复习列表
    async initializeCardsList() {
        try {
            const response = await fetch('/api/dailyreview/list');
            this.originRepo = await response.json();
        } catch (error) {
            console.error('Error loading cards list:', error);
        }

        this.dailyRepo = this.originRepo.reviews;

        console.log(' ========== initializeCardsList : this.dailyRepo ========== ',
            this.dailyRepo);

        let l = this.numofGroup;
        if (this.dailyRepo.length < this.numofGroup) {
            l = this.dailyRepo.length;
        }

        this.currentRepo = deepCloneByJSON(this.dailyRepo);

        for (let i = 0; i < this.numofTask; i++) {
            this.currentGroup.push(deepCloneByJSON(this.currentRepo.shift()));
        }

        this.displayTask = this.dailyRepo.length;
        this.currentCard = this.currentGroup.shift();


        this.displayCurrCard();
    }

    displayCurrCard() {
        // 显示单词基本信息
        this.wordDisplay.textContent = this.currentCard.Word;
        this.progressDisplay.textContent = `${this.dailyProcess} / ${this.displayTask}`;
        // TODO: 当前复习进度显示

        // 清空之前的释义
        this.detailsSection.innerHTML = '';

        let definitions = this.currentCard.Details;

        // 动态生成每个释义的section
        definitions.forEach((definition, index) => {
            this.createDefinitionSection(definition, index);
        });

        // 如果没有释义，显示提示
        if (definitions.length === 0) {
            this.detailsSection.innerHTML = '<div class="no-definitions">暂无释义</div>';
        }
    }

    displayEndReview() {
        this.showCompletion();
    }

    loadCards() {
        let toLoad = this.numofTask - this.currentGroup.length > this.currentRepo.length ? this.currentRepo.length : this.numofTask - this.currentGroup.length;

        for (let i = 0; i < toLoad; i++) {
            this.currentGroup.push(deepCloneByJSON(this.currentRepo.shift()));
        }

        console.log(' ========== loadCards : this.currentGroup ========== ',
            this.currentGroup);
    }

    async loadCards_abolished(num = null) {
        try {
            this.showLoading();
            const url = num ? `/api/dailyreview?num=${num}` : '/api/dailyreview';
            const response = await fetch(url);
            let data = await response.json();
            this.cardsRepo = data.reviews;


            // this.displayCurrCard();
        } catch (error) {
            console.error('Error loading card:', error);
            this.showError('加载单词失败，请重试');
        }
    }

    createDefinitionSection(definition, index) {
        // console.log(' ========== displayCurrCard : this.currentCard.definitions ========== ', 
        //     definition);
        const detailElement = document.createElement('div');
        detailElement.className = 'detail';
        detailElement.setAttribute('data-index', index);

        // 创建释义头部（等级|词性|补充）
        const header = document.createElement('div');
        header.className = 'definition-header';

        const levelSpan = document.createElement('span');
        levelSpan.className = 'level';
        levelSpan.textContent = definition.Level || 'N/A';

        const partOfSpeechSpan = document.createElement('span');
        partOfSpeechSpan.className = 'part-of-speech';
        partOfSpeechSpan.textContent = definition.part_of_speech || 'N/A';

        header.appendChild(levelSpan);
        header.appendChild(document.createTextNode(' | '));
        header.appendChild(partOfSpeechSpan);

        // 如果有补充信息，添加到头部
        if (definition.Addition && definition.Addition !== '-') {
            const additionSpan = document.createElement('span');
            additionSpan.className = 'addition';
            additionSpan.textContent = ` | ${definition.Addition}`;
            header.appendChild(additionSpan);
        }

        detailElement.appendChild(header);

        // 创建解释内容
        const explainDiv = document.createElement('div');
        explainDiv.className = 'explain';

        // TODO: 英文解释
        // if (definition.explanation_e && definition.explanation_e !== '-') {
        //     const englishExplain = document.createElement('div');
        //     englishExplain.className = 'english-explanation';
        //     englishExplain.innerHTML = `----- ${definition.explanation_e}`;
        //     explainDiv.appendChild(englishExplain);
        // }

        // 中文解释
        if (definition.ExplainationC && definition.ExplainationC !== '-') {
            const chineseExplain = document.createElement('div');
            chineseExplain.className = 'chinese-explanation';
            chineseExplain.innerHTML = `${definition.ExplainationC}`;
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
        if (this.cardsRepo.length === 0) return;

        this.currentProcess = (this.currentProcess - 1 + this.cardsRepo.length) % this.cardsRepo.length;
        this.loadCards_abolished(this.cardsRepo[this.currentProcess]);
    }

    nextCard() {
        if (this.cardsRepo.length === 0) return;

        this.currentProcess = (this.currentProcess + 1) % this.cardsRepo.length;
        this.loadCards_abolished(this.cardsRepo[this.currentProcess]);
    }

    markFamiliar() {
        this.currentProcess += 1;
        this.dailyProcess += 1;
        this.currentIndex += 1;
        this.finishedRoot.push(deepCloneByJSON(this.currentCard.Root));
        if (this.currentRepo.length === 0 && this.currentGroup.length === 0) {
            this.progressDisplay.textContent = `${this.dailyProcess} / ${this.displayTask}`;

            // 所有单词都被学习完了
            this.showCompletionModal();
            return;
        }
        else {
            if (this.currentGroup.length > 0) { this.currentCard = this.currentGroup.shift(); }

            if (this.currentIndex === this.numofTask - 1) {
                this.currentIndex = 0;
                this.loadCards();
            }

            this.displayCurrCard();
        }


    }

    markUnfamiliar() {
        if (this.currentRepo.length === 0 && this.currentGroup.length === 0) {
            this.progressDisplay.textContent = `${this.dailyProcess} / ${this.displayTask}`;

            this.showCompletionModal();
            return;
        }

        this.currentIndex += 1;
        this.currentGroup.push(this.currentCard);

        if (this.currentGroup.length > 0) { this.currentCard = this.currentGroup.shift(); }

        if (this.currentIndex === this.numofTask - 1 && this.currentRepo.length !== 0) {
            this.currentIndex = 0;
            this.loadCards();
        }

        console.log(' ========== markUnfamiliar : this.currentCard.length ========== ',
            this.currentCard.length);

        this.displayCurrCard();
    }
    // 显示完成学习的模态窗口
    showCompletionModal() {
        // 创建模态窗口背景
        const modalOverlay = document.createElement('div');
        modalOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        `;

        // 创建模态窗口内容
        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            width: 80%;
        `;

        // 创建标题
        const title = document.createElement('h2');
        title.textContent = '恭喜完成学习！';
        title.style.cssText = `
            margin-bottom: 20px;
            color: #4CAF50;
            font-size: 24px;
        `;

        // 创建描述文本
        const description = document.createElement('p');
        description.textContent = `您已完成今日所有 ${this.displayTask} 个单词的学习`;
        description.style.cssText = `
            margin-bottom: 30px;
            font-size: 16px;
            color: #666;
            line-height: 1.5;
        `;

        // 创建按钮容器
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = `
            display: flex;
            gap: 15px;
            justify-content: center;
        `;

        // 创建"继续下一组"按钮
        const nextGroupBtn = document.createElement('button');
        nextGroupBtn.textContent = '继续下一组';
        nextGroupBtn.style.cssText = `
            padding: 12px 24px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        `;
        nextGroupBtn.onmouseover = () => nextGroupBtn.style.background = '#45a049';
        nextGroupBtn.onmouseout = () => nextGroupBtn.style.background = '#4CAF50';

        // 创建"回到引导界面"按钮
        const guideBtn = document.createElement('button');
        guideBtn.textContent = '回到引导界面';
        guideBtn.style.cssText = `
            padding: 12px 24px;
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        `;
        guideBtn.onmouseover = () => guideBtn.style.background = '#1976D2';
        guideBtn.onmouseout = () => guideBtn.style.background = '#2196F3';

        // 组装模态窗口
        buttonContainer.appendChild(nextGroupBtn);
        buttonContainer.appendChild(guideBtn);
        modalContent.appendChild(title);
        modalContent.appendChild(description);
        modalContent.appendChild(buttonContainer);
        modalOverlay.appendChild(modalContent);

        // 添加到页面
        document.body.appendChild(modalOverlay);

        // 绑定按钮事件
        nextGroupBtn.addEventListener('click', () => {
            document.body.removeChild(modalOverlay);
            // TODO: post finishedRoot to server
            this.postFinishedRootToServer();
            this.loadNextGroup();
        });

        guideBtn.addEventListener('click', () => {
            document.body.removeChild(modalOverlay);
            // TODO: post finishedRoot to server
            this.postFinishedRootToServer();
            this.redirectToGuide();
        });

        // 点击背景关闭（可选）
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                document.body.removeChild(modalOverlay);
            }
        });
    }

    // 加载下一组单词
    loadNextGroup() {
        // 重置状态，加载新的单词组
        this.currentRepo = [];
        this.currentGroup = [];
        this.currentIndex = 0;
        this.currentProcess = 0;
        this.dailyProcess = 0;

        // 这里可以根据您的需求从服务器获取新的单词组
        // 暂时先重新初始化
        this.initializeCardsList();
    }

    // 跳转到引导界面
    redirectToGuide() {
        // 根据您的实际路由进行跳转
        window.location.href = '/'; // 示例
        console.log('跳转到引导界面');
        // 或者触发应用状态改变
        // this.showGuideInterface();
    }

    // 原有的显示完成方法（如果需要保留的话）
    showCompletion() {
        // 原有的完成显示逻辑（如果有的话）
        this.wordDisplay.textContent = '学习完成！';
        this.detailsSection.innerHTML = '<div class="completion-message">恭喜您完成了今日的所有学习任务！</div>';
    }

    // TODO: post finishedRoot to server
    async postFinishedRootToServer() {
        try {
            const response = await fetch('/api/dailyreview/finish', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ root: this.finishedRoot })
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('单词已完成');
            } else {
                console.error('单词不存在于复习列表');
            }
            
        } catch (error) {
            console.error('Error posting finished root:', error);
        }
    }
}

function deepCloneByJSON(obj) {
    return JSON.parse(JSON.stringify(obj));
}


// 初始化应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new DailyReviewApp();
    app.initDailyReviewApp();
});