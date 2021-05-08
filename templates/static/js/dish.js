var pageIndex = 0;
var pageSize = 10;
var pageTotal = 1;
var forUpdate = false;
$(document).ready(function () {
    getUsername();
    search();
    cancelSaveCategory();
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
        "/sell/product/list?productIdOrName=" + $("#categoryId").val() + "&pageIndex=" + pageIndex + "&pageSize=" + pageSize,
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
        "<td style='display: table-cell; vertical-align: middle;'>" + data.productId + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.productName + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.productPrice + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.productStock + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.productDescription + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'><img src='" + data.productIcon + "' /></td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.productStatus + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.categoryType + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.createTime + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.updateTime + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" +
            "<button class='btn btn-info' onclick='forUpdate = true;editCategory($(this).parent())'>编辑</button>" +
            "<button class='btn btn-danger' onclick='deleteCategory($(this).parent())'>删除</button>" +
        "</td>\n" +
        "</tr>";
}
function editCategory(tr) {
    $("#edit-header").html("<h4>编辑菜品</h4><h4 style='float: right; cursor: pointer' onclick='cancelSaveCategory()'>×</h4>");

    $("#newProductId").val(tr.parent().children().get(0).innerHTML);
    $("#newProductName").val(tr.parent().children().get(1).innerHTML);
    $("#newProductPrice").val(tr.parent().children().get(2).innerHTML);
    $("#newProductStock").val(tr.parent().children().get(3).innerHTML);
    $("#newProductDescription").val(tr.parent().children().get(4).innerHTML);
    $("#newProductIcon").val(tr.parent().children().get(5).getElementsByTagName("img")[0].src);
    $("#newProductStatus").val(tr.parent().children().get(6).innerHTML);
    $("#newCategoryType").val(tr.parent().children().get(7).innerHTML);

    $("#newProductName").attr("disabled", false);
    $("#newProductPrice").attr("disabled", false);
    $("#newProductDescription").attr("disabled", false);
    $("#newProductIcon").attr("disabled", false);
    $("#newProductStatus").attr("disabled", false);
    $("#newCategoryType").attr("disabled", false);

    $('.mask').css('display', 'block');
}
function newCategoty() {
    $('#edit-header').html("<h4>添加菜品</h4><h4 style='float: right; cursor: pointer' onclick='cancelSaveCategory()'>×</h4>");

    $("#newProductId").attr("disabled", false);
    $("#newProductName").attr("disabled", false);
    $("#newProductPrice").attr("disabled", false);
    $("#newProductStock").attr("disabled", false);
    $("#newProductDescription").attr("disabled", false);
    $("#newCategoryType").attr("disabled", false);

    $('.mask').css('display', 'block');
}
function saveCategory() {
    $.get(
        "/sell/product/save?productId=" + $("#newProductId").val() +
        "&productName=" + $("#newProductName").val() +
        "&categoryType=" + $("#newCategoryType").val() +
        "&productPrice=" + $("#newProductPrice").val() +
        "&productStock=" + $("#newProductStock").val() +
        "&productDescription=" + $("#newProductDescription").val() +
        "&productIcon=" + $("#newProductIcon").val() +
        "&productStatus=" + ($("#newProductStatus").val() == "" ? 0 : $("#newProductStatus").val()) +
        "&forUpdate=" + forUpdate
        ,
        function (data, status) {
            if (data.code == 0) {
                alert("保存成功！");
            } else {
                alert("保存失败！");
            }
            cancelSaveCategory();
            search();
        }
    );
}
function cancelSaveCategory() {
    $('.mask').css('display', 'none');
    $("#newProductId").val("");
    $("#newProductName").val("");
    $("#newProductPrice").val("");
    $("#newProductStock").val("");
    $("#newProductDescription").val("");
    $("#newProductIcon").val("");
    $("#newProductStatus").val("");
    $("#newCategoryType").val("");

    $("#newProductId").attr("disabled", true);
    $("#newProductName").attr("disabled", true);
    $("#newProductPrice").attr("disabled", true);
    $("#newProductStock").attr("disabled", true);
    $("#newProductDescription").attr("disabled", true);
    $("#newProductIcon").attr("disabled", true);
    $("#newProductStatus").attr("disabled", true);
    $("#newCategoryType").attr("disabled", true);
}
function deleteCategory(tr) {
    if (confirm("你确定要删除这个产品吗？") == true) {
        $.get(
            "/sell/product/delete?productId=" + tr.parent().children().get(0).innerHTML,
            function (data, status) {
                if (data.code == 0) {
                    alert("删除成功！");
                    search();
                } else {
                    alert("删除失败！");
                }
            }
        );
    }
}