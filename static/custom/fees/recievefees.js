
$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });

formatDate();
getFeeDistribution();
searchClass();
classChange();
searchStudent("");
searchBank();
studentChange();
bankChange();
modeChange();
searchPaymentModes();
searchTerm();
getFeeStandardCharges();
termChange();
saveFees();
addTotals();
getDefaultTerm();
removeTotals();
newFee();
radiotoggle();
})
function newFee() {
$('#newFees').click(function () {
clearpage();
})
}
function clearpage(){
    getFeeStandardCharges()
    $('#balance').val("0")
    $('#amountPaid').val("0")
    $('#amountPayable').val("0")
    $('#docNo').val('')
    $('#feeStudent').val('')
    $('#student_frm').empty()
    $('#feesClass').val('')
    $('#class_frm').empty()
    $('#paymentMode').val('')
    $('#payment_frm').empty()
    $('#bankBranch').val('')
    $('#bank_frm').empty()
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

}
function getFeeDistribution() {
    $.ajax({
                type: 'GET',
                url: 'feedistribution',
            }).done(function (s) {

              $('input[type=radio][name=distribution]').val()===s.mode
              $('input[type=radio][name=distribution][value='+s.mode+']').prop('checked',true)

            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)

            })
}
function saveFees(){
 $('#saveFees').click(function () {
        if($('#feeStudent').val()===''){
               swal({
          title: 'Alert!',
          type: 'info',
          text: 'Student Field is mandatory'
      })
        }
        else if($('#paymentMode').val()===''){
             swal({
          title: 'Alert!',
          type: 'info',
          text: 'Payment Mode is mandatory'
      })
        }
        else if($('#bankBranch').val()===''){
             swal({
          title: 'Alert!',
          type: 'info',
          text: 'Bank Paid from is mandatory'
      })
        }
           else if($('#feesTerm').val()===''){
             swal({
          title: 'Alert!',
          type: 'info',
          text: 'Term Paid is mandatory'
      })
        }
                  else if($('#docNo').val()===''){
             swal({
          title: 'Alert!',
          type: 'info',
          text: 'Document Number is mandatory'
      })
        }
        else {
            var form = $("#fees_form")[0];
            var data = new FormData(form);
            data.append('student',$('#feeStudent').val())
            data.append('classcode',$('#feesClass').val())
            data.append('mode',$('#paymentMode').val())
            data.append('bank',$('#bankBranch').val())
            data.append('document',$('#docNo').val())
            data.append('term',$('#feesTerm').val())
            data.append('date',$('#date').val())

            $.ajax({
                type: 'POST',
                url: 'recievefees',
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
              clearpage();
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)

            })

        }
	})
}
function radiotoggle(){
    $('input[type=radio][name="distribution"]').change(function() {
    if (this.value === 'manual') {
       if($('#feeStudent').val()===''){
           getFeeStandardCharges()
       }
       else{
           getFeeTrackerBalance($('#feeStudent').val())
       }
    }
    else if (this.value === 'automatic') {
       if($('#feeStudent').val()===''){
           getFeeStandardCharges()
       }
       else{
           getFeeTrackerBalance($('#feeStudent').val())
       }

    }
});
}
function searchClass() {

        $('#class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width: '67%',
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
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#feesClass').val(data.id)
        searchStudent(data.id)
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#feesClass').val('')

 });
}
function termChange() {
    $('#term_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#feesTerm').val(data.id)
    });
    $("#term_frm").on("select2:unselecting", function(e) {
    $('#feesTerm').val('')

 });
}
function modeChange() {
    $('#payment_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#paymentMode').val(data.id)
    });
    $("#payment_frm").on("select2:unselecting", function(e) {
    $('#paymentMode').val('')

 });
}

function bankChange() {
    $('#bank_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#bankBranch').val(data.id)
    });
    $("#bank_frm").on("select2:unselecting", function(e) {
    $('#bankBranch').val('')

 });
}

