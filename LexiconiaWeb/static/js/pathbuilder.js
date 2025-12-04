class PathBuilder {
    constructor() {
        this.graph = [];
        this.word_list = [];

        this.word = "";
        this.word_num = 0;

        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.wordForm = document.getElementById('word-selecter');
        this.wordsInput = document.getElementById('word-select');
        this.resultContainer = document.getElementById('result-container');
    }
        bindEvents() {
        if (this.wordForm) {
            this.wordForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }

    async handleSubmit(e) {
        e.preventDefault();

        this.word = this.wordsInput.value.trim();

                if (!this.word) {
            this.showMessage('请输入要添加的单词', 'error');
            return;
        }
        console.log(this.word);

        try{
            const response = await fetch(`/api/pathbuilder/${this.word}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ words: this.word })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.word_num = result.num;

                this.illustrateGraph();
            } else {
                console.error('Error building path:', "构建路径失败，请重试");  
            }
            
        } catch (error) {
            console.error('Error building path:', "构建路径失败，请重试");  
        }
    }

    initPathBuilder() {
        this.loadPathGraph();
    }

    async loadPathGraph() {
        try {
            const response = await fetch('/api/pathbuilder');
            const data = await response.json();
            

            this.graph = data.graph;
            this.word_list = data.word_list;
        } catch (error) {
            console.error('Error loading path graph:', error);
        }
    }

    illustrateGraph() {
        console.log("Graph:", this.graph);
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new PathBuilder();
    app.initPathBuilder();
});