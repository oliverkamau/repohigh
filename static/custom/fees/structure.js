
$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });

searchFeeCategory();
searchTerm();
termChange();
feeChange();
getFeeStandardCharges();
saveFeeStructure();
getStructures();
editFeeStructure();
newPage();
deleteFeeStructure();
})
function newPage() {
    $('#newStructure').click(function () {
        window.location.reload()
    })
}
function termChange() {
    $('#term_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#termCode').val(data.id)
    });
    $("#term_frm").on("select2:unselecting", function(e) {
    $('#termCode').val('')

 });
}
function saveFeeStructure() {
 $('#saveStructure').click(function () {
        if($('#termCode').val()==='' || $('#feeCategory').val()===''){
               swal({
          title: 'Alert!',
          type: 'info',
          text: 'Term and Fee Category are mandatory'
      })
        }
        else {
            var form = $("#structure-form")[0];
            var data = new FormData(form);
            var url = '';
            if ($('#structureCode').val() === '') {
                url = 'addfeestructure'
            } else {
                url = 'updatefeestructure/' + $('#structureCode').val()
            }
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false
            }).done(function (s) {
            getStructures()

                swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })
                $('#structure-form')[0].reset()
                $('#structureCode').val('')
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)

            })

        }
	})
}

function feeChange() {
    $('#fee_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#feeCategory').val(data.id)


    });
    $("#fee_frm").on("select2:unselecting", function(e) {
    $('#feeCategory').val('')
 });
}
function searchTerm() {
        $('#term_frm').select2({
            placeholder: 'Term',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamterm',
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

function searchFeeCategory() {
     $('#fee_frm').select2({
           placeholder: 'Fee Category',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchfeecategory',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function editFeeStructure(){
    $('#feeTable').on('click','.btn-editFee',function (s) {
        var data=$(this).closest('tr').find('#edit-fee').val();
        $.ajax({
            type: 'GET',
            url: 'editfeestructure/'+data,
        }).done(function (w) {
            var total = 0;
            if(w.length!==0) {
            $.each(w, function (i, s) {

                $('#structureCode').val(s.structureCode)

                if (s.termCode) {
                    $('#termCode').val(s.termCode)
                    var $newTerm = $("<option selected='selected' value='" + s.termCode + "'>'+s.termNumber+'</option>").val(s.termCode.toString()).text(s.termNumber)
                    $('#term_frm').append($newTerm).trigger('change');
                } else {
                    $('#termCode').val('')
                    $('#term_frm').empty();
                }
                if (s.categoryCode) {
                    $('#feeCategory').val(s.categoryCode)

                    var $newOption = $("<option selected='selected' value='" + s.categoryCode + "'>'+s.categoryName+'</option>").val(s.categoryCode.toString()).text(s.categoryName)

                    $('#fee_frm').append($newOption).trigger('change');
                } else {
                    $('#feeCategory').val('')

                    $('#fee_frm').empty();

                }
                  total=total+parseFloat(s.value)
                 $('#text-total').text("Total Balance : "+total.toFixed(2).toString())
                 $('#'+s.id+'').val(s.value)

            })
            }


        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function deleteFeeStructure() {
     $('#feeTable').on('click','.btn-deleteFee',function (s) {
        var data = $(this).closest('tr').find('#delete-fee').val();
        bootbox.confirm("Are you sure want to delete this Fee Structure?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deletefeestructure/'+data,

        }).done(function (s) {
            getStructures()
                   swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}
function getFeeStandardCharges() {
      $.ajax({
        type: 'GET',
        url: 'getfeestandardcharges',
        processData: false,
        contentType: false,
    }).done(function (s) {

        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#append-form").append(
                    "<div class='col-md-6 col-sm-12'>"
                    +"<div class='form-row mb-2 ml-1 mr-2'>"
                    + "<input type='hidden' name='"+item.chargeCodeName+"' id='"+item.chargeCodeName+"' value='"+item.chargeCode+"'>"
                    + "<label class='col-md-5 control-label' for='select'>"+item.chargeName+"</label>"
                    + "<input type='number' name='"+item.chargeAmount+"' class='form-control col-md-6' id='"+item.chargeAmount+"' value='"+parseFloat('0.00')+"'>"
                    + "</div>"
                    +"<div class='form-row mb-2 mr-1'>"
                    +      "</div>"
                    + "</div>")
            })
        }

    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}
function getStructures() {
     $.ajax({
        type: 'GET',
        url: 'getfeestructures',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#feeTable').DataTable().destroy();
       $("#feeTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#feeTable tbody").append(
                    "<tr scope='col'>"
                    + "<td>" + item.feeCategory + "</td>"
                    + "<td>" + item.feeTerm + "</td>"
                    + "<td>" + item.feeYear + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-fee" name="id" value=' + item.structureCode + '></form><button class="btn btn-outline-primary btn-sm btn-editFee" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-fee" name="id" value=' + item.structureCode + '></form><button class="btn btn-outline-danger btn-sm btn-deleteFee" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#feeTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}