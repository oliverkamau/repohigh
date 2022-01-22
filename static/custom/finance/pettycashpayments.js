$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
formatDate()
searchAccounts()
    searchUsers()
    accountChange()
    userChange()
    amountToWords()
   savePettyCash()
getGridValues()
    editPetty()
    newPettyCash()
})
function newPettyCash(){
    $('#newPettyCash').click(function (){
        clearPage()
    })
}
function clearPage(){

    $("#petty-form")[0].reset()
    formatDate()
    $('#pettyCode').val("")
    $('#amountWords').val("")
    $('#account').val('')
    $('#account_frm').empty()
    $('#description').val('')
    $('#paidby_frm').empty()
    $('#paidBy').val('')

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

    $('#pettyDate').val([year, month, day].join('-'));

}
function searchAccounts() {

        $('#account_frm').select2({
            placeholder: 'Accounts',
            allowClear: true,
            width: '66%',
            ajax: {
                delay: 250,
                url: 'searchaccount',
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

function searchUsers() {

        $('#paidby_frm').select2({
            placeholder: 'Paid By',
            allowClear: true,
            width: '66%',
            ajax: {
                delay: 250,
                url: 'searchusers',
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
function accountChange() {
    $('#account_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#account').val(data.id)
    });
    $("#account_frm").on("select2:unselecting", function(e) {
    $('#account').val('')

 });
}
function userChange() {
    $('#paidby_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#paidBy').val(data.id)
    });
    $("#paidby_frm").on("select2:unselecting", function(e) {
    $('#paidBy').val('')

 });
}
function amountToWords(){
    $('#amount').on('input',function (){
        var words = toWords($('#amount').val())
        $('#wording').val(words)
                $('#amountWords').val(words)

    })
}
function savePettyCash(){
 $('#savePettyCash').click(function () {

        if($('#payee').val()==''){
         swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide a Payee!',
         confirmButtonText: 'OK'
      })
        }
        else if($('#account').val()==='') {
            swal({
                title: 'Alert!',
                type: 'info',
                text: 'Provide an Account!',
                confirmButtonText: 'OK'
            })
        }
            else if($('#amount').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide an amount to pay',
         confirmButtonText: 'OK'
      })
        }
         else if($('#paidBy').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide the User that paid the money!',
         confirmButtonText: 'OK'
      })
        }

        else {
            if ($('#pettyCode').val() === '') {


                var form = $("#petty-form")[0];
                var data = new FormData(form);

                $.ajax({
                    type: 'POST',
                    url: 'savepettycash',
                    data: data,
                    processData: false,
                    contentType: false
                }).done(function (s) {
                    swal({
                        type: 'success',
                        title: 'Success',
                        text: s.success,
                        showConfirmButton: true
                    })
                    getGridValues()
                    clearPage()
                }).fail(function (xhr, error) {
                    bootbox.alert(xhr.responseText)
                })

            }
            else{
                         swal({
          title: 'Alert!',
          type: 'info',
          text: 'Editing of financial records is not allowed!',
         confirmButtonText: 'OK'
      })
            }
        }
	})
}
function getGridValues(){
     $.ajax({
        type: 'GET',
        url: 'getpettycashgrid',
        processData: false,
        contentType: false,
    }).done(function (s) {
         $('#pettyTable').DataTable().destroy();
        $("#pettyTable tbody").empty();
        $.each(s,function(i,item){
            $("#pettyTable tbody").append(
                "<tr>"
                  +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-petty" name="id" value='+item.code+'></form><button class="btn btn-outline-primary btn-sm btn-editpetty" ><i class="fa fa-edit"></button>'
                 +"</td>"
                +"<td>"+item.date+"</td>"
                +"<td>"+item.amount+"</td>"
                +"<td>"+item.wording+"</td>"
                +"<td>"+item.purpose+"</td>"
                +"<td>"+item.account+"</td>"
                +"<td>"+item.payee+"</td>"
                +"<td>"+item.payer+"</td>"
                +"<td>"+item.trans+"</td>"
                +"<td>"+item.voucher+"</td>"
                +"<td>"+item.receipt+"</td>"
                +"</tr>" )
        })
        $('#pettyTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}

function editPetty(){
    $('#pettyTable').on('click','.btn-editpetty',function (s) {
        var data=$(this).closest('tr').find('#edit-petty').val();
        	 $.ajax({

          type: 'GET',
          url: 'geteditpetty/'+data,

      }).done(function (s) {
          $('#pettyCode').val(s.code)
          	if (s.accountCode) {
			    var $newStat = $("<option selected='selected' value='" + s.accountCode + "'>'+s.accountName+'</option>").val(s.accountCode.toString()).text(s.accountName)

               $('#account_frm').append($newStat).trigger('change');
			   $('#account').val(s.accountCode)

			    }
          	else {
			    $('#account_frm').empty();
			    $('#account').val('')

			}
          		if (s.givenbyCode) {
			    var $newSt = $("<option selected='selected' value='" + s.givenbyCode + "'>'+s.givenbyName+'</option>").val(s.givenbyCode.toString()).text(s.givenbyName)

               $('#paidby_frm').append($newSt).trigger('change');
			   $('#paidBy').val(s.givenbyCode)

			    }
          	else {
			    $('#paidby_frm').empty();
			    $('#paidBy').val('')

			}

          	$('#payee').val(s.payee)
            $('#docNo').val(s.docno)
            $('#amount').val(s.amount)
            $('#wording').val(s.wording)
            $('#pettyDate').val(s.date)
            $('#description').val(s.trans)
            $('#date').val(s.date)

     })
      .fail(function (xhr, error) {

          bootbox.alert(xhr.responseText)

      });
    });

}