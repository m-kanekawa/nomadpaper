//--------------------------------------
// ロード時
//--------------------------------------
$(function () {
  calcLine();
});

function submit() {
  document.form.submit();
}

//--------------------------------------
// イベント
//--------------------------------------
//本文入力時の処理
$(document).on('keyup', '[id$="_price"], [id$="_quantity"]', function () {
  calcLine();
});
$(document).on('change', '[id$="_tax_rate"]', function () {
  calcLine();
});

// function setInitDate(){
//   const today    = new Date();
//   const endmonth = new Date(today.getFullYear(), today.getMonth()+1, 0);

//   if($('#id_date').val() == ''){
//     $('#id_date').val(today.toLocaleDateString('sv-SE'));
//   }
//   if($('#id_paydue').val() == ''){
//     $('#id_paydue').val(endmonth.toLocaleDateString('sv-SE'));
//   }
// }

//--------------------------------------
// 行追加処理
//--------------------------------------
function addLine() {
  var table = document.getElementById('items');
  var cnt = document.getElementById('item_cnt');
  var raw = table.rows.length - 3;
  var no = raw;
  var tr = table.insertRow(raw);
  var td1 = createColNo(no);
  var td_show = createColTitle(no);
  var td3 = createColPrice(no);
  var td4 = createColQuantity(no);
  var td5 = createColTotal(no);
  var td6 = createColRate(no);
  tr.appendChild(td1);
  tr.appendChild(td_show);
  tr.appendChild(td3);
  tr.appendChild(td4);
  tr.appendChild(td5);
  tr.appendChild(td6);
  cnt.value = parseInt(cnt.value) + 1;
  console.log('item_cnt', cnt.value);
}
function createColNo(no) {
  var td = document.createElement('td');
  td.innerHTML = no;
  return td;
}
function createColTitle(no) {
  var idTxt = 'line_' + no + '_title';
  var textarea = document.createElement('textarea');
  textarea.setAttribute('id', idTxt);
  textarea.setAttribute('name', idTxt);
  textarea.innerText = '';
  textarea.className = 'form-control form-control-sm';

  var td = document.createElement('td');
  td.className = 'border';
  td.appendChild(textarea);
  return td;
}
function createInputItem(no, id_post, label, disabled) {
  if(disabled){
    var idTxt = 'line_' + no + id_post;
    var input = document.createElement('input');
    input.setAttribute('id', idTxt);
    input.setAttribute('name', idTxt);
    input.setAttribute('type', 'hidden');
    input.value = '';

    var idTxt_show = 'line_' + no + id_post + '_show';
    var input_show = document.createElement('input');
    input_show.setAttribute('id', idTxt_show);
    input_show.setAttribute('type', 'text');
    input_show.value = '';
    input_show.disabled = disabled;
    input_show.className = 'form-control form-control-sm text-end';
  }
  else{
    var idTxt = 'line_' + no + id_post;
    var input = document.createElement('input');
    input.setAttribute('id', idTxt);
    input.setAttribute('name', idTxt);
    input.setAttribute('type', 'text');
    input.value = '';
    input.className = 'form-control form-control-sm text-end';
  }
  var span = document.createElement('span');
  span.className = 'input-group-text';
  span.innerHTML = label;

  var div = document.createElement('div');
  div.className = 'input-group';
  div.appendChild(span);
  div.appendChild(input);
  if(disabled)
    div.appendChild(input_show);


  var td = document.createElement('td');
  td.className = 'border';
  td.appendChild(div);
  return td;
}
function createColPrice(no) {
  return createInputItem(no, '_price', currency_display, false)
}
function createColQuantity(no) {
  return createInputItem(no, '_quantity', 'x', false)
}
function createColTotal(no) {
  return createInputItem(no, '_total', currency_display, true)
}
function createColRate(no) {
  var td = document.createElement('td');
  var sel = document.createElement('select');
  var idTxt = 'line_' + no + '_tax_rate';

  for (let i in tax_rates) {
    let op = document.createElement('option');
    op.value = tax_rates[i]['value'];
    op.text = tax_rates[i]['label'];
    sel.appendChild(op);
  }
  sel.setAttribute('id', idTxt);
  sel.setAttribute('name', idTxt);
  sel.className = 'form-select';
  td.className = 'border';
  td.appendChild(sel);
  return td;
}

//--------------------------------------
// 合計値計算
//--------------------------------------
function calcLine() {
  console.log('calcLine');
  var net   = 0;
  var vat   = 0;
  var vat9  = 0;
  var vat21 = 0;
  var net0  = 0;
  var net9  = 0;
  var net21 = 0;

  for (var i = 1; i <= $('#item_cnt').val(); i++) {
    var idPrice      = '#line_' + i + '_price';
    var idQuantity   = '#line_' + i + '_quantity';
    var idTotal      = '#line_' + i + '_total';
    var idTotal_show = '#line_' + i + '_total_show';
    var idTaxRate    = '#line_' + i + '_tax_rate';
    var price    = $(idPrice).val();
    var quantity = $(idQuantity).val();
    var taxRate  = $(idTaxRate).val();
    var line_total = price * quantity;
    console.log('taxRate', taxRate);

    if (line_total > 0) {
      if (taxRate == 0) {
        net0 += line_total
      }
      if (taxRate == 9) {
        net9 += line_total
        vat9 += line_total * (taxRate / 100);
      }
      if (taxRate == 21) {
        net21 += line_total
        vat21 += line_total * (taxRate / 100);
      }
      net += line_total;
      vat += line_total * (taxRate / 100);
      $(idTotal).val(line_total);
      $(idTotal_show).val(line_total.toFixed(digit));
    }
  }
  var total = net + vat;

  $('#in_net_show').html(currency_display + net.toFixed(digit));
  $('#in_vat_show').html(currency_display + vat.toFixed(digit));
  $('#in_total_show').html(currency_display + total.toFixed(digit));
  $('#in_net').val(net);
  $('#in_net0').val(net0);
  $('#in_net9').val(net9);
  $('#in_net21').val(net21);
  $('#in_vat').val(vat);
  $('#in_vat9').val(vat9);
  $('#in_vat21').val(vat21);
  $('#in_total').val(total);
}
