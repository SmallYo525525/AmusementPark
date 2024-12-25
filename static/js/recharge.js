$(document).ready(function() {
    var selectedAmount = 0;

    // 點擊預設金額按鈕
    $('button[data-amount]').on('click', function() {
        // 先重置所有按鈕為輪廓樣式
        $('button[data-amount]').removeClass('btn-primary').addClass('btn-outline-primary');
        
        // 設定選擇的金額
        selectedAmount = $(this).data('amount');
        
        // 顯示選擇的金額在餘額區域
        // $('#balance').text('NT$ ' + selectedAmount);
        
        // 將當前選中的按鈕變為填滿顏色
        $(this).removeClass('btn-outline-primary').addClass('btn-primary');
        
        // 清除自訂金額欄位
        $('#customAmount').val('');
    });

    // 自訂金額變更
    $('#customAmount').on('input', function() {
        selectedAmount = $(this).val();  // 更新自訂金額
        selectedAmount = parseInt(selectedAmount, 10);
    });

    // 儲值按鈕點擊事件
    $('#rechargeButton').on('click', function() {
        if (selectedAmount <= 0) {
            alert('請選擇儲值金額');
            return;
        }

        // 發送儲值請求
        $.ajax({
            url: '/ajax/recharge',
            type: 'POST',
            data: { amount: selectedAmount },
            success: function(response) {
                if (response.status === 'success') {
                    // 更新餘額
                    $('#balance').text('NT$ ' + response.new_balance);
                    Swal.fire({
                        title: '儲值成功！',
                        text: '您的餘額已更新。',
                        icon: 'success',
                        confirmButtonText: '確定'
                    });
                } else {
                    Swal.fire({
                        title: '儲值失敗！',
                        text: '請稍後再試。',
                        icon: 'error',
                        confirmButtonText: '確定'
                    });
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    title: '發生錯誤',
                    text: '請稍後再試！',
                    icon: 'error',
                    confirmButtonText: '確定'
                });
            }
        });
    });
});
