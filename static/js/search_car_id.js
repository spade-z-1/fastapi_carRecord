function search_car_id() {

    var carno = $("#search_carno").eq(0).val();


    var data = {
        "carno": carno,
    };

    $.ajax({

        headers: {'Content-Type': 'application/json;charset=UTF-8'},
        url: "http://127.0.0.1:8000/api/car/carno",
        type: "get",
        data: (data),
        dataType: 'json',
        success: function (json) {
            alert("车辆信息id="+json["id"]);
        },
        error: function (e) {
             alert("没有这个车辆信息请添加");
            console.log("error");
            //错误信息
            console.log(e);
        }
    });

}