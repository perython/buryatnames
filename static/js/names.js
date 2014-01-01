$(function(){
	// make active selected name
	$(document).on('click', '.names-list .name', function(){
		$(this).toggleClass('selected');
	});
});