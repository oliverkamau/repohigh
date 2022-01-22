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
    getCumulative()
replenishFloat()
    getGridValues()
    newFloat()
    editFloat()
})
function newFloat(){
    $('#newFloat').click(function (){
        clearPage()
    })
}
function clearPage(){

    $("#float-form")[0].reset()
    formatDate()
    $('#cf').text("")
    $('#accountBalance').text("")
    $('#floatReceiver').val('')
    $('#givento_frm').empty()
    $('#account').val('')
    $('#account_frm').empty()
    $('#floatCode').val('')

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

    $('#floatDate').val([year, month, day].join('-'));

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

        $('#givento_frm').select2({
            placeholder: 'Given To',
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
        getBalance()
    });
    $("#account_frm").on("select2:unselecting", function(e) {
    $('#account').val('')

 });
}
function getBalance(){
      $.ajax({
                type: 'POST',
                url: 'balance/'+ $('#account').val(),

            }).done(function (s) {
            $('#accountBalance').text(s.balance);
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })
}

function getCurrentFloat() {
     $.ajax({
                type: 'POST',
                url: 'float/'+ $('#floatReceiver').val(),

            }).done(function (s) {
            $('#balance').val(s.float);
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })
}
function getCumulative(){
    $('#amount').on('input',function (){
        if($('#amount').val()===''){
          $('#cf').text(0)
        }else {
            var p = parseFloat($('#amount').val()) + parseFloat($('#balance').val())
            $('#cf').text(p)
        }
    })
}

function userChange() {
    $('#givento_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#floatReceiver').val(data.id)
        getCurrentFloat()
    });
    $("#givento_frm").on("select2:unselecting", function(e) {
    $('#floatReceiver').val('')

 });
}
function amountToWords(){
    $('#amount').on('input',function (){
        var words = toWords($('#amount').val())
        $('#wording').val(words)
                $('#amountWords').val(words)

    })
}
function replenishFloat(){
    $('#saveFloat').click(function () {

        if($('#floatReceiver').val()==''){
         swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide a Reciever of the float!',
         confirmButtonText: 'OK'
      })
        }
        else if($('#account').val()==='') {
            swal({
                title: 'Alert!',
                type: 'info',
                text: 'Provide an Account to draw from!',
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

        else {
            if ($('#floatCode').val() === '') {

                var form = $("#float-form")[0];
                var data = new FormData(form);

                $.ajax({
                    type: 'POST',
                    url: 'savefloatcash',
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
                    clearPage()
                    getGridValues()
                }).fail(function (xhr, error) {
                    bootbox.alert(xhr.responseText)
                })

            }
             else {
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
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })

        }
	})
}

function getGridValues(){
     $.ajax({
        type: 'GET',
        url: 'getfloatgrid',
        processData: false,
        contentType: false,
    }).done(function (s) {
         $('#replenishTable').DataTable().destroy();
        $("#replenishTable tbody").empty();
        $.each(s,function(i,item){
            $("#replenishTable tbody").append(
                "<tr>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-float" name="id" value='+item.code+'></form><button class="btn btn-outline-primary btn-sm btn-editfloat" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+item.date+"</td>"
                +"<td>"+item.amount+"</td>"
                +"<td>"+item.balance+"</td>"
                +"<td>"+item.givento+"</td>"
                +"<td>"+item.givenby+"</td>"
                +"<td>"+item.account+"</td>"
                +"<td>"+item.docno+"</td>"
                +"</tr>" )
        })
        $('#replenishTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}

function editFloat(){
    $('#replenishTable').on('click','.btn-editfloat',function (s) {
        var data=$(this).closest('tr').find('#edit-float').val();
        	 $.ajax({

          type: 'GET',
          url: 'geteditfloat/'+data,

      }).done(function (s) {
          $('#floatCode').val(s.code)
          	if (s.accountCode) {
			    var $newStat = $("<option selected='selected' value='" + s.accountCode + "'>'+s.accountName+'</option>").val(s.accountCode.toString()).text(s.accountName)

               $('#account_frm').append($newStat).trigger('change');
			   $('#account').val(s.accountCode)

			    }
          	else {
			    $('#account_frm').empty();
			    $('#account').val('')

			}
          		if (s.giventoCode) {
			    var $newSt = $("<option selected='selected' value='" + s.giventoCode + "'>'+s.giventoName+'</option>").val(s.giventoCode.toString()).text(s.giventoName)

               $('#givento_frm').append($newSt).trigger('change');
			   $('#floatReceiver').val(s.giventoCode)

			    }
          	else {
			    $('#givento_frm').empty();
			    $('#floatReceiver').val('')

			}

          	$('#amount').val(s.amount)
            $('#balance').val(s.balance)
            $('#accountBalance').text(s.accountBalance)
            $('#givenBy').text(s.givenbyName)
            $('#cf').text(parseFloat(s.amount) + parseFloat(s.balance))
            $('#docNo').val(s.docno)
            $('#date').val(s.date)

     })
      .fail(function (xhr, error) {

          bootbox.alert(xhr.responseText)

      });
    });

}