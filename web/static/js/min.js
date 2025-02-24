function submitForm(event) {
  event.preventDefault(); // 阻止表单默认提交行为

  var form = document.getElementById("myForm");
  var url = form.getAttribute("action");
  var method = form.getAttribute("method");

  // 提交表单数据到指定URL
  fetch(url, {
    method: method,
    body: new FormData(form)
  }).then(function(response) {
    // 在新标签页中打开返回的响应页面
    window.open(response.url, "_blank");
  });
}