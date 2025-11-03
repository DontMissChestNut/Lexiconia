document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const messageDiv = document.getElementById('message');
    
    // 清除错误信息
    function clearErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.textContent = '';
        });
    }
    
    // 显示错误信息
    function showError(fieldId, message) {
        const errorElement = document.getElementById(fieldId + 'Error');
        errorElement.textContent = message;
    }
    
    // 验证表单
    function validateForm(formData) {
        let isValid = true;
        clearErrors();
        
        // 验证用户名
        if (formData.get('username').length < 3) {
            showError('username', '用户名至少需要3个字符');
            isValid = false;
        }
        
        // 验证邮箱
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.get('email'))) {
            showError('email', '请输入有效的邮箱地址');
            isValid = false;
        }
        
        // 验证密码
        if (formData.get('password').length < 6) {
            showError('password', '密码至少需要6个字符');
            isValid = false;
        }
        
        // 验证确认密码
        if (formData.get('password') !== formData.get('confirmPassword')) {
            showError('confirmPassword', '两次输入的密码不一致');
            isValid = false;
        }
        
        return isValid;
    }
    
    // 处理表单提交
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        
        if (validateForm(formData)) {
            // 发送数据到后端
            fetch('/register', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())                  // 解析JSON响应
            .then(data => {
                if (data.success) {
                    // 注册成功处理
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'message success';
                    form.reset();   // 清空表单
                } else {
                    // 注册失败处理
                    messageDiv.textContent = data.message;
                    messageDiv.className = 'message error';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageDiv.textContent = '注册过程中发生错误，请稍后重试';
                messageDiv.className = 'message error';
            });
        }
    });
    
    // 实时验证输入
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            const formData = new FormData(form);
            validateForm(formData);
        });
    });
});