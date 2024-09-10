//--------------------------------------
// ロード時
//--------------------------------------
$(function () {
  setDisable();
});

//--------------------------------------
// イベント
//--------------------------------------
$('#id_status').change(function () {
  setDisable();
});
$('#id_rate').change(function () {
  calcTotal();
});
$('#id_total').change(function () {
  calcRate();
});

//--------------------------------------
// レート計算
//--------------------------------------
function calcRate() {
  var local_total = $('#id_local_total').val();
  var total = $('#id_total').val();

  if (local_total > 0 && total > 0) {
    var rate = local_total / total;
    $('#id_rate').val(rate.toFixed(5));
  }
}
function calcTotal() {
  var local_total = $('#id_local_total').val();
  var rate = $('#id_rate').val();

  if (local_total > 0 && rate > 0) {
    var total = local_total / rate;
    $('#id_total').val(total.toFixed(2));
  }
}


function setDisable(){
  const id_currency = $('#id_currency');
  const id_status   = $('#id_status');
  const id_date_pay = $('#id_date_pay');
  const id_rate     = $('#id_rate');
  const id_total    = $('#id_total');

  if(id_currency.val() == 1){
    id_rate.prop('disabled', true);
    id_total.prop('disabled', true);
  }
  else if(id_status.val() == 3){
    id_date_pay.prop('disabled', false);
    id_rate.prop('disabled', false);
    id_total.prop('disabled', false);
  }
  else{
    id_date_pay.prop('disabled', true);
    id_rate.prop('disabled', true);
    id_total.prop('disabled', true);
  }
}