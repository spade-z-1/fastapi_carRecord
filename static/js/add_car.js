function add_car() {

    var carno = $("#carno").eq(0).val();
    var owner = $("#owner").eq(0).val();
    var brand = $("#brand").eq(0).val();


    var data = {
        "carno": carno,
        "owner": owner,
        "brand": brand
    };

    $.ajax({

        headers: {'Content-Type': 'application/json;charset=UTF-8'},
        url: "http://127.0.0.1:8000/api/create_car/",
        type: "Post",
        data: JSON.stringify(data),
        dataType: 'json',
        success: function (json) {
            alert("车辆信息已添加,车辆信息id=" + json["id"]);
        },
        error: function (e, json) {
            alert("车辆信息已存在,请在后面查询");
            console.log("error");
            //错误信息
            console.log(e);
        }
    });

}