
$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
    searchStudent();
    studentChange();
    formatDate();
    updateTrackerDetails();
})
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
function studentChange() {
    $('#student_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentCode').val(data.id)
        getFeeStandardCharges(data.id)
    });
    $("#student_frm").on("select2:unselecting", function(e) {
    $('#studentCode').val('')
 });
}
function updateTrackerDetails(){
 $('#saveInvoice').click(function () {
        if($('#trackerRemarks').val()==='' || $('#studentCode').val()===''){
               swal({
          title: 'Alert!',
          type: 'info',
          text: 'Remarks and Student Fields are mandatory'
      })
        }
        else {
            var form = $("#tracker-form")[0];
            var data = new FormData(form);
            data.append('student',$('#studentCode').val())
            data.append('notes',$('#trackerRemarks').val())
            data.append('date',$('#date').val())
            $.ajax({
                type: 'POST',
                url: 'updatebalancetracker',
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
                $('#structure-form')[0].reset()
                $('#structureCode').val('')
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)

            })

        }
	})
}
function searchStudent() {

        $('#student_frm').select2({
            placeholder: 'Students',
            allowClear: true,
            width: '67%',
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
function getFeeStandardCharges(id) {
      $.ajax({
        type: 'GET',
        url: 'getfeestandardcharges/'+id,
        processData: false,
        contentType: false,
    }).done(function (s) {

        if(s.length!==0) {
            $("#append-form").empty()
            $.each(s, function (i, item) {
                $('#trackerCode').val(item.trackerCode)
                $("#append-form").append(
                    "<div class='col-md-6 col-sm-12'>"
                    +"<div class='form-row mb-2 ml-1 mr-2'>"
                    + "<input type='hidden' name='"+item.chargeCodeName+"' id='"+item.chargeCodeName+"' value='"+item.chargeCode+"'>"
                    + "<label class='col-md-5 control-label' for='select'>"+item.chargeName+"</label>"
                    + "<input type='number' name='"+item.chargeAmount+"' class='form-control col-md-7' id='"+item.chargeAmount+"' value='"+parseFloat(item.ammount)+"'>"
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