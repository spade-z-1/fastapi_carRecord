function add_car_record() {

    var car_id = $("#car_id").eq(0).val();
    var reason = $("#reason").eq(0).val();
    var punish = $("#punish").eq(0).val();
    var makedate = $("#makedate").eq(0).val();


    var data = {
        "car_id": car_id,
        "reason": reason,
        "punish": punish,
        "makedate": makedate
    };

    $.ajax({

        headers: {'Content-Type': 'application/json;charset=UTF-8'},
        url: "http://127.0.0.1:8000/api/create_record/",
        type: "Post",
        data: JSON.stringify(data),
        dataType: 'json',
        success: function () {
            alert("违章记录已添加");
        },
        error: function (e) {
            alert("没有对应的车辆信息")
            console.log("error");
            //错误信息
            console.log(e);
        }
    });

}