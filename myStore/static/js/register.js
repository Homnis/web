$(function(){
	$(".tabFormBtn li").on("click",function(){
		var index=$(this).index();
		//console.log(index);
		$(".tabFormBtn div").css("display","none");
		$(".tabFormBtn div").eq(index).css("display","block");
		$(".wrapformbox").animate({"left":-index*600});	
	});
	
});
//更换验证码
function change(){
	$(".codepic").attr("src","http://www.gjw.com/ajax/verifycode.htm?t=" + new Date());
}
//表单验证
$(document).ready(function() {
		$(".formbox1").validate({
			onfocusout: function(element) { 
				$(element).valid(); 
			},
			rules:{
				phone:{
					required: true,
//					isMobile : true,//自定义验证手机号规则
					minlength : 11
				},
				passwordA:{
					 required: true,
					 minlength : 6,
					 maxlength : 20
				},
				passwordA2:{
					 required: true,
					 equalTo: "#passwordA"
				},
				number:{
					 required: true
				}		
			},
			messages : {
				phone : {
					required : "请输入手机号",
					minlength : "确认手机不能小于11个字符",
//					isMobile : "请正确填写您的手机号码"
				},
				passwordA:{
					required : "请输入密码"
				},
				passwordA2:{
					required: "请输入确认密码",
					equalTo: "请输入相同的密码"
				},
				number:{
					required: "请输入校检码"
				}
			}
		});
		$(".formbox2").validate({
			onfocusout: function(element) { 
				$(element).valid(); 
			},
			rules:{
				passwordB:{
					 required: true,
					 minlength : 6,
					 maxlength : 20
				},
				passwordB2:{
					 required: true,//必填
					 equalTo: "#passwordB"
				},
				email:{
					required:true
				}
			},
			messages : {
				email : {
					required : "请输入邮箱"
				},
				passwordB:{
					required : "请输入密码"
				},
				passwordB2:{
					required: "请输入确认密码",
					equalTo: "请输入相同的密码"
				}
			}
		});
		$.extend($.validator.messages, {
    		required: "请输入"
    	});
    	
  		// input.error { border: 1px solid red; }
		// label.error {display: inline-block; margin-top: -3px; margin-right: 3px; width: 14px; height: 12px; vertical-align: middle; background: url(../img/loginIcon.gif) no-repeat -16px -22px;}
	});
