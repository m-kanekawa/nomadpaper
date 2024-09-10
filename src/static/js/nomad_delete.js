$("[id^=btn_modal_]").on('click', function(){
  const pk     =  $(this).data('pk');
  const name   =  $(this).data('name');
  const action =  $('#form_delete').attr('action');
  const new_action = action.replace("/0/", "/" + pk + "/"); 

  console.log('action', action, new_action);
  $('#span_name').html(name);
  $('#form_delete').attr('action', new_action);
});