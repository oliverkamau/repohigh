$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
setTransDefault()
searchClass()
searchStudent()
formatDate()
transTypeCheck()
savePocketMoney()
})
function setTransDefault() {
$('#assign').prop('checked',true)
$('#transactionType').text('Deposit')
 $('#transType').val('Deposit')
 $("#colorForm").css("background-color", "#FFF0F5");
// $("#colorForm").css("background-color", "#B0E0E6");

}
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#date').val([year, month, day].join('-'));
    $('#dateFrom').val([year, month, day].join('-'));
    $('#dateTo').val([year, month, day].join('-'));
}
function searchClass() {

        $('#class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width: '66%',
            ajax: {
                delay: 250,
                url: 'searchclass',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchStudent() {

        $('#student_frm').select2({
            placeholder: 'Students',
            allowClear: true,
            width: '75%',
            ajax: {
                delay: 250,
                url: 'searchstudents',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function transTypeCheck() {
    $('#assign').change(function () {
        if(this.checked){
            $('#transType').val('Deposit')
            $('#transactionType').text('Deposit')
             $("#colorForm").css("background-color", "#FFF0F5");
        }
        else{
          $('#transType').val('Withdraw')
          $('#transactionType').text('Withdraw')
          $("#colorForm").css("background-color", "#B0E0E6");
        }
    })
}
function savePocketMoney() {
$('#savePocketMoney').click(function () {

  if($('#amount').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Amount to save provided!',
         confirmButtonText: 'OK'
      })
  }
    else if($('#pocketMoneyStudent').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide a Student first to assign the amount to!',
         confirmButtonText: 'OK'
      })
  }
  else {
      var data = new FormData();

      data.append("transType", $('#transType').val())
      data.append("category", $('#categoryCode').val())
      data.append("newcategory", $('#newCategoryCode').val())
      data.append('students', JSON.stringify(assigned))
      $.ajax({
          type: 'POST',
          url: 'assigncategory',
          data: data,
          processData: false,
          contentType: false,
      }).done(function (s) {
            swal.close()
          searchFeeStudent()
          searchNewFeeStudent()
          assigned=[]
        // swal({
        //  type: 'success',
        //  title: 'Success',
        //  text: s.success,
        //  showConfirmButton: true,
     //})
      }).fail(function (xhr, error) {
          swal.close()
          bootbox.alert(xhr.responseText)

      });
  }
})
}