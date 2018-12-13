$(function(){
	//商品详情页面的下拉的显示和隐藏
	$(".navBar_dt_hover").hover(
		function(){
			$(".navmenu_hover").fadeIn();
		},
		function(){
			$(".navmenu_hover").fadeOut();
		}
	);
	//end
	//商品详情页面的放大镜
	 /* 鼠标移动小图，小图对应大图显示在大图上，并替换放大镜中的图*/
    // $(".specList ul li img").livequery("mouseover",function(){ 
    //     var imgSrc = $(this).attr("src");
    //     var i = imgSrc.lastIndexOf(".");
    //     var unit = imgSrc.substring(i);
    //     imgSrc = imgSrc.substring(0,i);
    //     var imgSrc_small = $(this).attr("src_D");
    //     var imgSrc_big = $(this).attr("src_H");
    //     $("#midImg").attr({"src": imgSrc_small ,"jqimg": imgSrc_big });
    //     $(this).css({"border":"2px solid #3399cc","padding":"1px"});
    // });
    
    // $(".specList ul li img").livequery("mouseout",function(){ 
    //     $(this).css({"border":"1px solid #ddd","padding":"2px"});
    // });
    
    
	$('.jqzoom').jqzoom({
            zoomType: 'standard',
            lens:true,
            preloadImages: false,
            alwaysOn:false
	
	});
	//商品详情页面的放大镜 end
	//商品详情页面的选项卡
	$(".navboxinner ul li").on("click",function(){
		var index=$(this).index();
		$(".navboxinner ul a").removeClass();
		$(".navboxinner ul a").eq(index).addClass("active");
		if(index>0){
			$(".tabnavBox").css({"border-left":"1px solid #c9c9c9"});
		}else{
			$(".tabnavBox").css({"border-left":"0"});
		}
	});
	//商品搜索页面的底部卡片效果
	console.log($(".brandBox .imgDiv"));
	console.log($(".imgtop").eq(3));

	$(".brandBox .imgDiv").hover(
		

		function(){
			var index=$(this).index();
			$(this).children(".imgtop").css({"top":0});
			$(this).children(".imgtop").stop(true).animate({"top":-56},500);
			$(this).children(".imgtop").next().css({top:56}).stop(true).animate({"top":0},500);

			// $(".imgtop").css({"top":0});
			// $(".imgtop").stop(true).animate({"top":-56},500);
			// $(".imgtop").next().css({top:56}).stop(true).animate({"top":0},500);
		},
		function(){
			var index=$(this).index();
			$(this).children(".imgtop").stop(true).animate({"top":0},500);
			$(this).children(".imgtop").next().css({top:0}).stop(true).animate({"top":56},500);
		}

	);
	//找回密码的验证
	console.log($(".fornext"));
	$(".fornext").on("click",function(){

		if($("#txtmobile").val()==18012345678){
			
			$(this).children("a").attr("href","identifyingcode.html");
		}
	});
	//验证码的倒计时
//	var twoDaysFromNow = new Date().valueOf() + 3 * 60 * 1000;
//	$('#clock').countdown(twoDaysFromNow, function(event) {
//	  var totalHours = event.offset.totalDays * 24 + event.offset.hours;
//	  $(this).html(event.strftime(' %M 分钟 %S 秒'));
//	});
	//验证码的倒计时
	//登录的验证
	$(".login_form").on("submit",function(){
		if($("#username").val()==1||$("#pwd").val()==1){
			
		}
	});
	
	//登录的验证 end 
});