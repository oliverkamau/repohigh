$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
    getDynamicUrl();
setTransDefault()
searchClass()
searchStudent()
classChange()
studentChange()
formatDate()
transTypeCheck()
savePocketMoney()
newRecord()
getGridValues()
    editStudent()
    reportCheck()
    searchReportStudent()
    studentReportChange()
    $('.elementrep').hide()
    radiotoggle()
    generateReports()
})
function getDynamicUrl() {
   $.ajax({
          type: 'GET',
          url: 'dynamicaddress',
      }).done(function (s) {
       $('#context').val(s.url)
      }).fail(function (xhr, error) {
          bootbox.alert(xhr.responseText)

      });
}
function generateReports(){
$('#generateButton').click(function(){

 var format = $('#format').val()
   if($('#dateFrom').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Date From is required to run report!',
         confirmButtonText: 'OK'
      })
     }
     else if($('#dateFrom').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Date To is required to run report!',
         confirmButtonText: 'OK'
      })
     }else if($('#reportStudent').val()==='' && $('#reportClass').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Student or Class is required to run report!',
         confirmButtonText: 'OK'
      })
     }
     else{
        var context = $('#context').val()
        var id = $('#reportStudent').val()
        var classes = $('#reportClass').val()
        var dateFrom = $('#dateFrom').val()
        var dateTo = $('#dateTo').val()
        if(format==='excel'){

           if($('#reportStudent').val()!=='' && $('#reportClass').val()!==''){
           window.open(context + 'fees/pocket/pocketmoneyindividual?format=excel&name=pocketmoney_individual&id='+id+'&dateFrom='+dateFrom+'&dateTo='+dateTo, '_self');

           }
           else if($('#reportStudent').val()==='' && $('#reportClass').val()!==''){
           window.open(context + 'fees/pocket/pocketmoneyclass?format=excel&name=pocketmoney_class&classes='+classes+'&dateFrom='+dateFrom+'&dateTo='+dateTo, '_self');

           }
           else{
           window.open(context + 'fees/pocket/pocketmoneyindividual?format=excel&name=pocketmoney_individual&id='+id+'&dateFrom='+dateFrom+'&dateTo='+dateTo, '_self');

           }

        }
        else if(format==='pdf'){

           if($('#reportStudent').val()!=='' && $('#reportClass').val()!==''){
           window.open(context + 'fees/pocket/pocketmoneyindividual?format=pdf&name=pocketmoney_individual&id='+id+'&dateFrom='+dateFrom+'&dateTo='+dateTo, '_blank');

           }
           else if($('#reportStudent').val()==='' && $('#reportClass').val()!==''){
            window.open(context + 'fees/pocket/pocketmoneyclass?format=pdf&name=pocketmoney_class&classes='+classes+'&dateFrom='+dateFrom+'&dateTo='+dateTo, '_blank');

           }
           else{
           window.open(context + 'fees/pocket/pocketmoneyindividual?format=pdf&name=pocketmoney_individual&id='+id+'&dateFrom='+dateFrom+'&dateTo='+dateTo, '_blank');

           }

        }
        else{
         swal({
          title: 'Alert!',
          type: 'info',
          text: 'Select a report Format to continue!!',
         confirmButtonText: 'OK'
      })
        }
        }

})


}
 function radiotoggle(){
    $('input[type=radio][name="format"]').change(function() {
        if($('#excel').is(':checked')){
             $('#format').val('excel')
        }
        else if($('#pdf').is(':checked')){
             $('#format').val('pdf')

        }
        })
        }
