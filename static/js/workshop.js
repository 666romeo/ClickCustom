$('.content_header_menu a').on('click',function(){
  let targetBlock = $(this).data('cabinet_content');
  console.log(targetBlock);
  $('.'+targetBlock).show().siblings('.hide').hide();
});