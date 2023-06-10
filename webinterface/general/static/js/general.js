let table = $('#general_blockedProfilesTWs').DataTable({
    ajax: '/general/blockedProfileTWs',
    "bDestroy": true,
    ordering: false,
    searching: false,
    "paging": false,
    "bInfo": false,
    columns: [{ data: 'blocked' }]
});

function ResponsiveNavbar(){
	var tabsNewAnim = $('#navbarSupportedContent');
	var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
	var activeItemNewAnim = tabsNewAnim.find('.active');
	var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
	var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
	var itemPosNewAnimTop = activeItemNewAnim.position();
	var itemPosNewAnimLeft = activeItemNewAnim.position();
	$(".hori-selector").css({
		"top":itemPosNewAnimTop.top + "px", 
		"left":itemPosNewAnimLeft.left + "px",
		"height": activeWidthNewAnimHeight + "px",
		"width": activeWidthNewAnimWidth + "px"
	});
	$("#navbarSupportedContent").on("click","li",function(e){
		$('#navbarSupportedContent ul li').removeClass("active");
		$(this).addClass('active');
		var activeWidthNewAnimHeight = $(this).innerHeight();
		var activeWidthNewAnimWidth = $(this).innerWidth();
		var itemPosNewAnimTop = $(this).position();
		var itemPosNewAnimLeft = $(this).position();
		$(".hori-selector").css({
			"top":itemPosNewAnimTop.top + "px", 
			"left":itemPosNewAnimLeft.left + "px",
			"height": activeWidthNewAnimHeight + "px",
			"width": activeWidthNewAnimWidth + "px"
		});
	});
}
$(document).ready(function(){
	setTimeout(function(){ ResponsiveNavbar(); });
});
$(window).on('resize', function(){
	setTimeout(function(){ ResponsiveNavbar(); }, 500);
});
$(".navbar-toggler").click(function(){
	$(".navbar-collapse").slideToggle(300);
	setTimeout(function(){ ResponsiveNavbar(); });
});


jQuery(document).ready(function($){
	var path = window.location.pathname.split("/").pop();
	if ( path == '' ) {
		path = 'index.html';
	}
	var target = $('#navbarSupportedContent ul li a[href="'+path+'"]');
	target.parent().addClass('active');
});
