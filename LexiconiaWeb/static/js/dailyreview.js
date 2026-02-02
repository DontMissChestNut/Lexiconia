class DailyReviewApp {
    constructor() {
        this.numofGroup = 20;
        this.numofTask = 5;

        this.currentCard = null;
        this.originRepo = [];       // 所有单词(origin) - all
        this.finishedRoot = [];     // 已完成单词 - root

        this.dailyRepo = [];        // 所有单词 - all
        this.displayTask = 0;
        this.dailyProcess = 0;      // 今日复习进度 process / daily

        this.currentRepo = [];      // 当前复习单词 - 20
        this.currentTask = 0;       // 20
        this.currentProcess = 0;    // 本次复习进度 process / 20

        this.currentGroup = [];     // 当前显示的5个单词
        this.currentIndex = 0;      // 本组复习进度 index / 5

        this.currentCard = null;
        this.isDefinitionVisible = false; // 新增：控制释义显示状态

        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.wordDisplay = document.getElementById('word-display');
        this.progressDisplay = document.getElementById('progress-text');
        this.phoneticSymbol = document.getElementById('phonetic-symbol');
        this.phoneticAudio = document.getElementById('phonetic-audio');
        this.detailsSection = document.getElementById('details-section');

        // 新增：显示释义按钮
        this.btnShowDefinition = document.getElementById('show-definition-btn');

        this.fmlBtn = document.getElementById('familiar-btn');
        this.unfmlBtn = document.getElementById('unfamiliar-btn');

        // 新增：模态窗口元素
        this.modalOverlay = document.getElementById('completion-modal');
        this.completedCount = document.getElementById('completed-count');
        this.modalNextGroup = document.getElementById('next-group-btn');
        this.modalToGuide = document.getElementById('to-guide-btn');
    }

    bindEvents() {
        // 绑定显示释义按钮事件
        this.btnShowDefinition.addEventListener('click', () => this.toggleDefinition());

        this.fmlBtn.addEventListener('click', () => this.markFamiliar());
        this.unfmlBtn.addEventListener('click', () => this.markUnfamiliar());

        // 绑定模态窗口按钮事件
        this.modalNextGroup.addEventListener('click', () => this.handleNextGroup());
        this.modalToGuide.addEventListener('click', () => this.redirectToGuide());

        // 键盘导航
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowLeft': this.prevCard(); break;
                case 'ArrowRight': this.nextCard(); break;
                case 'r': this.loadReviewRepo(); break;
                case ' ': // 空格键切换释义显示
                    this.toggleDefinition();
                    e.preventDefault(); // 防止页面滚动
                    break;
            }
        });
    }

    // 切换释义显示状态的方法
    toggleDefinition() {
        this.isDefinitionVisible = !this.isDefinitionVisible;

        if (this.isDefinitionVisible) {
            this.detailsSection.style.display = 'block';
            this.btnShowDefinition.innerHTML = '<span class="btn-icon">👁️</span><span class="btn-text">隐藏释义</span>';
            this.btnShowDefinition.classList.add('active');
        } else {
            this.detailsSection.style.display = 'none';
            this.btnShowDefinition.innerHTML = '<span class="btn-icon">🔍</span><span class="btn-text">显示释义</span>';
            this.btnShowDefinition.classList.remove('active');
        }
    }

    // 显示完成学习的模态窗口（优化版）
    showCompletionModal() {
        // 更新完成单词数量
        this.completedCount.textContent = this.displayTask;

        // 显示模态窗口
        this.modalOverlay.style.display = 'flex';
    }

    // 处理继续下一组
    handleNextGroup() {
        this.hideCompletionModal();
        this.postFinishedRootToServer();
        this.loadNextGroup();
    }

    // 隐藏模态窗口
    hideCompletionModal() {
        this.modalOverlay.style.display = 'none';
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
        this.displayTask = this.dailyRepo.length;

        // load current repo and group, reset task and process
        this.loadCurrentRepo();
        this.loadCurrentGroup();

        // load current card
        this.currentCard = this.currentGroup.shift();


        this.displayCurrCard();
    }

    displayCurrCard() {
        // 重置释义显示状态
        this.isDefinitionVisible = false;
        this.detailsSection.style.display = 'none';
        this.btnShowDefinition.innerHTML = '<span class="btn-icon">🔍</span><span class="btn-text">显示释义</span>';
        this.btnShowDefinition.classList.remove('active');

        // 显示单词基本信息
        this.wordDisplay.textContent = this.currentCard.Word;
        this.progressDisplay.textContent = `${this.currentProcess} / ${this.currentTask}`;
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

    // 跳转到引导界面
    redirectToGuide() {
        this.hideCompletionModal();
        this.postFinishedRootToServer();
        window.location.href = '/';
    }

    // 原有的显示完成方法
    showCompletion() {
        this.wordDisplay.textContent = '学习完成！';
        this.detailsSection.innerHTML = '<div class="completion-message">恭喜您完成了今日的所有学习任务！</div>';
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

        // TODO: 英文解释
        // if (definition.explanation_e && definition.explanation_e !== '-') {
        //     const englishExplain = document.createElement('div');
        //     englishExplain.className = 'english-explanation';
        //     englishExplain.innerHTML = `----- ${definition.explanation_e}`;
        //     explainDiv.appendChild(englishExplain);
        // }

        // 中文解释
        if (definition.explaination_c && definition.explaination_c !== '-') {
            const chineseExplain = document.createElement('div');
            chineseExplain.className = 'chinese-explanation';
            chineseExplain.innerHTML = `${definition.explaination_c}`;
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
        this.finishedRoot.push(deepCloneByJSON(this.currentCard.root));
        if (this.currentRepo.length === 0 && this.currentGroup.length === 0) {
            this.progressDisplay.textContent = `${this.currentProcess} / ${this.currentTask}`;

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
            this.progressDisplay.textContent = `${this.currentProcess} / ${this.currentTask}`;

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
    
    // // 显示完成学习的模态窗口
    // showCompletionModal() {
    //     // 创建模态窗口背景
    //     const modalOverlay = document.createElement('div');
    //     modalOverlay.style.cssText = `
    //         position: fixed;
    //         top: 0;
    //         left: 0;
    //         width: 100%;
    //         height: 100%;
    //         background: rgba(0, 0, 0, 0.6);
    //         display: flex;
    //         justify-content: center;
    //         align-items: center;
    //         z-index: 1000;
    //     `;

    //     // 创建模态窗口内容
    //     const modalContent = document.createElement('div');
    //     modalContent.style.cssText = `
    //         background: white;
    //         padding: 30px;
    //         border-radius: 12px;
    //         box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    //         text-align: center;
    //         max-width: 400px;
    //         width: 80%;
    //     `;

    //     // 创建标题
    //     const title = document.createElement('h2');
    //     title.textContent = '恭喜完成学习！';
    //     title.style.cssText = `
    //         margin-bottom: 20px;
    //         color: #4CAF50;
    //         font-size: 24px;
    //     `;

    //     // 创建描述文本
    //     const description = document.createElement('p');
    //     description.textContent = `您已完成今日所有 ${this.displayTask} 个单词的学习`;
    //     description.style.cssText = `
    //         margin-bottom: 30px;
    //         font-size: 16px;
    //         color: #666;
    //         line-height: 1.5;
    //     `;

    //     // 创建按钮容器
    //     const buttonContainer = document.createElement('div');
    //     buttonContainer.style.cssText = `
    //         display: flex;
    //         gap: 15px;
    //         justify-content: center;
    //     `;

    //     // 创建"继续下一组"按钮
    //     const nextGroupBtn = document.createElement('button');
    //     nextGroupBtn.textContent = '继续下一组';
    //     nextGroupBtn.style.cssText = `
    //         padding: 12px 24px;
    //         background: #4CAF50;
    //         color: white;
    //         border: none;
    //         border-radius: 6px;
    //         cursor: pointer;
    //         font-size: 14px;
    //         transition: background 0.3s;
    //     `;
    //     nextGroupBtn.onmouseover = () => nextGroupBtn.style.background = '#45a049';
    //     nextGroupBtn.onmouseout = () => nextGroupBtn.style.background = '#4CAF50';

    //     // 创建"回到引导界面"按钮
    //     const guideBtn = document.createElement('button');
    //     guideBtn.textContent = '回到引导界面';
    //     guideBtn.style.cssText = `
    //         padding: 12px 24px;
    //         background: #2196F3;
    //         color: white;
    //         border: none;
    //         border-radius: 6px;
    //         cursor: pointer;
    //         font-size: 14px;
    //         transition: background 0.3s;
    //     `;
    //     guideBtn.onmouseover = () => guideBtn.style.background = '#1976D2';
    //     guideBtn.onmouseout = () => guideBtn.style.background = '#2196F3';

    //     // 组装模态窗口
    //     buttonContainer.appendChild(nextGroupBtn);
    //     buttonContainer.appendChild(guideBtn);
    //     modalContent.appendChild(title);
    //     modalContent.appendChild(description);
    //     modalContent.appendChild(buttonContainer);
    //     modalOverlay.appendChild(modalContent);

    //     // 添加到页面
    //     document.body.appendChild(modalOverlay);

    //     // 绑定按钮事件
    //     nextGroupBtn.addEventListener('click', () => {
    //         document.body.removeChild(modalOverlay);
    //         // TODO: post finishedRoot to server
    //         this.postFinishedRootToServer();
    //         this.loadNextGroup();
    //     });

    //     guideBtn.addEventListener('click', () => {
    //         document.body.removeChild(modalOverlay);
    //         // TODO: post finishedRoot to server
    //         this.postFinishedRootToServer();
    //         this.redirectToGuide();
    //     });

    //     // 点击背景关闭（可选）
    //     modalOverlay.addEventListener('click', (e) => {
    //         if (e.target === modalOverlay) {
    //             document.body.removeChild(modalOverlay);
    //         }
    //     });
    // }

    // 加载下一组单词
    loadNextGroup() {
        this.loadCurrentRepo();
        this.loadCurrentGroup();

        console.log(' ========== dailyRepo ========== ', this.dailyRepo);
        console.log(' ========== currentRepo :========== ', this.currentRepo);
        console.log(' ========== currentGroup :========== ', this.currentGroup);
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

    loadCurrentRepo() {
        let l = this.numofGroup;
        if (this.dailyRepo.length < this.numofGroup) {
            l = this.dailyRepo.length;
        }

        for (let i = 0; i < l; i++) {
            this.currentRepo.push(deepCloneByJSON(this.dailyRepo.shift()));      // 20个
        }

        this.currentTask = this.currentRepo.length;
        this.currentProcess = 0;    // 本次复习进度 process / 20
    }

    loadCurrentGroup() {
        let l = this.numofTask;
        if (this.currentRepo.length < this.numofTask) {
            l = this.currentRepo.length;
        }
        for (let i = 0; i < l; i++) {
            this.currentGroup.push(deepCloneByJSON(this.currentRepo.shift()));      // 5个
        }
        this.currentIndex = 0;      // 本组复习进度 index / 5
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