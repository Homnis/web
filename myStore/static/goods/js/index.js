$(function(){
	//index
	//topconleft下拉
	$(".topleft").mousemove(function(){
		$(".topleft").css({"background":"#fff","color":"#c40000"});
		$(".hoverQrCode").slideDown().mouseleave(function(){
			$(this).slideUp();
			$(".topleft").css({"background":"#f7f7f7","color":"#656565"});
		});
	});
	//topconleft下拉
	//noticeBar广告关闭
	$("#noticeBar span").on("click",function(){
		$("#noticeBar").css("display","none");
	});
	//noticeBar广告关闭
	//navBar_subNav的下拉导航菜单
	$(".navbar li,.navBar_subNav").hover(
		function(){
			var $index=$(this).index();
			
			$(".navBar_subNav").eq($index).show();
		},
		function(){
			$(".navBar_subNav").hide();
		}
	);
	//end
	//商品倒计时
	var twoDaysFromNow = new Date().valueOf() + 2 * 24 * 60 * 60 * 1000;
	$('.clock').countdown(twoDaysFromNow, function(event) {
	  var totalHours = event.offset.totalDays * 24 + event.offset.hours;
	  $(this).html(event.strftime(totalHours + ' 时 %M 分 %S 秒'));
	});
	//商品倒计时 end
	//banner轮播图
	var 
		order=0,
		oTimer=null;
	autoPlay();
	function autoPlay(){
		oTimer=setInterval(function(){
			order++;
			if(order==$(".focusBox > li").length){
				order=0;
			}
			show(order);
		},6000);
	}
	function show(order){
		$(".focusBox > li").stop(true).fadeOut(600);
		$(".num > span").removeClass("active");
		$(".num > span").eq(order).addClass("active");
		$(".focusBox > li").eq(order).stop(true).fadeIn(600);
	}
	$(".num > span").on("mouseenter",function(){
		show($(this).index());
		order=$(this).index();
	});
	$(".focusBox > li").hover(
		function(){
			clearInterval(oTimer);
		},
		function(){
			autoPlay();
		}
	);
	//banner轮播图 end

	//顶部广告图
	var isFlag = true;
	$(".focusPic_close").on("click",function(){
		if(isFlag) {
			$("#focusPic img").attr("src","img/adtop.jpg").css({"top":0});
			$("#focusPic").animate({"height":270},1000);
			$(".focusPic_close").text("收起");
			isFlag = false;
		} else {
			$("#focusPic img").attr("src","img/indextop.jpg");
			$("#focusPic").animate({"height":80});
			$(".focusPic_close").text("展开");
			isFlag = true;
		}
		
	});
	//顶部广告图 end
	//底部动画
	$(".floor6pic img").hover(
		function(){
			$(this).stop(true).animate({"left":-156});
		},
		function(){
			$(this).stop(true).animate({"left":0});
		}
	);
	//底部动画 end
	//
	// function playImg(container, pagination, next, prev) {
	//  	var swiper = new Swiper(container, {
 //        pagination: pagination,
 //        nextButton: next,
 //        prevButton: prev,
 //        slidesPerView: 1,
 //        paginationClickable: true,
 //        spaceBetween: 0,
 //        loop: true,
 //        autoplay: 3000,//可选选项，自动滑动
 //        autoplayDisableOnInteraction : false//设置为false，用户操作swiper之后自动切换不会停止，每次都会重新启动autoplay。
 //    	});
	// }
	 // playImg(".swiper-container", ".swiper-pagination", ".swiper-button-next", ".swiper-button-prev");
	// //main 轮播图 end

	// $(".swiper-container").each(function(obj) {
	// 	var swiper = new Swiper($(obj), 
	// 	{
	//         pagination: $(obj).children().find(".swiper-pagination"),
	//         nextButton: $(obj).children().find('.swiper-button-next'),
	//         prevButton: $(obj).children().find('.swiper-button-prev'),
	//         slidesPerView: 1,
	//         paginationClickable: true,
	//         spaceBetween: 0,
	//         loop: true,
	//         autoplay: 3000//可选选项，自动滑动
 //    	});
	// });
	 //main 轮播图
	 var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween:0,
        loop: true,
        autoplay: 5000,
        autoplayDisableOnInteraction : false
    });
	//main 轮播图 end 
	 //slidelist轮播图的按钮显示与隐藏
	 //.slideAdleft,.slideAdright
	 $(".slidelist, .slideAdright, .slideAdleft").hover(
	 	function(){
	 		// $(".slideAdleft").css("display","block");
	 		// $(".slideAdright").css("display","block");
	 		$(".slideAdleft").stop(true).show();
	 		$(".slideAdright").stop(true).show();
	 	},
	 	function(){
	 		//$(".slideAdleft").css("display","none");
	 		//$(".slideAdright").css("display","none");
	 		$(".slideAdleft").stop(true).hide();
	 		$(".slideAdright").stop(true).hide();
	 	}
	 );

	 //end

	 //楼层选项卡
	 $(".tabitembox .lia").each(function(){
	 	$(this).mouseenter(function(){
	 		var i=$(this).index();
		 	$(".tabitembox .lia > a").removeClass("active");
		 	$(this).children().addClass("active");
		 	$(".tabitembox span").removeClass("act");
		 	$(this).children().find("span").addClass("act");
		 	$(".tabslide_right > div[class^=tabslide]").css("display","none");
		 	$(".tabslide_right > div").eq(i).css("display","block");

	 	});
	 });

	 
	 //index 吸顶
	 $(window).scroll(function(){
	 	if($(document).scrollTop()>400){
	 		//$("#fixedBox").slideDown(70);
	 		$("#fixedBox").stop(true).animate({"top":0},100);
	 	}else{
	 		//$("#fixedBox").slideUp(70);
	 		$("#fixedBox").stop(true).animate({"top":-100},100);
	 	}
	 });

	 //index 搜索
	 $(".searchBtn").on("click",function(){
	 	if($(".search").val()=="洋河"){
			window.open('html/search_yanghe.html'); 
		}
	 });
	//index 搜索 跨域
	$(".search").focus(function(){
		$("#searchBtnlist").css({"display":"block;"});
	});
	$(".search").blur(function(){
		$("#searchBtnlist").css({"display":"none;"});
	});
	
	$(".search").on("keyup",function(){
		$("#searchBtnlist").html("");
		if($("#sea").val()==""){
				$("#searchBtnlist").css({"display":"none;"});
		}
		console.log($("#sea").val());

		//  $.ajax(  
	 //    {  
	 //        type:'getJSON',  
	 //        url : 'http://www.gjw.com/ajax/SearchKey.aspx?q='+$(".search").val() + "&cb=?",  
	 //        dataType : 'jsonp',  
	 //        jsonp:"jsoncallback",  
	 //        success  : function(data) {  
	 //            console.log(typeof data); 
	 //           // $("#searchBtnlist li") 
	 //        },  
	 //        error : function() {  
	 //            console.log('fail');  
	 //        }  
	 //    }  
		// );
		//searchBtnlist
			$.getJSON(
				"https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd="+$(".search").val()+"&cb=?",
				function (data) {
					console.log(data.s);
					var $arr=data.s;
					//console.log($arr[0]);
					$.each($arr,function(n,value){
			        	//var $li=$("<li>");
			        	//$li.text()=value;
			        	//console.log(value);				
			        	$("#searchBtnlist").append("<li>"+value+"</li>");
			        });
				}
			); 
			
	});
	
	 //index 搜索 end
	 //侧边栏
	 $(".quick_links_panel li").mouseenter(function(){
		$(this).children(".mp_tooltip").animate({left:-92,queue:true});
		$(this).children(".mp_tooltip").css("visibility","visible");
		$(this).children(".ibar_login_box").css("display","block");
	});
	$(".quick_links_panel li").mouseleave(function(){
		$(this).children(".mp_tooltip").css("visibility","hidden");
		$(this).children(".mp_tooltip").animate({left:-121,queue:true});
		$(this).children(".ibar_login_box").css("display","none");
	});
	$(".quick_toggle li").mouseover(function(){
		$(this).children(".mp_qrcode").show();
	});
	$(".quick_toggle li").mouseleave(function(){
		$(this).children(".mp_qrcode").hide();
	});

	// 元素以及其他一些变量
	var eleFlyElement = document.querySelector("#flyItem"), eleShopCart = document.querySelector("#shopCart");
	var numberItem = 0;
	// 抛物线运动
	var myParabola = funParabola(eleFlyElement, eleShopCart, {
		speed: 400, //抛物线速度
		curvature: 0.0008, //控制抛物线弧度
		complete: function() {
			eleFlyElement.style.visibility = "hidden";
			eleShopCart.querySelector("span").innerHTML = ++numberItem;
		}
	});
	// 绑定点击事件
	if (eleFlyElement && eleShopCart) {
		
		[].slice.call(document.getElementsByClassName("btnCart")).forEach(function(button) {
			button.addEventListener("click", function(event) {
				// 滚动大小
				var scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft || 0,
				    scrollTop = document.documentElement.scrollTop || document.body.scrollTop || 0;
				eleFlyElement.style.left = event.clientX + scrollLeft + "px";
				eleFlyElement.style.top = event.clientY + scrollTop + "px";
				eleFlyElement.style.visibility = "visible";
				
				// 需要重定位
				myParabola.position().move();			
			});
		});
	}
	 //侧边栏 end
	 //index end
});