function getFeeTrackerBalance(id) {
  $.ajax({
        type: 'GET',
        url: 'getrackerbalances/'+id,
        processData: false,
        contentType: false,
    }).done(function (s) {
        $("#append-form").empty()
        var total = 0;
        if(s.length!==0) {
            $.each(s, function (i, item) {
              if($('input[type=radio][name=distribution]:checked').val()==='manual') {

                  $("#append-form").append(
                      "<div class='col-md-11 col-sm-12 chargeme'>"
                      + "<div class='form-row ml-1 mr-1 chargenext'>"
                      + "<input type='hidden' name='" + item.tracker + "' id='" + item.trackerCode + "' value='" + item.trackerCode + "'>"
                      + "<label class='col-md-5 control-label' for='select'>" + item.chargeName + "</label>"
                      + "<input type='number' name='" + item.chargeAmountName + "' class='form-control col-md-3 mr-1 charges' id='" + item.chargeAmountName + "'>"
                      + "<input type='number' name='" + item.trackerAmountName + "' class='form-control col-md-3' id='" + item.trackerAmountName + "'  value='" + item.trackerAmountValue + "' readonly>"
                      + "</div>"
                      + "<div class='form-row mr-1'>"
                      + "</div>"
                      + "</div>")
                  total = total + parseFloat(item.trackerAmountValue)
                  $('#amountPayable').val(total.toFixed(2).toString())
                  $('#amountPaid').val('0')
                  $('#balance').val('0')
                  $('#amountPaid').prop('disabled',true)

              }
              else{
                  $("#append-form").append(
                      "<div class='col-md-11 col-sm-12 chargeme'>"
                      + "<div class='form-row ml-1 mr-1 chargenext'>"
                      + "<input type='hidden' name='" + item.tracker + "' id='" + item.trackerCode + "' value='" + item.trackerCode + "'>"
                      + "<label class='col-md-5 control-label' for='select'>" + item.chargeName + "</label>"
                      + "<input type='number' name='" + item.chargeAmountName + "' class='form-control col-md-3 mr-1 charges' id='" + item.chargeAmountName + "' readonly>"
                      + "<input type='number' name='" + item.trackerAmountName + "' class='form-control col-md-3' id='" + item.trackerAmountName + "'  value='" + item.trackerAmountValue + "' readonly>"
                      + "</div>"
                      + "<div class='form-row mr-1'>"
                      + "</div>"
                      + "</div>")
                    total = total + parseFloat(item.trackerAmountValue)
                  $('#amountPayable').val(total.toFixed(2).toString())
                 $('#amountPaid').val('0')
                 $('#balance').val('0')
                 $('#amountPaid').prop('disabled',false)

              }
            })

        }

    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}

function computetotal(val) {
    console.log(val)
    console.log($('#amountPaid').val())
     var amp=parseFloat($('#amountPaid').val())+parseFloat(val)
     $('#amountPaid').val(amp.toFixed(2).toString())
     var amt=parseFloat($('#amountPayable').val())-parseFloat($('#amountPaid').val())
     $('#balance').val(amt.toFixed(2).toString())
}

function addTotals(){

    $('#append-form').on('focusout','.chargeme .chargenext .charges',function () {
        var val = 0
        if($(this).val()===''){
            val = 0
        }
        else{
            val = $(this).val()
        }
       computetotal(val)
    })
}

function subtracttotals(val) {
         var amp=parseFloat($('#amountPaid').val())-parseFloat(val)
         $('#amountPaid').val(amp.toFixed(2).toString())
         var amt=parseFloat($('#amountPayable').val())-parseFloat($('#amountPaid').val())
         $('#balance').val(amt.toFixed(2).toString())
}

function removeTotals(){

    $('#append-form').on('focus','.chargeme .chargenext .charges',function () {
        var val = 0
        if($(this).val()===''){
            val = 0
        }
        else{
            val = $(this).val()
        }
       subtracttotals(val)
    })
}
function getDefaultTerm(){
    $.ajax({
                type: 'GET',
                url: 'currentterm',
            }).done(function (s) {
               if (s.termCode) {
                $('#feesTerm').val(s.termCode)
                var $newClass = $("<option selected='selected' value='" + s.termCode + "'>'+s.termNumber+'</option>").val(s.termCode.toString()).text(s.termNumber)

                $('#term_frm').append($newClass).trigger('change');
            }
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)

            })
}
function studentChange() {
    $('#student_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#feeStudent').val(data.id)
        $('#amountPaid').val('0')
        getFeeTrackerBalance(data.id)
    });
    $("#student_frm").on("select2:unselecting", function(e) {
    $('#feeStudent').val('')

 });
}
function searchStudent(id) {

        $('#student_frm').select2({
            placeholder: 'Students',
            allowClear: true,
            width: '67%',
            ajax: {
                delay: 250,
                url: 'searchstudents/'+id,
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

function searchBank() {

        $('#bank_frm').select2({
            placeholder: 'Banks',
            allowClear: true,
            width: '58%',
            ajax: {
                delay: 250,
                url: 'searchbanks',
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
function searchPaymentModes() {

        $('#payment_frm').select2({
            placeholder: 'Payment Mode',
            allowClear: true,
            width: '58%',
            ajax: {
                delay: 250,
                url: 'searchmodes',
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

function getFeeStandardCharges() {
      $.ajax({
        type: 'GET',
        url: 'getfeestandardcharges',
        processData: false,
        contentType: false,
    }).done(function (s) {
        $("#append-form").empty()
        if(s.length!==0) {
            $.each(s, function (i, item) {
              if($('input[type=radio][name=distribution]:checked').val()==='manual') {

                  $("#append-form").append(
                      "<div class='col-md-11 col-sm-12'>"
                      + "<div class='form-row ml-1 mr-1'>"
                      + "<input type='hidden' name='" + item.chargeCodeName + "' id='" + item.chargeCodeName + "' value='" + item.chargeCode + "'>"
                      + "<label class='col-md-5 control-label' for='select'>" + item.chargeName + "</label>"
                      + "<input type='number' name='" + item.chargeAmount + "' class='form-control col-md-3 mr-1' id='" + item.chargeAmount + "'>"
                      + "<input type='number' name='" + item.chargeAmount + "' class='form-control col-md-3' id='" + item.chargeAmount + "'  readonly>"

                      + "</div>"
                      + "<div class='form-row mr-1'>"
                      + "</div>"
                      + "</div>"
                  )

                  $('#amountPaid').prop('disabled',true)
              }
              else{
                   $("#append-form").append(
                      "<div class='col-md-11 col-sm-12'>"
                      + "<div class='form-row ml-1 mr-1'>"
                      + "<input type='hidden' name='" + item.chargeCodeName + "' id='" + item.chargeCodeName + "' value='" + item.chargeCode + "'>"
                      + "<label class='col-md-5 control-label' for='select'>" + item.chargeName + "</label>"
                      + "<input type='number' name='" + item.chargeAmount + "' class='form-control col-md-3 mr-1' id='" + item.chargeAmount + "' readonly>"
                      + "<input type='number' name='" + item.chargeAmount + "' class='form-control col-md-3' id='" + item.chargeAmount + "'  readonly>"

                      + "</div>"
                      + "<div class='form-row mr-1'>"
                      + "</div>"
                      + "</div>"
                  )
                  $('#amountPaid').prop('disabled',false)
              }
            })
        }

    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}
function searchTerm() {

        $('#term_frm').select2({
            placeholder: 'Term',
            allowClear: true,
            width: '65%',
            ajax: {
                delay: 250,
                url: 'searchterm',
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