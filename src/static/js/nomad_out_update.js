//--------------------------------------
// イベント
//--------------------------------------
// $('#id_local_total').change(function () {
//   console.log('id_local_total');
//   calcTotal();
// });
// $('#id_rate').change(function () {
//   console.log('id_rate');
//   calcTotal();
// });
// $('#id_total').change(function () {
//   console.log('id_total');
//   calcRate();
// });

$('#id_net').change(function () {
  calcTotalFromNet();
});
$('#id_total').change(function () {
  calcNetFromTotal();
});
$('#id_tax_rate').change(function () {
  calcNetFromTotal();
});

//--------------------------------------
// VAT計算
//--------------------------------------
function calcTotalFromNet() {
  var net       = parseFloat($('#id_net').val());
  var tax_rate  = parseInt($('#id_tax_rate').val());
  var vat = net * tax_rate/100;
  var total = net + vat;
  $('#id_total').val(total.toFixed(2))
  setVatValue(tax_rate, vat);
}
function calcNetFromTotal() {
  var total     = parseFloat($('#id_total').val());
  var tax_rate  = parseInt($('#id_tax_rate').val());
  var net = total / (1 + tax_rate/100);
  var vat = total - net;
  $('#id_net').val(net.toFixed(2));
  setVatValue(tax_rate, vat);
}
function setVatValue(tax_rate, vat) {
  $('#id_vat').val(vat.toFixed(2));
  if (tax_rate == 21) {
    $('#id_vat9').val(0);
    $('#id_vat21').val(vat.toFixed(2));
  }
  if (tax_rate == 9)  {
    $('#id_vat9').val(vat.toFixed(2));
    $('#id_vat21').val(0);
  }
  if (tax_rate == 0)  {
    $('#id_vat9').val(0);
    $('#id_vat21').val(0);
  }
}

//--------------------------------------
// レート計算
//--------------------------------------
// function calcRate() {
//   var local_total = $('#id_local_total').val();
//   var total       = $('#id_total').val();

//   if (local_total > 0 && total > 0) {
//     var rate = local_total / total;
//     $('#id_rate').val(rate);
//   }
// }
// function calcTotal() {
//   var local_total = $('#id_local_total').val();
//   var rate        = $('#id_rate').val();

//   if (local_total > 0 && rate > 0) {
//     var total = local_total * rate;
//     $('#id_total').val(total);
//   }
// }

//--------------------------------------
// drag & drop
//--------------------------------------
var dragDropArea = document.getElementById('dragDropArea');
var fileInput    = document.getElementById('id_reciept');
dragDropArea.addEventListener('dragover', function(evt){
  evt.preventDefault();
  dragDropArea.classList.add('dragover');
});
dragDropArea.addEventListener('dragleave', function(evt){
    evt.preventDefault();
    dragDropArea.classList.remove('dragover');
});
dragDropArea.addEventListener('drop', function(evt){
    evt.preventDefault();
    dragDropArea.classList.remove('dragenter');
    var files = evt.dataTransfer.files;
    console.log("DRAG & DROP");
    console.table(files);
    fileInput.files = files;
    preview('onChenge',files[0]);
});

function preview(event, f = null) {
  var file = f;
  if(file === null){
    file = event.target.files[0];
  }
  console.log('file', file);

  var reader = new FileReader();
  reader.onload = function(ev) {
    console.log('reader.result');
    $('#previewImage').attr("src", ev.target.result);
    $('#dragDropArea').hide();
    $('#previewArea').show();
  };
  reader.readAsDataURL(file);
}
// function preview(event, f = null) {
//   var file = f;
//   if(file === null){
//     file = event.target.files[0];
//   }
//   console.log('file', file);

//   var image = new Image();
//   var reader = new FileReader();
//   var iframe = $('#previewImage');
//   reader.onload = function(ev) {
//     image.src = reader.result;
//     image.onload = function() {
//       result = {width: image.naturalWidth, height: image.naturalHeight};
//       console.log(result);
//       console.log('iframe.width:', iframe.width());
//       var ratio = iframe.width() / image.naturalWidth;
//       console.log('Ratio:', ratio);
//       iframe
//         .css('-ms-transform',     `scale(${ratio})`)
//         .css('-moz-transform',    `scale(${ratio})`)
//         .css('-o-transform',      `scale(${ratio})`)
//         .css('-webkit-transform', `scale(${ratio})`)
//         .css('transform',         `scale(${ratio})`)
//         .css('-ms-transform-origin',     '0 0')
//         .css('-moz-transform-origin',    '0 0')
//         .css('-o-transform-origin',      '0 0')
//         .css('-webkit-transform-origin', '0 0')
//         .css('transform-origin',         '0 0');
//     } 
//     iframe.attr("src", ev.target.result);
//     $('#dragDropArea').hide();
//     $('#previewArea').show();
//   };
//   reader.readAsDataURL(file);
// }

function removeImage()
{
  console.log('removeImage');
  $('#previewImage').attr("src", null);
  $('#dragDropArea').show();
  $('#previewArea').hide();
  $('#id_reciept').val(null);
}
