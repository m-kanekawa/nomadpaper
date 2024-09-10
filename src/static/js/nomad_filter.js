//--------------------------------------
// イベント
//--------------------------------------
$('#filter').on('change', function () {
  var val = $('#filter').val();
  var txt = $('#filter option:selected').text();
  console.log('filter:', val, txt);
  $('#form_filter').submit();
});
