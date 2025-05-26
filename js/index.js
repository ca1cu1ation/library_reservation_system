function showMessage(msg) {
    alert(msg);  
}
const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const usertype = document.querySelector('input[name="usertype"]:checked').value;

    try {
        const response = await fetch('http://localhost:3000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password,usertype })
        });

        const data = await response.json();
        
        if (data.success) {
            showMessage('登录成功！正在跳转...', 'success');
            // 跳转页面
            //document.cookie = "username=${data.username}; usertype=${data.usertype}";                
            window.location.href = `./home.html?username=${data.user.username}&usertype=${data.user.usertype}`;
        } else {
            showMessage(data.message || '认证失败', 'error');
        }
    } catch (error) {
        showMessage('网络连接错误', 'error');
    }
});