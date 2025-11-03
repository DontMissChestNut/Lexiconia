document.addEventListener('DOMContentLoaded', function() {
    const wordElement = document.getElementById('word');
    const phoneticElement = document.getElementById('phonetic');
    const meaningElement = document.getElementById('meaning');
    const exampleElement = document.getElementById('example');
    const progressElement = document.getElementById('progress');
    const nextBtn = document.getElementById('nextBtn');
    
    // 获取初始单词索引
    let currentIndex = 1; // 从1开始，因为第一个单词已经显示
    
    // 添加点击事件监听器
    nextBtn.addEventListener('click', function() {
        // 禁用按钮防止重复点击
        nextBtn.disabled = true;
        nextBtn.textContent = '加载中...';
        
        // 发送请求获取下一个单词
        fetch(`/next_word/${currentIndex}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('网络响应不正常');
                }
                return response.json();
            })
            .then(data => {
                // 更新页面内容
                updateWordCard(data);
                
                // 更新当前索引
                currentIndex = data.index;
                
                // 恢复按钮状态
                nextBtn.disabled = false;
                nextBtn.textContent = '下一个单词';
            })
            .catch(error => {
                console.error('获取单词失败:', error);
                alert('获取单词失败，请刷新页面重试');
                
                // 恢复按钮状态
                nextBtn.disabled = false;
                nextBtn.textContent = '下一个单词';
            });
    });
    
    // 更新单词卡片内容
    function updateWordCard(wordData) {
        // 添加淡出效果
        wordElement.style.opacity = 0;
        phoneticElement.style.opacity = 0;
        meaningElement.style.opacity = 0;
        exampleElement.style.opacity = 0;
        
        // 短暂延迟后更新内容并淡入
        setTimeout(() => {
            wordElement.textContent = wordData.word;
            phoneticElement.textContent = wordData.phonetic;
            meaningElement.textContent = wordData.meaning;
            exampleElement.textContent = wordData.example;
            progressElement.textContent = `单词 ${wordData.index} / ${wordData.total}`;
            
            // 淡入效果
            wordElement.style.opacity = 1;
            phoneticElement.style.opacity = 1;
            meaningElement.style.opacity = 1;
            exampleElement.style.opacity = 1;
        }, 300);
    }
});