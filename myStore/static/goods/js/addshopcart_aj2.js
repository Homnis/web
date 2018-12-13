/*========================================================,
|   ajax
|---------------------------------------------------------:
|   joinCart jquerry
`========================================================*/
//(function ($){
//    function joinCart() {
//        var $goods_id = $(this).attr("goods_id")
//        var $count = $("#txtQuantity").val()
//        $ajax({
//        url:"/shopcart/"+$count+"/add/"+$goods_id+"/",
//        type:"get",
//        success:function (msg){
//            alert(msg)
//        },
//        error:function (info){
//            alert("添加失败，请重新添加！")
//        },
//        });
//    };
//})(jQuery);

$(function () {
    $("#addcart").click(function () {
        var $goods_id = $(this).attr("goods_id")
        var $count = 1
        if ($count <= 0) {
            alert("对不起，数量不能小于0")
        }
        $.ajax({
            url: "/shopcart/"+$count+"/add/"+$goods_id+"/",
            type: "get",
            success: function (msg) {

                $sp_num = $("#sp_count").text()

                $sp_num = parseInt(msg)
                console.info(parseInt(msg))

                $("#sp_count").html($sp_num)

                alert("添加成功")
            },
            error: function (info) {
                alert("添加失败，请重新添加")
                window.location.href='/user/login/?next=/goods/'+$goods_id+'/detail/'
            },
        })
    });

});