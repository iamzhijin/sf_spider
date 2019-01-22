function deleteCrawData(){
    var selEntName = $('#monitor-list-table').bootstrapTable('getSelections');
    var url = "./deleteCrawDataInfo";

    $.ajax({
               type: "POST",
               cache:false,
               async : true,
               dataType : "html",
               url:  url,
               data: {sel_entName:selEntName},
               success: function(){
                    $('#monitor-list-table').bootstrapTable('refresh');
               }
    });

};


