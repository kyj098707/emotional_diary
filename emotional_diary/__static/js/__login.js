
function error_vib(msg_string){
  let element = $('.vib')
  element.addClass('error_login');
  setTimeout(() => {
      element.removeClass('error_login');
  }, 300) 
  $('#error_msg').text(msg_string)
  document.getElementById('error_msg').style.display = "block";
}

function request_ajax(url, method, data_dic) {
  $.ajax({
      url:url,
      type:method,
      async:false,
      data:data_dic,
      success: function (response) {
              result = response
                  let msg = "임시"
                  if (msg == "error") {
                      error_vib("에러메시지 추가")
                  } else {
                      let val = 1 
                      
                  }
              },
  error: function (e) {
      result = "error"
      error_vib("서버와의 연결에 문제가 있습니다.")
      }
  });
  return result;
}


$(document).on("click","#to_signup", function(){
  const modals = document.querySelector('#modal_signup');
  let modal = bootstrap.Modal.getOrCreateInstance(modals)  
  modal.show()
})

$(document).on("click","#to_findpw", function(){
    const modals = document.querySelector('#modal_findpw');
    let modal = bootstrap.Modal.getOrCreateInstance(modals)  
    modal.show()
  })