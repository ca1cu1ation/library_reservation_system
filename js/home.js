// 获取座位数据
async function loadSeats() {
    const response = await fetch('http://localhost:3000/api/seats');
    const seats = await response.json();
    document.querySelectorAll('.seat-list').forEach(element => {
        element.innerHTML='';
    });
    renderSeats(seats);
}               

// 渲染座位列表
function renderSeats(seats) {                                                
    seats.forEach(seat => {
        const seatList = document.getElementById(`${seat.区域}`);
        const seatCard = document.createElement('div');
        seatCard.className = `seat-card ${seat.状态 ? 'reserved' : 'available'}`;
        seatCard.innerHTML = `
            <h3>${seat.楼层} ${seat.区域}</h3>
            <div class="facilities">
                ${seat.has_power ? '🔌' : ''}
                ${seat.near_window ? '🪟' : ''}
            </div>
            <p>状态: ${seat.状态 ? '当前有预约' : '当前无预约'}</p>
            <button onclick="reserveSeat(${seat.座位id})">立即预约</button>                    
        `;
        seatList.appendChild(seatCard);
    });
}

// 预约座位
async function reserveSeat(seatId) {            
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;

    if (!startTime || !endTime) {
        alert('请填写完整信息');
        return;
    }

    try {
        const response = await fetch('http://localhost:3000/api/reserve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ seatId, userId,usertype, startTime, endTime })
        });
        
        const result = await response.json();
        if (result.error) throw new Error(result.error);
        
        alert('预约成功！');
        loadSeats();
        loadReservations(userId);
    } catch (err) {
        alert('预约失败: ' + err.message);
    }
}

// 加载预约记录
async function loadReservations(userId) {
    const response = await fetch(`http://localhost:3000/api/reservations/${username}&${usertype}`);
    const reservations = await response.json();
    document.querySelectorAll('.seat-list').forEach(otherHeader => {
        this.innerHTML='';
    });
    renderReservations(reservations);
}

// 渲染预约记录
function renderReservations(reservations) {
    const list = document.getElementById('reservationList');
    list.innerHTML = '';            
    if (reservations.length === 0) {
        list.innerHTML = '<p>暂无预约记录</p>';
        return;
    }

    const table = document.createElement('table');
    table.className="reservation-table";
    table.innerHTML = `
        <tr>
            <th>序号</th>
            <th>位置</th>
            <th>时间段</th>
            <th>状态</th>
            <th>操作</th>
        </tr>
    `;
    var num=1;
    reservations.forEach(res => {
        const statusClass = (res.状态 === '正在进行'?'status-started':
            (res.状态==='已结束' ? 'status-ended' :'status-unstarted'));                 
        const row = document.createElement('tr');
        row.innerHTML = `                
            <td>${num++}</td>
            <td class="location-cell">${res.楼层} ${res.区域}</td>
            <td class="time-cell">${new Date(res.起始时间).toLocaleString()} - 
                ${new Date(res.结束时间).toLocaleString()}</td>
            <td class="${statusClass}">${res.状态}</td>
            <td class="action-cell">
            ${res.状态 === '未开始' ? 
            `<button class="cancel-btn" onclick="cancelReservation('${res.预约id}')">取消预约</button>` : 
            (res.状态==='正在进行' ? `<button class="cancel-btn" onclick="cancelReservation('${res.预约id}')">提前结束</button>` :
            '不可取消')}
            </td>                
        `;
        table.appendChild(row);
    });
    
    list.appendChild(table);
}

// 取消预约功能
async function cancelReservation(reservationId) {
    if (!confirm('确定要取消该预约吗？')) return;
    try {
        const response = await fetch(`http://localhost:3000/api/cancel_reservations/${usertype}&${reservationId}`,{
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },                    
        });
        const result = await response.json();
        if (result.error) throw new Error(result.error);
            alert('取消预约成功');
            loadReservations(userId);            
    } catch (error) {
        console.error('取消预约失败:', error);
        alert('网络错误，请稍后重试');
    }
}

// 初始化
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');
const usertype = urlParams.get('usertype');
const userId = username;        
if(username==undefined)window.location.href='./index.html';
else {
    usernameElement = document.getElementById('username');
    usernameElement.innerText=`${username}`;    
}

//楼层按钮添加展开事件
document.querySelectorAll('.floor-header').forEach(header => {
    header.addEventListener('click',function(){
    // 切换激活状态
    this.classList.toggle('active');                
    // 获取对应的容器
    const container = this.nextElementSibling;                
    // 计算总高度（包含所有子元素）
    if (container.style.maxHeight) {
        container.style.maxHeight = null;
    } else {
        // 计算所有子元素的总高度
        let totalHeight = 0;
        Array.from(container.children).forEach(child => {
            totalHeight += child.offsetHeight + 10;
        });
        container.style.maxHeight = totalHeight + "px";
    }
    // 关闭其他元素
    document.querySelectorAll('.floor-header').forEach(otherHeader => {
        if (otherHeader !== this) {
            otherHeader.classList.remove('active');
            const otherContainer = otherHeader.nextElementSibling;
            otherContainer.style.maxHeight = null;
        }
    });
});
});

// 加载用户信息    
function showEditForm() {
    const dropdown = document.getElementById('userDropdown');
    dropdown.innerHTML = `
        <h3>修改信息</h3>
        <form id="userEditForm" onsubmit="submitEdit(event)">
            <span>用户名:</span>
            <span id="editName"></span>
            <br>
            <span>用户类型:</span>
            <span id="editType"></span>
            <input type="tel" id="editPassword" placeholder="密码">
            <button type="submit">保存修改</button>
            <button type="button" onclick="cancelEdit()">取消</button>
        </form>
    `;
    
    // 填充现有数据
    fetch(`http://localhost:3000/api/user/${usertype}&${userId}`)
        .then(response => response.json())
        .then(user => {
            document.getElementById('editName').innerText = username;
            document.getElementById('editType').innerText = usertype;            
            document.getElementById('editPassword').value = user.password || '';
        });
}

//更新用户信息
async function submitEdit(event) {
    event.preventDefault();
    const password=document.getElementById('editPassword').value;
    try{
        const response = await fetch(`http://localhost:3000/api/user/${usertype}&${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({password})
        })
        const result = await response.json();
        if (result.error) throw new Error(result.error);
            alert('更新成功');
    }catch (error) {
        alert(error);
    }
}

function toggleUserMenu() {
    document.getElementById('userDropdown').classList.toggle('show');
}

// 点击外部关闭菜单
function cancelEdit() {
    // 重新加载原始用户信息并关闭编辑表单
    const dropdown = document.getElementById('userDropdown');
    dropdown.innerHTML = `<button onclick="showEditForm()">修改信息</button>`;
}

loadSeats();
loadReservations(userId);
// 每分钟刷新
setInterval(() => loadSeats(), 60000); 
setInterval(() => loadReservations(userId), 60000);