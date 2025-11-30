// 在 script.js 文件末尾添加以下代码

// Add Words 页面功能
class AddWordsApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.addWordsForm = document.getElementById('add-words-form');
        this.wordsInput = document.getElementById('words-input');
        this.resultMessage = document.getElementById('result-message');
    }

    bindEvents() {
        if (this.addWordsForm) {
            this.addWordsForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const wordsString = this.wordsInput.value.trim();
        
        if (!wordsString) {
            this.showMessage('请输入要添加的单词', 'error');
            return;
        }
        console.log(wordsString);
        
        try {
            const response = await fetch('/api/addmyreview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ words: wordsString })
            });
            
            const result = await response.json();
            
            if (result.success) {
                let message = `<strong>${result.message}</strong>`;
                
                if (result.added && result.added.length > 0) {
                    message += `<div class="word-list"><strong>添加的单词：</strong> ${result.added.join(', ')}</div>`;
                }
                
                if (result.skipped && result.skipped.length > 0) {
                    message += `<div class="word-list"><strong>跳过的单词：</strong> ${result.skipped.join(', ')}</div>`;
                }
                
                this.showMessage(message, 'success');
                this.wordsInput.value = ''; // 清空输入框
            } else {
                this.showMessage(result.message, 'error');
            }
            
        } catch (error) {
            console.error('Error adding words:', error);
            this.showMessage('添加单词失败，请重试', 'error');
        }
    }
    
    showMessage(message, type) {
        this.resultMessage.innerHTML = message;
        this.resultMessage.className = `result-message ${type}`;
        this.resultMessage.style.display = 'block';
        
        // 滚动到结果消息
        this.resultMessage.scrollIntoView({ behavior: 'smooth' });
    }

        // 初始化加载卡片列表
    async initializeCardsList() {
        try {
            const response = await fetch('/api/cards/list');
            this.allCards = await response.json();

        } catch (error) {
            console.error('Error loading cards list:', error);
        }
    }
}
// 初始化应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new AddWordsApp();
    await app.initializeCardsList();
});