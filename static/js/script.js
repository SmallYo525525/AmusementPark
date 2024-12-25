$(document).ready(function(){

    $('#EnterPark').on('click', function(){
        var userId = $('#name').val();  // 獲取輸入的 ID

        if (userId.trim() === '') {
            alert('請輸入 ID');
            return;
        }

        // 發送 AJAX 請求
        $.ajax({
            url: '/ajax/enter_park',
            type: 'POST',
            data: { name: userId },
            success: function(response){
                // 假設後端成功返回，並且會有 "status" 字段表示成功
                if (response.status === 'success') {
                    // 顯示 ID 並隱藏輸入框
                    $('#userId').text(userId);  // 顯示 ID
                    $('#name').hide();  // 隱藏 ID 輸入框
                    $('#welcome').hide();
                    $('#id').hide();
                    $('#EnterPark').hide();
                    $('#LeavePark').show();
                    $('#userIdDisplay').show();   // 顯示 ID 顯示區塊
                    $('#recharge').css('visibility','visible');

                    // 更新餘額顯示
                    $('#balance').text('NT$ ' + response.balance);
                    // 更新交易紀錄
                    var records = response.records;
                    var recordsList = $('#transactionHistory');  // 假設這是你用來顯示交易紀錄的容器
                    recordsList.empty();  // 清空現有的交易紀錄

                    if (records.length > 0) {
                        records.forEach(function(record) {
                            recordsList.append('<a href="#" class="list-group-item list-group-item-action">' + record + '</a>');
                        });
                    } else {
                        recordsList.append('<a href="#" class="list-group-item list-group-item-action">----</a>');
                    }

                } else {
                    alert('入園失敗，請再試一次');
                }
            },
            error: function(xhr, status, error){
                alert('發生錯誤，請稍後再試');
            }
        });
    });

    $('#LeavePark').on('click', function() {
        $.ajax({
            url: '/ajax/leave_park',
            type: 'POST',
            success: function(response) {
                if (response.status === 'success') {
                    // 清除畫面上的 ID 和顯示重新登入的內容
                    $('#name').show();
                    $('#EnterPark').show();
                    $('#LeavePark').hide();
                    $('#userIdDisplay').hide();
                    $('#welcome').show();
                    $('#id').show();
                    $('#recharge').css('visibility','hidden');
                    // 更新餘額顯示
                    $('#balance').text('----');
                }
            },
            error: function(xhr, status, error) {
                alert('發生錯誤，請稍後再試');
            }
        });
    });

})