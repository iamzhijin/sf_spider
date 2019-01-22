function test() {
    var web_name = $('input[name="web_name"]').val();
    var web_site = $('input[name="web_site"]').val();
    var request_function = $('input:radio[name="request_function"]:checked').val();
    var request_body = $('textarea[name="request_body"]').val();
    var response_type = $('input:radio[name="response_type"]:checked').val();
    var xpath_str = $('input[name="xpath_str"]').val();
    var re_str = $('input[name="re_str"]').val();
    var keyword = $('input[name="keyword"]').val();
    var per_num = $('input[name="per_num"]').val();

    data={
        web_name:web_name,
        web_site:web_site,
        request_function:request_function,
        request_body:request_body,
        response_type:response_type,
        xpath_str:xpath_str,
        re_str:re_str,
        keyword:keyword,
        per_num:per_num
    };
    var url = "./test_web_monitor_task";
    $.ajax({
           type: "POST",
           cache:false,
           async : true,
           // tranditional:true,
           // dataType : "html",
           url:  url,
           // data: {webMonitorInfo_list:JSON.stringify(webMonitorInfo_list)},
           data:data,
           success: function(dic) {
                 alert("数据：" + dic.num );
           }})
}