function newRecord() {
$('#newPocketMoney').click(function () {
clearPage()
})
}
function clearPage(){
    $('#balance').val('')
    $('#amount').val('')
    $('#pocketMoneyStudent').val('')
    $('#student_frm').empty()
}
function setTransDefault() {
$('#assign').prop('checked',true)
$('#transactionType').text('Deposit')
 $('#transType').val('Deposit')
 $("#colorForm").css("background-color", "#FFF0F5");
// $("#colorForm").css("background-color", "#B0E0E6");

}
function getGridValues(){
     $.ajax({
        type: 'GET',
        url: 'getstudents',
        processData: false,
        contentType: false,
    }).done(function (s) {
         $('#pocketTable').DataTable().destroy();
        $("#pocketTable tbody").empty();
        $.each(s,function(i,item){
            $("#pocketTable tbody").append(
                "<tr>"
                +"<td>"+item.admNo+"</td>"
                +"<td>"+item.name+"</td>"
                +"<td>"+item.studentClass+"</td>"
                +"<td>"+item.dorm+"</td>"
                +"<td>"+item.balance+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-student" name="id" value='+item.studentCode+'></form><button class="btn btn-outline-primary btn-sm btn-editstudent" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"</tr>" )
        })
        $('#pocketTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
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
            width: '75%',
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

function searchReportStudent() {

        $('#student_report_frm').select2({
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
function reportCheck() {
    $('#reports').change(function () {
        if(this.checked){
            $('.elementrep').show()
        }
        else{
            $('.elementrep').hide()

        }
    })
}

function getBalance(id) {
     $.ajax({

          type: 'GET',
          url: 'getbalance/'+id,


      }).done(function (s) {
          $('#balance').val(s.balance)
     })
      .fail(function (xhr, error) {

          bootbox.alert(xhr.responseText)

      });
}

function studentChange() {
    $('#student_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#pocketMoneyStudent').val(data.id)
        getBalance(data.id)
    });
    $("#student_frm").on("select2:unselecting", function(e) {
    $('#pocketMoneyStudent').val('')

 });
}
function studentReportChange() {
    $('#student_report_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#reportStudent').val(data.id)
        getBalance(data.id)
    });
    $("#student_report_frm").on("select2:unselecting", function(e) {
    $('#reportStudent').val('')

 });
}
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#reportClass').val(data.id)
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#reportClass').val('')

 });
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
      data.append("student", $('#pocketMoneyStudent').val())
      data.append("balance", $('#balance').val())
      data.append("amount", $('#amount').val())
      data.append("date", $('#date').val())

      $.ajax({

          type: 'POST',
          url: 'savepocketmoney',
          data: data,
          processData: false,
          contentType: false,

      }).done(function (s) {
          if(s.success) {
              swal({
                  type: 'success',
                  title: 'Success',
                  text: s.success,
                  showConfirmButton: true,
              })
              clearPage()
              getGridValues()
          }
          else if(s.timeout){
            swal({
                title: 'Alert!',
                 type: 'info',
                 text: s.timeout,
                 confirmButtonText: 'OK'
                      })
                       setInterval('refreshPage()', 3 * 1000);
                    }
                else{
                       swal({
                        title: 'Alert!',
                       type: 'info',
                       text: 'Your User Session expired!',
                        confirmButtonText: 'OK'
                      })
                       setInterval('refreshPage()', 3 * 1000);
                    }
      }).fail(function (xhr, error) {

          bootbox.alert(xhr.responseText)

      });
  }
})
}
function refreshPage() {

    window.location.reload()

    }
function editStudent(){
    $('#pocketTable').on('click','.btn-editstudent',function (s) {
        var data=$(this).closest('tr').find('#edit-student').val();
        	 $.ajax({

          type: 'GET',
          url: 'getstudentgrid/'+data,

      }).done(function (s) {
          	if (s.studentCode) {
			    var $newStat = $("<option selected='selected' value='" + s.studentCode + "'>'+s.studentName+'</option>").val(s.studentCode.toString()).text(s.studentName)

               $('#student_frm').append($newStat).trigger('change');
			   $('#pocketMoneyStudent').val(s.studentCode)

			    }
          	else {
			    $('#student_frm').empty();
			    $('#pocketMoneyStudent').val('')

			}
          	$('#balance').val(s.balance)

     })
      .fail(function (xhr, error) {

          bootbox.alert(xhr.responseText)

      });
    });

}