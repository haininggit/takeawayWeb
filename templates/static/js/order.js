var pageIndex = 0;
var pageSize = 10;
var pageTotal = 1;
$(document).ready(function () {
    getUsername();
    search();
});
function resetPage() {
    pageIndex = 0;
}
function getUsername() {
    $.get(
        "/sell/currentUsername",
        function (data, status) {
            if (data.code == 0) {
                $("#admin").html(data.data);
            }
        }
    );
}
function search() {
    $.get(
        "/sell/buyer/order/list?nameOrId=" + $("#orderId").val() + "&pageIndex=" + pageIndex + "&pageSize=" + pageSize,
        function (data, status) {
            pageTotal = data.data[data.data.length - 1] - 1;
            if (pageTotal < 0) pageTotal = 0;
            $("#order tbody").empty();
            for (var i=0;i<data.data.length-1;i++) {
                $("#order tbody").append(insertTableRow(data.data[i]));
            }
            $("#showpage").html("第" + (pageIndex + 1) + " 页，共 " + (pageTotal + 1) + " 页");
        }
    );
}
function miss(e) {
    switch (e.innerHTML) {
        case "首页":
            pageIndex = 0;
            search();
            break;
        case "上一页":
            if (pageIndex > 0) {
                pageIndex--;
                search();
            }
            break;
        case "下一页":
            if (pageIndex < pageTotal) {
                pageIndex++;
                search();
            }
            break;
        case "尾页":
            pageIndex = pageTotal;
            search();
            break;
    }
}
function insertTableRow(data) {
    return "<tr>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.orderId + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.buyerName + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.buyerPhone + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.buyerAddress + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.orderAmount + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.orderStatus + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.payStatus + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.createTime + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.updateTime + "</td>\n" +
        "</tr>";
}