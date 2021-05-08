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
        "/category/list?categoryIdOrName=" + $("#categoryId").val() + "&pageIndex=" + pageIndex + "&pageSize=" + pageSize,
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
        "<td style='display: table-cell; vertical-align: middle;'>" + data.categoryId + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.name + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" + data.type + "</td>\n" +
        "<td style='display: table-cell; vertical-align: middle;'>" +
            "<button class='btn btn-info' onclick='editCategory($(this).parent())'>编辑</button>" +
            "<button class='btn btn-danger' onclick='deleteCategory($(this).parent())'>删除</button>" +
        "</td>\n" +
        "</tr>";
}
function editCategory(tr) {
    $("#edit-header").html("<h4>编辑类目</h4><h4 style='float: right; cursor: pointer' onclick='cancelSaveCategory()'>×</h4>");
    $("#newCategoryId").val(tr.parent().children().get(0).innerHTML);
    $("#newCategoryName").val(tr.parent().children().get(1).innerHTML);
    $("#newCategoryType").val(tr.parent().children().get(2).innerHTML);
    $('.mask').css('display', 'block');
}
function newCategoty() {
    $('#edit-header').html("<h4>添加类目</h4><h4 style='float: right; cursor: pointer' onclick='cancelSaveCategory()'>×</h4>");
    $('.mask').css('display', 'block');
}
function saveCategory() {
    $.get(
        "/sell/category/save?categoryId=" + $("#newCategoryId").val() + "&categoryName=" + $("#newCategoryName").val() + "&categoryType=" + $("#newCategoryType").val(),
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
    $("#newCategoryId").val("");
    $("#newCategoryName").val("");
    $("#newCategoryType").val("");
}
function deleteCategory(tr) {
    if (confirm("你确定要删除这条类目吗？") == true) {
        $.get(
            "/sell/category/delete?categoryId=" + tr.parent().children().get(0).innerHTML,
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