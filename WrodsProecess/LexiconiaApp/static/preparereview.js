class PrepareReview {
    constructor() {
        this.words = []; // 所有待处理的单词
        this.currentIndex = 0; // 当前单词索引
        this.selectedWords = []; // 用户选择的不熟悉单词
        this.batchSize = 120; // 初始批次大小
        this.additionalBatchSize = 20; // 后续批次大小
        this.targetCount = 5; // 目标复习单词数
        this.isLoading = false;
        this.isCompleted = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadInitialWords();
    }
    
    initializeElements() {
        this.wordDisplay = document.getElementById('word-display');
        this.wordDetails = document.getElementById('word-details');
        this.progressText = document.getElementById('progress-text');
        this.progressPercent = document.getElementById('progress-percent');
        this.progressFill = document.getElementById('progress-fill');
        
        this.btnSkip = document.getElementById('btn-skip');
        this.btnUnfamiliar = document.getElementById('btn-unfamiliar');
        this.btnFinish = document.getElementById('btn-finish');
        this.btnStartReview = document.getElementById('btn-start-review');
        
        this.reviewCard = document.getElementById('review-card');
        this.completionMessage = document.getElementById('completion-message');
        this.selectedCountDisplay = document.getElementById('selected-count');
    }
    
    bindEvents() {
        this.btnSkip.addEventListener('click', () => this.skipWord());
        this.btnUnfamiliar.addEventListener('click', () => this.markUnfamiliar());
        this.btnFinish.addEventListener('click', () => this.finishPreparation());
        this.btnStartReview.addEventListener('click', () => this.startReview());
        
        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            if (this.isLoading || this.isCompleted) return;
            
            switch(e.key) {
                case 'ArrowLeft':
                case '1':
                    this.skipWord();
                    break;
                case 'ArrowRight':
                case '2':
                    this.markUnfamiliar();
                    break;
                case 'Escape':
                    this.finishPreparation();
                    break;
            }
        });
    }
    
    async loadInitialWords() {
        this.isLoading = true;
        this.updateButtonStates();
        
        try {
            // 从后端获取初始批次单词
            const response = await fetch('/api/prepare_review_words?count=' + this.batchSize);
            const data = await response.json();

            console.log('接收到的单词数据:', data);
            
            if (data.words && data.words.length > 0) {
                this.words = data.words;
                this.displayCurrentWord();
            } else {
                this.showNoWordsMessage();
            }
        } catch (error) {
            console.error('加载单词失败:', error);
            this.showErrorMessage('加载单词失败，请刷新页面重试');
        } finally {
            this.isLoading = false;
            this.updateButtonStates();
        }
    }
    
    async loadMoreWords() {
        this.isLoading = true;
        this.updateButtonStates();
        
        try {
            // 从后端获取更多单词
            const response = await fetch('/api/prepare_review_words?count=' + this.additionalBatchSize);
            const data = await response.json();
            
            if (data.words && data.words.length > 0) {
                this.words = this.words.concat(data.words);
                this.displayCurrentWord();
            } else {
                this.showNoMoreWordsMessage();
            }
        } catch (error) {
            console.error('加载更多单词失败:', error);
            this.showErrorMessage('加载更多单词失败');
        } finally {
            this.isLoading = false;
            this.updateButtonStates();
        }
    }
    
    displayCurrentWord() {
        console.log('DoadeWord:',"loading");
        if (this.currentIndex >= this.words.length) {
            // 当前批次已用完，尝试加载更多
            if (this.selectedWords.length < this.targetCount) {
                this.loadMoreWords();
            } else {
                this.completePreparation();
            }
            return;
        }
        
        const wordData = this.words[this.currentIndex];
        this.wordDisplay.textContent = wordData.word;
        
        console.log("wordInfo: ", wordData);
        this.renderWordDetails(wordData);
        this.updateProgress();
    }
    
    renderWordDetails(wordData) {
        this.wordDetails.innerHTML = '';
        
        console.log("wordPhonetico: ", wordData.phonetic);
        /* =============== TODO =============== */
        // 显示单词的基本信息   音标信息
        // if (wordData.phonetic) {
        //     const phoneticElem = document.createElement('div');
        //     phoneticElem.className = 'phonetic';
        //     phoneticElem.textContent = wordData.phonetic;
        //     this.wordDetails.appendChild(phoneticElem);
        // }
        
        // 显示单词的释义
        if (wordData.details && wordData.details.length > 0) {

            const definitionElem = document.createElement('div');
            definitionElem.className = 'definition-preview';

             wordData.details.forEach((detail, index) => {
                console.log(`详情 ${index + 1}:`, detail);
                
                const info = document.createElement('div')
                info.className = `info${index}`;

                const lElem = document.createElement('span');
                lElem.className = "defination-level";
                lElem.textContent = detail.Level;
                info.appendChild(lElem);
                
                const pElem = document.createElement('span');
                pElem.className = "defination-partofspeech"
                pElem.textContent = detail.part_of_speech;
                info.appendChild(pElem);

                const aElem = document.createElement('span');
                aElem.className = "defination-addition"
                aElem.textContent = detail.Addition;
                info.appendChild(aElem);

                definitionElem.appendChild(info);

                const eeElem = document.createElement('div');
                eeElem.className = "defination-explainatione"
                eeElem.textContent = detail.ExplainationE;
                definitionElem.appendChild(eeElem);


                const ecElem = document.createElement('span');
                ecElem.className = "defination-explainationc"
                ecElem.textContent = detail.ExplainationC;
                definitionElem.appendChild(ecElem);
            });
            
            this.wordDetails.appendChild(definitionElem);
        }
    }
    
    skipWord() {
        // 只是跳过，不做任何标记
        this.currentIndex++;
        this.displayCurrentWord();
    }
    
    markUnfamiliar() {
        const currentWord = this.words[this.currentIndex];
        this.selectedWords.push(currentWord);
        
        // 检查是否达到目标数量
        if (this.selectedWords.length >= this.targetCount) {
            this.completePreparation();
            return;
        }
        
        this.currentIndex++;
        this.displayCurrentWord();
    }
    
    updateProgress() {
        const progress = (this.selectedWords.length / this.targetCount) * 100;
        this.progressText.textContent = `${this.selectedWords.length}/${this.targetCount}`;
        this.progressPercent.textContent = `${Math.round(progress)}%`;
        this.progressFill.style.width = `${progress}%`;
    }
    
    updateButtonStates() {
        this.btnSkip.disabled = this.isLoading;
        this.btnUnfamiliar.disabled = this.isLoading;
    }
    
    async finishPreparation() {
        // 用户主动结束准备
        if (this.selectedWords.length === 0) {
            if (!confirm('您还没有选择任何单词，确定要结束吗？')) {
                return;
            }
        }
        
        await this.completePreparation();
    }
    
    async completePreparation() {
        this.isCompleted = true;
        
        // 更新后端，将选中的单词标记为今日复习
        try {

            console.log("selectedWords:", this.selectedWords);

            const response = await fetch('/api/update_review_list', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    selectedWords: this.selectedWords
                })
            });
            
            if (response.ok) {
                this.showCompletionMessage();
            } else {
                throw new Error('更新复习列表失败');
            }
        } catch (error) {
            console.error('保存复习列表失败:', error);
            alert('保存复习列表失败，请重试');
            this.isCompleted = false;
        }
    }
    
    showCompletionMessage() {
        this.selectedCountDisplay.textContent = this.selectedWords.length;
        this.reviewCard.style.display = 'none';
        this.completionMessage.style.display = 'block';
    }
    
    startReview() {
        // 跳转到复习页面
        window.location.href = '/dailyreview';
    }
    
    showNoWordsMessage() {
        this.wordDisplay.textContent = '暂无需要准备的单词';
        this.wordDetails.innerHTML = '<p>所有单词都已加入复习或已完成复习。</p>';
        this.btnSkip.disabled = true;
        this.btnUnfamiliar.disabled = true;
    }
    
    showNoMoreWordsMessage() {
        this.wordDisplay.textContent = '没有更多单词';
        this.wordDetails.innerHTML = '<p>已加载所有可用单词。</p>';
        this.btnSkip.disabled = true;
        this.btnUnfamiliar.disabled = true;
        
        // 即使没有达到目标数量，也允许用户结束
        setTimeout(() => {
            if (confirm(`已选择 ${this.selectedWords.length} 个单词，是否结束准备？`)) {
                this.finishPreparation();
            }
        }, 500);
    }
    
    showErrorMessage(message) {
        this.wordDisplay.textContent = '出错';
        this.wordDetails.innerHTML = `<p class="error">${message}</p>`;
        this.btnSkip.disabled = true;
        this.btnUnfamiliar.disabled = true;
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new PrepareReview();
});