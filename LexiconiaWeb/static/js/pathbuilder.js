
class PathBuilder {
    constructor() {
        this.graph = [];
        this.word_list = [];
        
        // Maps for fast lookup
        this.idToWordMap = new Map();
        this.wordToIdMap = new Map();

        this.word = "";
        this.word_num = 0;

        this.svg = null;
        this.width = 0;
        this.height = 0;

        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.wordForm = document.getElementById('word-selecter');
        this.wordsInput = document.getElementById('word-select');
        this.graphContainer = document.getElementById('graph-container');
        this.detailsContent = document.getElementById('word-details-content');
        
        // Initialize D3 SVG dimensions
        this.updateDimensions();
        this.svg = d3.select("#main-svg")
            .attr("width", this.width)
            .attr("height", this.height);
            
        window.addEventListener('resize', () => {
            this.updateDimensions();
            if (this.svg) {
                this.svg.attr("width", this.width).attr("height", this.height);
                if (this.word) this.illustrateGraph(); // Re-render on resize
            }
        });
    }

    updateDimensions() {
        if (this.graphContainer) {
            this.width = this.graphContainer.clientWidth;
            this.height = this.graphContainer.clientHeight;
        }
    }

    bindEvents() {
        if (this.wordForm) {
            this.wordForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        const inputWord = this.wordsInput.value.trim();

        if (!inputWord) {
            alert('请输入查询单词');
            return;
        }

        // Check if word exists in our loaded list first
        if (this.wordToIdMap.has(inputWord)) {
            this.word = inputWord;
            this.word_num = this.wordToIdMap.get(inputWord);
            this.illustrateGraph();
        } else {
            // Fallback to API if not found (though loadPathGraph should have loaded all)
            // Or maybe the user entered a new word that needs to be created/fetched?
            // The original code called /api/pathbuilder/:word to get num.
            await this.fetchWordNum(inputWord);
        }
    }

    async fetchWordNum(word) {
        try {
            const response = await fetch(`/api/pathbuilder/${word}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ words: word })
            });
            const result = await response.json();
            
            if (result.success) {
                this.word = word;
                this.word_num = result.num;
                this.illustrateGraph();
            } else {
                alert("未找到该单词信息");
            }
        } catch (error) {
            console.error('Error fetching word:', error);
            alert("查询失败");
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
            
            this.processData();
            console.log("Graph loaded:", this.graph.length, "nodes");
        } catch (error) {
            console.error('Error loading path graph:', error);
        }
    }

    processData() {
        this.idToWordMap.clear();
        this.wordToIdMap.clear();
        
        this.word_list.forEach(item => {
            // item is like { "123": "apple" }
            const key = Object.keys(item)[0];
            const val = item[key];
            const id = parseInt(key);
            this.idToWordMap.set(id, val);
            this.wordToIdMap.set(val, id);
        });
    }

    illustrateGraph() {
        if (!this.word || !this.word_num) return;

        // 1. Find Node Data
        // The graph array contains objects with { node, root, step0... }
        // We need to find the one where node == this.word_num
        const nodeData = this.graph.find(n => n.node === this.word_num);

        if (!nodeData) {
            console.warn("No graph data found for word:", this.word, "ID:", this.word_num);
            // Fallback: Show just the center node
            this.renderD3([{ id: "center", label: this.word, type: "center", x: this.width/2, y: this.height/2, realId: this.word_num }], []);
            this.updateDetailsPanel(this.word);
            return;
        }

        // 2. Build Nodes and Links
        const nodes = [];
        const links = [];
        const centerX = this.width / 2;
        const centerY = this.height / 2;

        // Center Node
        nodes.push({ 
            id: "center", 
            label: this.word, 
            type: "center", 
            x: centerX, 
            y: centerY, 
            realId: this.word_num 
        });

        // Root Node (Up)
        if (nodeData.root && nodeData.root !== -1 && nodeData.root !== this.word_num) {
            const rootWord = this.idToWordMap.get(nodeData.root);
            if (rootWord) {
                nodes.push({ 
                    id: "root", 
                    label: rootWord, 
                    type: "root", 
                    x: centerX, 
                    y: centerY - 150, 
                    realId: nodeData.root 
                });
                links.push({ source: "center", target: "root" });
            }
        }

        // Step Nodes (Down)
        let stepNodesData = [];
        
        const parseStep = (stepStr, type) => {
            if (!stepStr) return;
            try {
                // Handle python list string representation if needed
                let cleanStr = stepStr;
                if (typeof stepStr === 'string') {
                    cleanStr = stepStr.replace(/'/g, '"');
                    const ids = JSON.parse(cleanStr);
                    if (Array.isArray(ids)) {
                        ids.forEach(id => {
                            if (id !== this.word_num) {
                                const w = this.idToWordMap.get(id);
                                if (w) stepNodesData.push({ id: id, label: w, type: type });
                            }
                        });
                    }
                }
            } catch (e) {
                console.warn("Error parsing step:", type, stepStr, e);
            }
        };

        parseStep(nodeData.step0, "step0"); // 同根词
        parseStep(nodeData.step1, "step1"); // 同根不同义
        parseStep(nodeData.step2, "step2"); // 近义词
        parseStep(nodeData.step3, "step3"); // 反义词
        parseStep(nodeData.step4, "step4"); // 形近词

        // Layout Step Nodes
        // Spread them horizontally at the bottom
        const count = stepNodesData.length;
        if (count > 0) {
            // Calculate width needed. 
            // If many nodes, we might need multiple rows or a curve.
            // For now, simple horizontal spread.
            const gap = 120;
            const totalWidth = (count - 1) * gap;
            const startX = centerX - totalWidth / 2;

            stepNodesData.forEach((n, i) => {
                const nodeId = `step-${n.id}`;
                // If too many, maybe wrap to second line
                const row = Math.floor(i / 10);
                const col = i % 10;
                // Recalculate X for wrapped rows
                const rowWidth = (Math.min(count - row*10, 10) - 1) * gap;
                const rowStartX = centerX - rowWidth / 2;
                
                nodes.push({
                    id: nodeId,
                    label: n.label,
                    type: "step",
                    x: rowStartX + col * gap,
                    y: centerY + 150 + row * 60,
                    realId: n.id,
                    stepType: n.type
                });
                links.push({ source: "center", target: nodeId });
            });
        }

        this.renderD3(nodes, links);
        this.updateDetailsPanel(this.word);
    }

    renderD3(nodes, links) {
        // Clear previous
        this.svg.selectAll("*").remove();

        // Arrow marker
        this.svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 20)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#999");

        // Links (Lines)
        // Note: D3 force layout expects source/target to be objects or indices, 
        // but here we are using fixed positions, so we can draw lines directly.
        // However, to get nice curves, we can use d3.linkVertical or similar.
        
        // Since we have explicit x/y, we can just draw lines.
        const linkSelection = this.svg.selectAll(".link")
            .data(links)
            .enter().append("path")
            .attr("class", "link")
            .attr("d", d => {
                const source = nodes.find(n => n.id === d.source);
                const target = nodes.find(n => n.id === d.target);
                if (!source || !target) return "";
                
                // Simple straight line or Bezier?
                // Let's use a cubic bezier for smoother look (Vertical Mindmap style)
                return d3.linkVertical()
                    .x(d => d.x)
                    .y(d => d.y)
                    ({source: source, target: target});
            });

        // Nodes (Groups)
        const nodeSelection = this.svg.selectAll(".node")
            .data(nodes)
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.x},${d.y})`)
            .on("click", (event, d) => {
                this.handleNodeClick(d);
            });

        // Circles/Rects
        nodeSelection.each(function(d) {
            const el = d3.select(this);
            if (d.type === 'center') {
                el.append("rect")
                    .attr("x", -50).attr("y", -25)
                    .attr("width", 100).attr("height", 50)
                    .attr("rx", 10).attr("ry", 10)
                    .style("fill", "#ff9800");
            } else if (d.type === 'root') {
                 el.append("circle")
                    .attr("r", 30)
                    .style("fill", "#4caf50");
            } else {
                 el.append("rect")
                    .attr("x", -40).attr("y", -20)
                    .attr("width", 80).attr("height", 40)
                    .attr("rx", 20).attr("ry", 20)
                    .style("fill", "#2196f3");
            }
        });

        // Labels
        nodeSelection.append("text")
            .attr("dy", ".35em")
            .text(d => d.label)
            .style("fill", "white")
            .style("font-weight", "bold");
            
    }

    handleNodeClick(d) {
        if (d.realId) {
            this.word = d.label;
            this.word_num = d.realId;
            // Update input box
            if (this.wordsInput) this.wordsInput.value = this.word;
            // Re-render
            this.illustrateGraph();
        }
    }

    async updateDetailsPanel(word) {
        this.detailsContent.innerHTML = `
            <h4>${word}</h4>
            <p class="text-muted">ID: ${this.word_num}</p>
            <div class="loading">正在加载详情...</div>
        `;

        try {
            const response = await fetch(`/api/pathbuilder/word/${this.word_num}`);
            const result = await response.json();

            if (result.success && result.data && result.data.length > 0) {
                let html = `<h4>${word}</h4><p class="text-muted">ID: ${this.word_num}</p>`;
                
                result.data.forEach((detail, index) => {
                    html += `
                        <div class="detail-item" style="margin-top: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
                            <div><span class="badge badge-info" style="background:#17a2b8; color:white; padding:2px 5px; border-radius:3px;">${detail.Level || '-'}</span> 
                                 <span class="text-primary" style="font-weight:bold; margin-left:5px;">${detail.part_of_speech || '-'}</span></div>
                            <div style="margin-top: 5px;"><strong>释义：</strong>${detail.ExplainationC || '-'}</div>
                            <div style="margin-top: 5px; color: #666;"><strong>English:</strong> ${detail.ExplainationE || '-'}</div>
                            ${detail.Addition && detail.Addition !== '-' ? `<div style="margin-top: 5px; font-size: 0.9em; color: #888;">变形: ${detail.Addition}</div>` : ''}
                        </div>
                    `;
                });
                
                this.detailsContent.innerHTML = html;
            } else {
                this.detailsContent.innerHTML = `
                    <h4>${word}</h4>
                    <p>ID: ${this.word_num}</p>
                    <p>暂无详细信息</p>
                `;
            }
        } catch (error) {
            console.error('Error loading details:', error);
            this.detailsContent.innerHTML = `
                <h4>${word}</h4>
                <p>ID: ${this.word_num}</p>
                <p class="text-danger">加载详情失败</p>
            `;
        }
    }
}

// 初始化应用
document.addEventListener('DOMContentLoaded', async () => {
    const app = new PathBuilder();
    app.initPathBuilder();
});
